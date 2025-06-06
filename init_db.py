from db_utils import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS user_app;')
create_table_query = """
    CREATE TABLE IF NOT EXISTS user_app (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        ssn TEXT NOT NULL,
        credit_lines SMALLINT NOT NULL,
        requested_loan_amount NUMERIC(12, 2) NOT NULL,
        term_months SMALLINT,
        interest_rate NUMERIC(5,4),
        total_loan_amount NUMERIC(12, 2),
        monthly_payment NUMERIC(12, 2),
        status TEXT DEFAULT 'pending'
    );
    """
cur.execute(create_table_query)
conn.commit()
print('create table query executed')
cur.close()
conn.close()