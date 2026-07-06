from typing import List, Tuple, Protocol, Any, runtime_checkable
from botocore.exceptions import ClientError
from core.config import settings
from botocore.config import Config
import asyncio
import boto3


R2_PUBLIC_BASE_URL = (
    settings.CLOUDFLARE_R2_PUBLIC_URL
    or f"https://{settings.CLOUDFLARE_BUCKET_NAME}.{settings.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com"
)

R2_ENDPOINT_URL = f"https://{settings.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com"


@runtime_checkable
class UploadFileLike(Protocol):
    file: Any
    content_type: str
    async def seek(self, offset: int) -> None: ...


_s3_client = None


def get_r2_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
        )
    return _s3_client


async def upload_files_to_r2(
    files_with_keys: List[Tuple[UploadFileLike, str]], public: bool = True
) -> List[str]:
    """
    Upload files to R2 without framework dependencies.
    """
    client = get_r2_client()

    async def upload_one(file_obj: UploadFileLike, key: str):
        try:
            # Handle both async and sync seek for maximum compatibility
            if asyncio.iscoroutinefunction(file_obj.seek):
                await file_obj.seek(0)
            else:
                file_obj.seek(0)

            extra_args = {}
            if public:
                extra_args["ACL"] = "public-read"

            if hasattr(file_obj, 'content_type') and file_obj.content_type:
                extra_args["ContentType"] = file_obj.content_type

            # Pass the underlying file-like object (BytesIO or SpooledTempFile)
            await asyncio.to_thread(
                client.upload_fileobj,
                file_obj.file,
                settings.CLOUDFLARE_BUCKET_NAME,
                key,
                ExtraArgs=extra_args,
            )

            return f"{R2_PUBLIC_BASE_URL}/{key}" if public else key

        except ClientError as e:
            raise Exception(f"Failed to upload {key}: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error uploading {key}: {str(e)}")

    results = await asyncio.gather(
        *[upload_one(file_obj, key) for file_obj, key in files_with_keys],
        return_exceptions=True,
    )

    final_urls = []
    for result in results:
        if isinstance(result, Exception):
            raise result
        final_urls.append(result)

    return final_urls


async def delete_objects_from_r2(keys: List[str] | str):
    """
    Delete objects from R2.
    :param keys: Single key string or list of keys.
    """
    if isinstance(keys, str):
        keys = [keys]

    if not keys:
        return

    client = get_r2_client()
    try:
        # R2/S3 delete_objects can handle up to 1000 keys at once
        await asyncio.to_thread(
            client.delete_objects,
            Bucket=settings.CLOUDFLARE_BUCKET_NAME,
            Delete={"Objects": [{"Key": key} for key in keys]},
        )
    except ClientError as e:
        raise Exception(f"Failed to delete objects: {str(e)}")


async def list_objects_in_r2(prefix: str = "") -> List[str]:
    """
    List objects in R2 with a given prefix.
    :return: List of object keys.
    """
    client = get_r2_client()
    try:
        response = await asyncio.to_thread(
            client.list_objects_v2,
            Bucket=settings.CLOUDFLARE_BUCKET_NAME,
            Prefix=prefix,
        )
        contents = response.get("Contents", [])
        return [obj["Key"] for obj in contents]
    except ClientError as e:
        raise Exception(f"Failed to list objects: {str(e)}")


async def generate_presigned_url(
    key: str, expires_in: int = 3600, method: str = "get_object"
) -> str:
    """
    Generate a presigned URL for an object.
    :param key: Object key
    :param expires_in: Expiration time in seconds
    :param method: 'get_object' or 'put_object'
    :return: Presigned URL string
    """
    client = get_r2_client()
    try:
        url = await asyncio.to_thread(
            client.generate_presigned_url,
            method,
            Params={"Bucket": settings.CLOUDFLARE_BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in,
        )
        return url
    except ClientError as e:
        raise Exception(f"Failed to generate presigned URL for {key}: {str(e)}")


async def generate_presigned_urls(
    keys: List[str] | str, expires_in: int = 3600, method: str = "get_object"
) -> List[str]:
    """
    Generate presigned URLs for multiple objects concurrently.
    """
    if isinstance(keys, str):
        keys = [keys]

    if not keys:
        return []

    urls = await asyncio.gather(
        *[generate_presigned_url(key, expires_in, method) for key in keys]
    )
    return urls

