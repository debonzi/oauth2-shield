from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from oauth_shield.config import settings
from oauth_shield.oauth2 import AuthenticatedMiddleware, router as oauth_router


app = FastAPI(
    title=settings.SERVICE_NAME,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(AuthenticatedMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


app.include_router(oauth_router)
app.mount("/", StaticFiles(directory=settings.STATIC_PATH, html=True), name="static")
