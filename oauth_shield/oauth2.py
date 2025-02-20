import jwt
from typing import Annotated

from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware


from sqlmodel import SQLModel, Field

from requests_oauthlib import OAuth2Session

from oauth_shield.config import settings, templates


oauth2_client = OAuth2Session(
    settings.CLIENT_ID,
    redirect_uri=settings.redirect_url,
    scope=settings.SCOPES,
)


class AuthenticatedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in [
            settings.REDIRECT_PATH,
            settings.LOGIN_PATH,
            settings.LOGOUT_PATH,
            settings.INVALID_DOMAIN_PATH,
        ]:
            return await call_next(request)

        openid = request.session.get("openID")
        if not openid:
            return RedirectResponse(settings.LOGIN_PATH)

        return await call_next(request)


router = APIRouter()


class OIDCCallbackDM(SQLModel):
    state: str | None = Field(nullable=True, default=None)
    code: str | None = Field(nullable=True, default=None)
    scope: str | None = Field(nullable=True, default=None)
    authuser: str | None = Field(nullable=True, default=None)
    prompt: str | None = Field(nullable=True, default=None)


def callback(filter_query: Annotated[OIDCCallbackDM, Query()], request: Request):
    token = oauth2_client.fetch_token(
        settings.TOKEN_URL,
        client_secret=settings.CLIENT_SECRET,
        code=filter_query.code,
    )

    id_token = token.get("id_token")
    jwks_client = jwt.PyJWKClient(settings.KEYS_URL)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)

    openid = jwt.decode(
        id_token,
        signing_key.key,
        algorithms=signing_key.algorithm_name,
        audience=settings.CLIENT_ID,
    )

    if settings.AUTHORIZED_DOMAINS:
        _, domain = openid.get("email", " @ ").split("@")
        if domain.strip().lower() not in [d.lower() for d in settings.AUTHORIZED_DOMAINS]:
            return RedirectResponse(f"{settings.INVALID_DOMAIN_PATH}?domain={domain}")

    request.session["openID"] = openid
    return RedirectResponse("/")


def logout(request: Request):
    if "openID" in request.session:
        request.session.pop("openID")
    return RedirectResponse("/")


def login(request: Request):
    authorization_url, _ = oauth2_client.authorization_url(
        settings.AUTHORIZATION_BASE_URL
    )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "authorization_url": authorization_url,
            "title": settings.SERVICE_NAME,
        },
    )


def invalid_domain(request: Request):
    domain = request.query_params.get("domain")
    authorization_url, _ = oauth2_client.authorization_url(
        settings.AUTHORIZATION_BASE_URL
    )

    return templates.TemplateResponse(
        request=request,
        name="invalid_domain.html",
        context={
            "authorization_url": authorization_url,
            "title": settings.SERVICE_NAME,
            "domain": domain,
        },
    )


router.add_api_route(settings.REDIRECT_PATH, callback, methods=["GET"])
router.add_api_route(settings.LOGOUT_PATH, logout, methods=["GET"])
router.add_api_route(
    settings.LOGIN_PATH, login, methods=["GET"], response_class=HTMLResponse
)
router.add_api_route(
    settings.INVALID_DOMAIN_PATH,
    invalid_domain,
    methods=["GET"],
    response_class=HTMLResponse,
)
