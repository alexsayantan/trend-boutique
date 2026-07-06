from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileUploadItem(_message.Message):
    __slots__ = ("file_data", "filename", "content_type", "key", "public")
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    file_data: bytes
    filename: str
    content_type: str
    key: str
    public: bool
    def __init__(self, file_data: _Optional[bytes] = ..., filename: _Optional[str] = ..., content_type: _Optional[str] = ..., key: _Optional[str] = ..., public: bool = ...) -> None: ...

class FileUploadResult(_message.Message):
    __slots__ = ("key", "presigned_url", "error")
    KEY_FIELD_NUMBER: _ClassVar[int]
    PRESIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    key: str
    presigned_url: str
    error: str
    def __init__(self, key: _Optional[str] = ..., presigned_url: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[FileUploadItem]
    def __init__(self, files: _Optional[_Iterable[_Union[FileUploadItem, _Mapping]]] = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[FileUploadResult]
    def __init__(self, results: _Optional[_Iterable[_Union[FileUploadResult, _Mapping]]] = ...) -> None: ...

class PresignedUrlItem(_message.Message):
    __slots__ = ("key", "expires_in")
    KEY_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    key: str
    expires_in: int
    def __init__(self, key: _Optional[str] = ..., expires_in: _Optional[int] = ...) -> None: ...

class PresignedUrlResult(_message.Message):
    __slots__ = ("key", "presigned_url", "error")
    KEY_FIELD_NUMBER: _ClassVar[int]
    PRESIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    key: str
    presigned_url: str
    error: str
    def __init__(self, key: _Optional[str] = ..., presigned_url: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class GeneratePresignedUrlRequest(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[PresignedUrlItem]
    def __init__(self, items: _Optional[_Iterable[_Union[PresignedUrlItem, _Mapping]]] = ...) -> None: ...

class GeneratePresignedUrlResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[PresignedUrlResult]
    def __init__(self, results: _Optional[_Iterable[_Union[PresignedUrlResult, _Mapping]]] = ...) -> None: ...

class FileUpdateItem(_message.Message):
    __slots__ = ("file_data", "filename", "content_type", "key", "public")
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    file_data: bytes
    filename: str
    content_type: str
    key: str
    public: bool
    def __init__(self, file_data: _Optional[bytes] = ..., filename: _Optional[str] = ..., content_type: _Optional[str] = ..., key: _Optional[str] = ..., public: bool = ...) -> None: ...

class FileUpdateResult(_message.Message):
    __slots__ = ("key", "presigned_url", "error")
    KEY_FIELD_NUMBER: _ClassVar[int]
    PRESIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    key: str
    presigned_url: str
    error: str
    def __init__(self, key: _Optional[str] = ..., presigned_url: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class UpdateFileRequest(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[FileUpdateItem]
    def __init__(self, files: _Optional[_Iterable[_Union[FileUpdateItem, _Mapping]]] = ...) -> None: ...

class UpdateFileResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[FileUpdateResult]
    def __init__(self, results: _Optional[_Iterable[_Union[FileUpdateResult, _Mapping]]] = ...) -> None: ...

class DeleteFileRequest(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteFileResponse(_message.Message):
    __slots__ = ("deleted_keys",)
    DELETED_KEYS_FIELD_NUMBER: _ClassVar[int]
    deleted_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, deleted_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class ListFilesRequest(_message.Message):
    __slots__ = ("prefix", "max_keys")
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    MAX_KEYS_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    max_keys: int
    def __init__(self, prefix: _Optional[str] = ..., max_keys: _Optional[int] = ...) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ...) -> None: ...
