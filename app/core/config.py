from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QR Kot'
    description: str = 'Приложение для Благотворительного фонда поддержки котиков'
    database_url: str
    secret: str = 'SECRET_WORD'

    class Config:
        env_file = '.env'

settings = Settings()
