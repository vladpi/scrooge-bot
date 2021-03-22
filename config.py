from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(env='BOT_TOKEN')
    WEBHOOK_HOST: Optional[HttpUrl] = Field(env='WEBHOOK_HOST')
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
