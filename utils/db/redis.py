import os
import redis
import redis.asyncio as aioredis 

async def build_async_redis_pool():
    r_pool = aioredis.ConnectionPool.from_url(
        'redis://localhost:6379/0',
        password=os.getenv('REDIS_PASSWORD', None),
        max_connections=10
    )
    return r_pool

def redis_pool_buildup():
    r_pool = redis.ConnectionPool(
        host='localhost',
        port=6379,
        db=0,
        password=os.getenv('REDIS_PASSWORD',None),
        max_connections=10 
    )
    return r_pool

