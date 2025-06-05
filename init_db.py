from db_utils import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS user_app;')
create_table_query = """
    CREATE TABLE IF NOT EXISTS user_app (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        ssn TEXT UNIQUE,
        requested_loan_amount NUMERIC(12, 2),
        offered_loan_amount NUMERIC(12, 2),
        status TEXT DEFAULT 'pending'
    );
    """
cur.close()
conn.close()