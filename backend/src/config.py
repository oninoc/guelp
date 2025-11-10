from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import cached_property

def ofuscate(value: str) -> str:
    return value if len(value) < 4 else value[:2] + "*" * (len(value) - 4) + value[-2:]


class ConfigurationVariables(BaseSettings):
    environment: Annotated[str, Field(alias="ENVIRONMENT", default="local")]
    database_url: Annotated[str, Field(alias="POSTGRES_URL")]
    log_sql_queries: Annotated[bool, Field(alias="LOG_SQL_QUERIES", default=False)]
    secret_key: Annotated[str, Field(alias="SECRET_KEY", default="")]
    algorithm: Annotated[str, Field(alias="ALGORITHM", default="HS256")]
    aws_access_key_id: Annotated[str, Field(alias="AWS_ACCESS_KEY_ID", default="")]
    aws_secret_access_key: Annotated[str, Field(alias="AWS_SECRET_ACCESS_KEY", default="")]
    aws_region: Annotated[str, Field(alias="AWS_REGION", default="us-east-1")]
    aws_file_bucket_name: Annotated[str, Field(alias="AWS_FILE_BUCKET_NAME")]

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

    @cached_property
    def aws_credentials(self) -> dict:
        """Return AWS credentials if available"""
        if self.is_development:
            print("Using explicit AWS credentials for development")
            print(f"Region: {self.aws_region}")
            print(f"Access Key ID: {ofuscate(self.aws_access_key_id)}")
            print(f"Secret Access Key: {ofuscate(self.aws_secret_access_key)}")
            return {
                "aws_access_key_id": self.aws_access_key_id,
                "aws_secret_access_key": self.aws_secret_access_key,
                "region_name": self.aws_region,
            }
        print("Using IAM role for AWS credentials")
        print(f"Region: {self.aws_region}")
        return {
            "region_name": self.aws_region,
        }

configuration_variables = ConfigurationVariables()
