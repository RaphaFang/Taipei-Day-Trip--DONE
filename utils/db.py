import os
import mysql.connector.pooling

def pool_buildup():
    pool_config = {
        'pool_name': 'day_trip_pool',
        'pool_size': 10,
        'host': '52.4.229.207',
        'user': os.getenv('SQL_USER'),
        'password': os.getenv('SQL_PASSWORD'),
        # 'host': 'localhost',
        # 'user': os.getenv('SQL_USER_LOCAL'),
        # 'password': os.getenv('SQL_PASSWORD_LOCAL'),
        'database': 'basic_db',
        'port': 3306,
        'use_pure': True
    }
    return mysql.connector.pooling.MySQLConnectionPool(**pool_config)