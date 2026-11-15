import os
from dataclasses import dataclass

from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: list[str]


def get_settings() -> Settings:
    """Load and validate application settings from the environment."""
    database_url = os.getenv("DATABASE_URL", "").strip()

    if not database_url:
        raise RuntimeError("A variável de ambiente DATABASE_URL é obrigatória.")

    try:
        parsed_url = make_url(database_url)
    except ArgumentError as exc:
        raise RuntimeError("A variável DATABASE_URL contém uma URL inválida.") from exc

    if (
        not isinstance(parsed_url, URL)
        or not parsed_url.drivername
        or "://" not in database_url
    ):
        raise RuntimeError("A variável DATABASE_URL contém uma URL inválida.")

    cors_origins = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]

    return Settings(database_url=database_url, cors_origins=cors_origins)
