import os
import mysql.connector.pooling

def pool_buildup():
    pool_config = {
        'pool_name': 'day_trip_pool',
        'pool_size': 10,
        # 'host': '52.4.229.207',
        'host': 'localhost',
        # 'user': os.getenv('SQL_USER'),
        'user': os.getenv('SQL_USER_LOCAL'),
        # 'password': os.getenv('SQL_PASSWORD'),
        'password': os.getenv('SQL_PASSWORD_LOCAL'),
        'database': 'basic_db',
        'port': 3306,
        'use_pure': True
    }
    return mysql.connector.pooling.MySQLConnectionPool(**pool_config)

# nano ~/.zshrc
# source ~/.zshrc