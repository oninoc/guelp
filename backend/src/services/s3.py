import boto3

from io import BytesIO, StringIO
from botocore.exceptions import ClientError
from typing import Optional
from ..schemas.s3 import S3DownloadFile, S3GeneratePresignedUrl
from ..logger import logger
from ..config import configuration_variables

bucket_name = configuration_variables.aws_file_bucket_name

class S3Service:
    def __init__(self) -> None:
        """
        Initialize S3Service with AWS credentials from environment variables
        """
        self.s3_client = boto3.client("s3", **configuration_variables.aws_credentials)

    def download_file(self, payload: S3DownloadFile) -> Optional[str]:
        """
        Generate a presigned URL for downloading a file from S3

        Args:
            bucket_name (str): Name of the S3 bucket
            object_key (str): Name of the file to download
            expiration (int): Time in seconds for the presigned URL to remain valid

        Returns:
            Optional[str]: Presigned URL for downloading, or None if generation failed
        """
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket_name,
                    "Key": f"{payload.object_key}"
                },
                ExpiresIn=payload.expiration,
            )

            logger.info(
                f"Generated presigned URL for downloading {payload.object_key} from {bucket_name}"
            )
            logger.info(f"URL will expire in {payload.expiration} seconds")
            return presigned_url

        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

    def generate_presigned_url(self, payload: S3GeneratePresignedUrl) -> Optional[str]:
        """
        Generate a presigned URL for uploading a file to S3 using MD5 hash of content

        Args:
            bucket_name (str): Name of the S3 bucket
            object_key (str): Name of the file to upload
            expiration (int): Time in seconds for the presigned URL to remain valid

        Returns:
            Optional[str]: Presigned URL for uploading, or None if generation failed
        """
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": payload.bucket_name,
                    "Key": payload.object_key,
                    "ContentType": "application/pdf",
                },
                ExpiresIn=payload.expiration,
            )

            logger.info(
                f"Generated presigned URL for uploading to {payload.bucket_name}/{payload.object_key}"
            )
            logger.info(f"URL will expire in {payload.expiration} seconds")
            return presigned_url

        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

    def download_file_by_key(self, bucket_name: str, object_key: str) -> BytesIO:
        """
        Download a file from S3 and return its content as a BytesIO object.

        Args:
            bucket_name (str): Name of the S3 bucket.
            object_key (str): Key of the object to download.

        Returns:
            BytesIO: Content of the downloaded file.
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            return BytesIO(response["Body"].read())
        except Exception as e:
            logger.error("Failed to download file from S3")
            logger.error(f"Bucket: {bucket_name}, Key: {object_key}")
            raise RuntimeError(f"Failed to download file from S3: {e}") from e

    def upload_file(
        self, bucket_name: str, object_key: str, file_content: StringIO
    ) -> None:
        """
        Upload a file to S3.

        Args:
            bucket_name (str): Name of the S3 bucket.
            object_key (str): Key for the object to upload.
            file_content (BytesIO): Content of the file to upload.

        Returns:
            None
        """
        try:
            byte_stream = BytesIO(file_content.read().encode("utf-8"))
            self.s3_client.upload_fileobj(
                Bucket=bucket_name, Key=object_key, Fileobj=byte_stream
            )
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to S3: {e}") from e

    def delete_file(self, bucket_name: str, object_key: str) -> None:
        """
        Delete a file from S3.

        Args:
            bucket_name (str): Name of the S3 bucket.
            object_key (str): Key of the object to delete.

        Returns:
            None
        """
        self.s3_client.delete_object(Bucket=bucket_name, Key=object_key)
