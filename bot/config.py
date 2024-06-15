from typing import List, Type, Tuple
import pydantic
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource,
)


class Prometheus(pydantic.BaseModel):
    enabled: bool = False
    url: str | None = None


class Database(pydantic.BaseModel):
    url: str | None = None


class Config(BaseSettings):
    api_server: str = pydantic.Field(default="https://kubernetes.default.svc")
    bot_token: str = pydantic.Field(...)
    guild_ids: List[int] | None = None

    prometheus: Prometheus = Prometheus()
    database: Database = Database()

    # secret settings can be left empty
    # in the yml file and provided as an environment variable
    # example: BOT_CONFIG_DATABASE_URL=postgres+asyncpg:///...
    model_config = SettingsConfigDict(
        env_prefix="BOT_CONFIG_",
        env_nested_delimiter="_",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            YamlConfigSettingsSource(settings_cls),
        )


config: Config = None


def load_config(yaml_file):
    global config
    Config.model_config["yaml_file"] = yaml_file
    config = Config()
