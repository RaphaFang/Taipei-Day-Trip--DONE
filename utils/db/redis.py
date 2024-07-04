import os
import redis
# import aioredis

def redis_pool_buildup():
    r_pool = redis.ConnectionPool(
        host='localhost',
        port=6379,
        db=0,
        password=os.getenv('REDIS_PASSWORD',None),
        max_connections=10 
    )
    return r_pool

# async def aioredis_pool_buildup():
#     pool = await aioredis.create_redis_pool(
#         'redis://localhost:6379',
#         password=os.getenv('REDIS_PASSWORD', None),
#         minsize=1,
#         maxsize=10
#     )
#     return pool