from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, PostgresDsn


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(env='BOT_TOKEN')
    WEBHOOK_HOST: Optional[HttpUrl] = Field(env='WEBHOOK_HOST')
    DB_URL: PostgresDsn

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
