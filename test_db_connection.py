from db import get_connection

try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print(f"Connected to database: {result}")
    cursor.close()
    connection.close()
except Exception as e:
    print(f"Error: {e}")
