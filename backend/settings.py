from pydantic import BaseSettings, Field

from urllib.parse import quote_plus


class MongoSettings(BaseSettings):
    username: str = Field(..., env="MONGO_USERNAME")
    password: str = Field(..., env="MONGO_PASSWORD")
    host: str = Field("localhost", env="MONGO_HOST")
    port: int = Field(..., env="MONGO_PORT")

    @property
    def connection_url(self) -> str:
        credentials = f"{quote_plus(self.username)}:{quote_plus(self.password)}"
        address = f"{self.host}:{self.port}"
        return f"mongodb://{credentials}@{address}"


class Settings:
    mongo = MongoSettings()
