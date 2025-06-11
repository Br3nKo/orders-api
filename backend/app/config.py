from pydantic_settings import BaseSettings
from utils import get_url


class Settings(BaseSettings):
    database_url: str = get_url()
    echo_sql: bool = True
    test: bool = False
    project_name: str = "Orders API"
    oauth_token_secret: str = "my_dev_secret"
    log_level: str = "DEBUG"


settings = Settings()
