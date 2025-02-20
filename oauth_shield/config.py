from typing import Literal, Annotated, Any

from pydantic import computed_field, BeforeValidator, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi.templating import Jinja2Templates

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=".env", env_ignore_empty=True, extra="ignore"
    # )

    SERVICE_NAME: str = "OAuth Shield"

    DOMAIN: str = "localhost:8000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = [
        "http://localhost:8000"
    ]


    TEMPLATES_DIR: str = "templates"
    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""
    SCOPES: list = []
    AUTHORIZATION_BASE_URL: str = ""
    TOKEN_URL: str = ""
    KEYS_URL: str = ""
    SECRET_KEY: str = ""

    REDIRECT_PATH: str = "/__oauth/callback"
    LOGOUT_PATH: str = "/__oauth/logout"
    LOGIN_PATH: str = "/__oauth/login"
    INVALID_DOMAIN_PATH: str = "/__oauth/invalid_domain"

    STATIC_PATH: str = "site"

    AUTHORIZED_DOMAINS: list = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def redirect_url(self) -> str:
        return f"{settings.server_host}/__oauth/callback"


settings = Settings()
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)