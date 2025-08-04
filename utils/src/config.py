from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    telegram_token: SecretStr

    postgres_user: SecretStr
    postgres_password: SecretStr
    postgres_db: SecretStr
    postgres_host: SecretStr
    postgres_port: int

    redis_host: SecretStr
    redis_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
