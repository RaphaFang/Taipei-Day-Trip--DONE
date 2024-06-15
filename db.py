import os
import mysql.connector.pooling

sql_password = os.getenv('SQL_PASSWORD')
sql_username = os.getenv('SQL_USER')

pool_config = {
    'pool_name': 'day_trip_pool',
    'pool_size': 10,
    'host': '52.4.229.207',
    'user': sql_username,
    'password': sql_password,
    'database': 'basic_db',
    'port':3306,
    'use_pure': True

}
mydb_pool = mysql.connector.pooling.MySQLConnectionPool(**pool_config)

def get_connection():
    connection = mydb_pool.get_connection()
    connection.ssl_disabled = True  # Disable SSL
    return connection
