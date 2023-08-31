from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    model_config = SettingsConfigDict(env_file='config\.env.txt', env_file_encoding='utf-8')


config = Settings()
