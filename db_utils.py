import os
import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='loan_app_db',
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
        return conn
    except Exception as e:
        print('Error Connecting to DB: ', e)