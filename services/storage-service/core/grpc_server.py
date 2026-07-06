from pb.storage.storage_pb2_grpc import add_StorageServiceServicer_to_server
from grpc_services.storage_service import StorageServicer
import grpc.aio


async def start_grpc_server() -> grpc.aio.Server:
    """
    Initializes and starts the asynchronous gRPC server.
    Returns the server instance so FastAPI's lifespan can manage it.
    """
    server = grpc.aio.server(
        options=[
            ("grpc.max_send_message_length", 100 * 1024 * 1024),
            ("grpc.max_receive_message_length", 100 * 1024 * 1024),
        ]
    )

    servicer = StorageServicer()
    add_StorageServiceServicer_to_server(servicer, server)

    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)

    await server.start()
    return server
