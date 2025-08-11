from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings

class ConfigurationVariables(BaseSettings):
    environment: Annotated[str, Field(alias="ENVIRONMENT", default="local")]
    database_url: Annotated[str, Field(alias="POSTGRES_URL")]
    log_sql_queries: Annotated[bool, Field(alias="LOG_SQL_QUERIES", default=False)]
    secret_key: Annotated[str, Field(alias="SECRET_KEY", default="")]
    algorithm: Annotated[str, Field(alias="ALGORITHM", default="HS256")]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "prod"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() in ["dev", "development", "local"]

    @property
    def get_database_url(self) -> str:
        return self.database_url.replace("%", "%%")

configuration_variables = ConfigurationVariables()
