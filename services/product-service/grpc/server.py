import shared.grpc.product_pb2_grpc as pb2_grpc
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import async_session_maker
import shared.grpc.product_pb2 as pb2
from db.models.product import Product
from concurrent import futures
from sqlalchemy import select
import logging
import grpc

logger = logging.getLogger(__name__)

class ProductServiceServicer(pb2_grpc.ProductServiceServicer):
    async def GetProduct(self, request, context):
        try:
            async with async_session_maker() as session:
                result = await session.execute(select(Product).filter(Product.id == request.product_id))
                product = result.scalars().first()
                
                if product:
                    return pb2.ProductResponse(
                        id=str(product.id),
                        title=product.title,
                        base_price=float(product.base_price),
                        is_active=product.is_active
                    )
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Product not found')
                    return pb2.ProductResponse()
        except Exception as e:
            logger.error(f"Error in GetProduct gRPC: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal error')
            return pb2.ProductResponse()

async def serve(port: int):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting gRPC server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()
