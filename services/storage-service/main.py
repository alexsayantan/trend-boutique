from core.grpc_server import start_grpc_server
import asyncio
import logging


grpc_server = None
grpc_task: asyncio.Task | None = None


async def main():
    global grpc_server, grpc_task

    logging.basicConfig(level=logging.INFO)
    logging.info("Starting storage-service gRPC server on port 50051")

    try:
        grpc_server = await start_grpc_server()
        grpc_task = asyncio.create_task(grpc_server.wait_for_termination())
        logging.info("Storage gRPC server running on port 50051")
        await grpc_task  # blocks here keeping the process alive
    except Exception as e:
        logging.error(f"Failed to start storage gRPC server: {e}", exc_info=True)
        raise
    finally:
        if grpc_server:
            logging.info("Shutting down storage gRPC server...")
            await grpc_server.stop(grace=5.0)
            if grpc_task and not grpc_task.done():
                try:
                    await asyncio.wait_for(grpc_task, timeout=7.0)
                except asyncio.TimeoutError:
                    logging.warning("gRPC shutdown timed out, cancelling task")
                    grpc_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
