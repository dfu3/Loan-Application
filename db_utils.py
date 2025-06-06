import os
from psycopg2 import connect, sql
from flask import abort

def get_db_connection():
    try:
        conn = connect(
            host='localhost',
            database='loan_app_db',
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
        print('DB connection succesfull')
        return conn
    except Exception as e:
        print('Error Connecting to DB: ', e)


insert_query_approved = sql.SQL("""
    INSERT INTO user_app (
        name, address, email, phone, ssn, credit_lines,
        requested_loan_amount, term_months, interest_rate,
        total_loan_amount, monthly_payment, status
    ) VALUES (
        %(name)s, %(address)s, %(email)s, %(phone)s, %(ssn)s, %(credit_lines)s,
        %(requested_loan_amount)s, %(term_months)s, %(interest_rate)s,
        %(total_loan_amount)s, %(monthly_payment)s, %(status)s
    )
""")

insert_query_denied= sql.SQL("""
    INSERT INTO user_app (
        name, address, email, phone, ssn, credit_lines,
        requested_loan_amount, status
    ) VALUES (
        %(name)s, %(address)s, %(email)s, %(phone)s, %(ssn)s, %(credit_lines)s,
        %(requested_loan_amount)s, %(status)s
    )
""")

def save_user_app(user_fields, loan_fields):
    data = {
        "name": user_fields["name"],
        "address": user_fields["address"],
        "email": user_fields["email"],
        "phone": user_fields["phone"],
        "ssn": user_fields["ssn"],
        "credit_lines": int(loan_fields["credit_lines"]),
        "requested_loan_amount": float(loan_fields["requested_amount"]),
    }

    query = insert_query_denied
    data['status'] = 'denied'
    if loan_fields['status'] == 'approved':
        data['status'] = 'approved'
        data['total_loan_amount'] = float(loan_fields['total_amount'])
        data['interest_rate'] = float(loan_fields['interest_rate'])
        data['term_months'] = int(loan_fields['term_months'])
        data['monthly_payment'] = float(loan_fields['monthly_payment'])
        query = insert_query_approved

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, data)
        conn.commit()
    except Exception as e:
        msg = 'Error saving loan application '
        print(msg, e)
        abort(500, msg)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

