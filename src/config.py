from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


settings = Settings()
