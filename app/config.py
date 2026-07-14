"""Application settings."""
from functools import lru_cache


class Settings:
    app_name: str = "Event & Conference Management Platform"
    version: str = "1.0.0"
    debug: bool = True
    # Placeholder tokens (NOT real auth — kept for tutorial-style demo dependencies).
    fake_header_token: str = "fake-super-secret-token"
    fake_query_token: str = "jessica"
    default_page_size: int = 20
    max_page_size: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()
