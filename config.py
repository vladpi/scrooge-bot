from typing import Optional, Dict

from pydantic import BaseSettings, Field, HttpUrl, PostgresDsn, RedisDsn


class SQLAlchemyPostgresDsn(PostgresDsn):
    @classmethod
    def validate_parts(cls, parts: Dict[str, str]) -> Dict[str, str]:
        if parts['scheme'] == 'postgres':
            parts['scheme'] = 'postgresql'
        return super().validate_parts(parts)


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
