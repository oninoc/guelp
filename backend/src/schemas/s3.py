from typing import Optional
from .shared.BaseModel import BaseModel


class S3Base(BaseModel):
    object_key: str


class S3DownloadFile(S3Base):
    expiration: Optional[int] = 3600


class S3GeneratePresignedUrl(S3Base):
    expiration: Optional[int] = 3600


class S3UrlSigned(BaseModel):
    url: str
    expiration: Optional[int] = 3600
