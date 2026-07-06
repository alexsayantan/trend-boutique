from pb.storage import storage_pb2, storage_pb2_grpc
from core.r2_service import (
    delete_objects_from_r2,
    list_objects_in_r2,
    upload_files_to_r2,
    generate_presigned_url,
)
from io import BytesIO
import asyncio
import grpc


class SimpleUploadFile:
    def __init__(self, data: bytes, filename: str, content_type: str):
        self.file = BytesIO(data)
        self.filename = filename
        self.content_type = content_type
        self.size = len(data)

    async def read(self, size: int = -1):
        return self.file.read(size)

    async def seek(self, offset: int):
        self.file.seek(offset)

    async def close(self):
        self.file.close()


class StorageServicer(storage_pb2_grpc.StorageServiceServicer):

    async def UploadFile(self, request, context):
        try:
            if not request.files:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("at least one file must be provided")
                return storage_pb2.UploadFileResponse()

            # Validate all items have keys before doing any work
            for item in request.files:
                if not item.key:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details("key must be provided for every file")
                    return storage_pb2.UploadFileResponse()

            async def upload_one(item) -> storage_pb2.FileUploadResult:
                try:
                    file = SimpleUploadFile(
                        data=item.file_data,
                        filename=item.filename,
                        content_type=item.content_type,
                    )
                    await upload_files_to_r2(
                        files_with_keys=[(file, item.key)],
                        public=item.public,
                    )
                    presigned_url = ""
                    if not item.public:
                        presigned_url = await generate_presigned_url(
                            item.key, expires_in=3600
                        )
                    return storage_pb2.FileUploadResult(
                        key=item.key,
                        presigned_url=presigned_url,
                    )
                except Exception as e:
                    return storage_pb2.FileUploadResult(key=item.key, error=str(e))

            results = await asyncio.gather(*[upload_one(item) for item in request.files])
            return storage_pb2.UploadFileResponse(results=results)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return storage_pb2.UploadFileResponse()

    async def GeneratePresignedUrl(self, request, context):
        try:
            if not request.items:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("at least one item must be provided")
                return storage_pb2.GeneratePresignedUrlResponse()

            for item in request.items:
                if not item.key:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details("key must be provided for every item")
                    return storage_pb2.GeneratePresignedUrlResponse()

            async def generate_one(item) -> storage_pb2.PresignedUrlResult:
                try:
                    expires_in = item.expires_in if item.expires_in > 0 else 3600
                    presigned_url = await generate_presigned_url(
                        item.key, expires_in=expires_in
                    )
                    return storage_pb2.PresignedUrlResult(
                        key=item.key,
                        presigned_url=presigned_url,
                    )
                except Exception as e:
                    return storage_pb2.PresignedUrlResult(key=item.key, error=str(e))

            results = await asyncio.gather(*[generate_one(item) for item in request.items])
            return storage_pb2.GeneratePresignedUrlResponse(results=results)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return storage_pb2.GeneratePresignedUrlResponse()

    async def UpdateFile(self, request, context):
        try:
            if not request.files:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("at least one file must be provided")
                return storage_pb2.UpdateFileResponse()

            for item in request.files:
                if not item.key:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details("key must be provided for every file")
                    return storage_pb2.UpdateFileResponse()

            async def update_one(item) -> storage_pb2.FileUpdateResult:
                try:
                    await delete_objects_from_r2(item.key)
                    file = SimpleUploadFile(
                        data=item.file_data,
                        filename=item.filename,
                        content_type=item.content_type,
                    )
                    await upload_files_to_r2(
                        files_with_keys=[(file, item.key)],
                        public=item.public,
                    )
                    presigned_url = ""
                    if not item.public:
                        presigned_url = await generate_presigned_url(
                            item.key, expires_in=3600
                        )
                    return storage_pb2.FileUpdateResult(
                        key=item.key,
                        presigned_url=presigned_url,
                    )
                except Exception as e:
                    return storage_pb2.FileUpdateResult(key=item.key, error=str(e))

            results = await asyncio.gather(*[update_one(item) for item in request.files])
            return storage_pb2.UpdateFileResponse(results=results)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return storage_pb2.UpdateFileResponse()

    async def DeleteFile(self, request, context):
        try:
            if not request.keys:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("at least one key must be provided")
                return storage_pb2.DeleteFileResponse()

            await delete_objects_from_r2(list(request.keys))
            return storage_pb2.DeleteFileResponse(deleted_keys=list(request.keys))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return storage_pb2.DeleteFileResponse()
    
    async def ListFiles(
        self,
        request: storage_pb2.ListFilesRequest,
        context: grpc.ServicerContext,
    ) -> storage_pb2.ListFilesResponse:
        try:
            prefix = request.prefix.strip()
            max_keys = request.max_keys if request.max_keys > 0 else 1000

            if not prefix:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("prefix cannot be empty")
                return storage_pb2.ListFilesResponse()

            # Use the existing helper from r2_service
            keys = await list_objects_in_r2(prefix=prefix)

            # Optional: limit the number of keys returned
            if len(keys) > max_keys:
                keys = keys[:max_keys]

            return storage_pb2.ListFilesResponse(keys=keys)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to list files: {str(e)}")
            return storage_pb2.ListFilesResponse()