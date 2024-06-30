import os
import redis

def redis_pool_buildup():
    r_pool = redis.ConnectionPool(
        # host='localhost',
        host='52.4.229.207',
        port=6379,
        db=0,
        password=os.getenv('REDIS_PASSWORD',None),
        max_connections=10 
    )
    return r_pool