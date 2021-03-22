from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, PostgresDsn, RedisDsn


class SQLAlchemyPostgresDsn(PostgresDsn):
    def __init__(self, url, *args, **kwargs) -> None:
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://')

        if kwargs.get('scheme') == 'postgres':
            kwargs['scheme'] = 'postgresql'

        super().__init__(url, *args, **kwargs)


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(env='BOT_TOKEN')

    WEBHOOK_HOST: Optional[HttpUrl] = Field(env='WEBHOOK_HOST')
    WEBHOOK_PATH: str = '/tg'
    WEBAPP_HOST: str = '127.0.0.1'
    WEBAPP_PORT: int = 5000

    DATABASE_URL: SQLAlchemyPostgresDsn
    REDIS_URL: RedisDsn

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
