from pb.storage import storage_pb2, storage_pb2_grpc
from core.config import get_settings
import grpc, uuid

settings = get_settings()


class StorageClient:
    _channel: grpc.aio.Channel | None = None
    _stub = None

    @classmethod
    def init(cls):
        cls._channel = grpc.aio.insecure_channel(settings.STORAGE_SERVICE_GRPC_HOST)
        cls._stub = storage_pb2_grpc.StorageServiceStub(cls._channel)

    @classmethod
    async def close(cls):
        if cls._channel:
            await cls._channel.close()
            cls._channel = None
            cls._stub = None

    @classmethod
    def get_stub(cls):
        if cls._stub is None:
            raise RuntimeError(
                "StorageClient not initialized. Call StorageClient.init() at startup."
            )
        return cls._stub

    @classmethod
    async def upload_file(
        cls,
        file_data: bytes,
        filename: str,
        content_type: str,
        key: str,
        public: bool = False,
    ) -> tuple[str, str]:
        """Upload a single file. Returns (key, presigned_url)."""
        stub = cls.get_stub()
        response = await stub.UploadFile(
            storage_pb2.UploadFileRequest(
                files=[
                    storage_pb2.FileUploadItem(
                        file_data=file_data,
                        filename=filename,
                        content_type=content_type,
                        key=key,
                        public=public,
                    )
                ]
            )
        )
        result = response.results[0]
        if result.error:
            raise Exception(f"Upload failed for key '{key}': {result.error}")
        return result.key, result.presigned_url

    @classmethod
    async def upload_files(
        cls,
        files: list[dict],
    ) -> list[tuple[str, str]]:
        """
        Bulk upload files.
        Each dict: { file_data, filename, content_type, key, public }
        Returns list of (key, presigned_url).
        """
        stub = cls.get_stub()
        response = await stub.UploadFile(
            storage_pb2.UploadFileRequest(
                files=[
                    storage_pb2.FileUploadItem(
                        file_data=f["file_data"],
                        filename=f["filename"],
                        content_type=f["content_type"],
                        key=f["key"],
                        public=f.get("public", False),
                    )
                    for f in files
                ]
            )
        )
        results = []
        for result in response.results:
            if result.error:
                raise Exception(f"Upload failed for key '{result.key}': {result.error}")
            results.append((result.key, result.presigned_url))
        return results

    @classmethod
    async def generate_presigned_url(
        cls,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        """Generate a presigned URL for a single key."""
        stub = cls.get_stub()
        response = await stub.GeneratePresignedUrl(
            storage_pb2.GeneratePresignedUrlRequest(
                items=[
                    storage_pb2.PresignedUrlItem(
                        key=key,
                        expires_in=expires_in,
                    )
                ]
            )
        )
        result = response.results[0]
        if result.error:
            raise Exception(
                f"Failed to generate presigned URL for key '{key}': {result.error}"
            )
        return result.presigned_url

    @classmethod
    async def generate_presigned_urls(
        cls,
        items: list[dict],
    ) -> list[str]:
        """
        Bulk generate presigned URLs.
        Each dict: { key, expires_in (optional) }
        Returns list of presigned URLs in the same order.
        """
        stub = cls.get_stub()
        response = await stub.GeneratePresignedUrl(
            storage_pb2.GeneratePresignedUrlRequest(
                items=[
                    storage_pb2.PresignedUrlItem(
                        key=item["key"],
                        expires_in=item.get("expires_in", 3600),
                    )
                    for item in items
                ]
            )
        )
        urls = []
        for result in response.results:
            if result.error:
                raise Exception(
                    f"Failed to generate presigned URL for key '{result.key}': {result.error}"
                )
            urls.append(result.presigned_url)
        return urls

    @classmethod
    async def update_file(
        cls,
        file_data: bytes,
        filename: str,
        content_type: str,
        key: str,
        public: bool = False,
    ) -> tuple[str, str]:
        """Update a single file. Returns (key, presigned_url)."""
        stub = cls.get_stub()
        response = await stub.UpdateFile(
            storage_pb2.UpdateFileRequest(
                files=[
                    storage_pb2.FileUpdateItem(
                        file_data=file_data,
                        filename=filename,
                        content_type=content_type,
                        key=key,
                        public=public,
                    )
                ]
            )
        )
        result = response.results[0]
        if result.error:
            raise Exception(f"Update failed for key '{key}': {result.error}")
        return result.key, result.presigned_url

    @classmethod
    async def update_files(
        cls,
        files: list[dict],
    ) -> list[tuple[str, str]]:
        """
        Bulk update files.
        Each dict: { file_data, filename, content_type, key, public }
        Returns list of (key, presigned_url).
        """
        stub = cls.get_stub()
        response = await stub.UpdateFile(
            storage_pb2.UpdateFileRequest(
                files=[
                    storage_pb2.FileUpdateItem(
                        file_data=f["file_data"],
                        filename=f["filename"],
                        content_type=f["content_type"],
                        key=f["key"],
                        public=f.get("public", False),
                    )
                    for f in files
                ]
            )
        )
        results = []
        for result in response.results:
            if result.error:
                raise Exception(f"Update failed for key '{result.key}': {result.error}")
            results.append((result.key, result.presigned_url))
        return results

    @classmethod
    async def delete_file(
        cls,
        key: str,
    ) -> list[str]:
        """Delete a single file. Returns list of deleted keys."""
        return await cls.delete_files([key])

    @classmethod
    async def delete_files(
        cls,
        keys: list[str],
    ) -> list[str]:
        """Bulk delete files. Returns list of deleted keys."""
        stub = cls.get_stub()
        response = await stub.DeleteFile(storage_pb2.DeleteFileRequest(keys=keys))
        return list(response.deleted_keys)


class UserStorageClient(StorageClient):

    @classmethod
    async def update_profile_image(
        cls,
        file_data: bytes,
        filename: str,
        content_type: str,
        user_id: str,
        existing_key: str | None = None,
    ) -> tuple[str, str]:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"

        if existing_key:
            return await cls.update_file(
                file_data=file_data,
                filename=filename,
                content_type=content_type,
                key=existing_key,
                public=False,
            )

        key = f"users/{user_id}/profile-images/{uuid.uuid4()}.{ext}"
        return await cls.upload_file(
            file_data=file_data,
            filename=filename,
            content_type=content_type,
            key=key,
            public=False,
        )

    @classmethod
    async def delete_profile_image(
        cls,
        existing_key: str,
    ) -> None:
        await cls.delete_file(key=existing_key)
