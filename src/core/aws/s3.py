from functools import partial

from aioaws.s3 import S3Client, S3Config
from httpx import AsyncClient


http_client = AsyncClient(verify=False)
AWSClient = partial(
    S3Client,
    http_client=http_client,
    config=S3Config(),
)
s3_client = AWSClient()
# TODO: install aioaws and add settings
