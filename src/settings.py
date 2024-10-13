from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str
    jwt_access_token_expires: int
    jwt_refresh_token_expires: int
    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    db_url: PostgresDsn | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.db_url:
            self.db_url = PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.db_user,
                password=self.db_password.get_secret_value(),
                host=self.db_host,
                port=self.db_port,
                path=self.db_name,
            )


settings = Settings()

