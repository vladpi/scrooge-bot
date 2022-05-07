from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, PostgresDsn, RedisDsn, SecretStr


class SQLAlchemyPostgresDsn(PostgresDsn):
    def __new__(cls, url: Optional[str], **kwargs) -> 'SQLAlchemyPostgresDsn':
        if url and url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://')

        if kwargs.get('scheme') == 'postgres':
            kwargs['scheme'] = 'postgresql'

        return super().__new__(cls, url, **kwargs)


class Settings(BaseSettings):
    TG_BOT_TOKEN: SecretStr

    WEBHOOK_HOST: Optional[HttpUrl]

    DATABASE_URL: SQLAlchemyPostgresDsn
    REDIS_URL: RedisDsn

    LOG_LEVEL: str = Field(default='INFO')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
