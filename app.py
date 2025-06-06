from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
import re
from loan_service import get_num_credit_lines, process_loan_req
from db_utils import save_user_app

app = Flask(__name__)
app.secret_key = secrets.token_hex(32) # in place of key from prod env

@app.route('/apply')
def apply():
    return render_template('loan_app.html')

@app.route('/submit', methods=['POST'])
def submit():

    errors = validate_form_data(request.form)
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('apply'))

    credit_lines = get_num_credit_lines()
    amount = float(request.form.get('requested_amount'))
    loan_result = process_loan_req(amount, credit_lines)

    save_user_app(request.form.to_dict(), loan_result)

    session['name'] = request.form.get('name')
    session['loan_result'] = loan_result
    session['from_submit'] = True

    return redirect(url_for('offer'))

@app.route('/offer')
def offer():
    if not session.get('from_submit'):
        return redirect(url_for('apply'))
    
    loan_result = session.get('loan_result')
    name = session.get('name')
    status = loan_result.get('status')

    if status == 'denied':
        return render_template(
            'loan_denied.html',
            name=name,
            requested_amount=loan_result.get('requested_amount')
        )

    return render_template(
        'loan_offer.html',
        name=name,
        loan_amount=loan_result.get('total_amount'),
        interest_rate=loan_result.get('interest_rate'),
        term=loan_result.get('term_months'),
        monthly_payment=loan_result.get('monthly_payment')
    )


def validate_form_data(form):
    errors = []

    name = form.get('name', '').strip()
    if not name:
        errors.append("Name is required.")

    address = form.get('address', '').strip()
    if not address:
        errors.append("Address is required.")

    email = form.get('email', '').strip()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Valid email is required.")

    phone = form.get('phone', '').strip()
    if not re.fullmatch(r"\d{10}", phone):
        errors.append("Phone number must be 10 digits.")

    ssn = form.get('ssn', '').strip()
    if not re.fullmatch(r"\d{3}-\d{2}-\d{4}", ssn):
        errors.append("SSN must be in the format XXX-XX-XXXX.")

    try:
        print(form.get('requested_amount'))
        amount = float(form.get('requested_amount', 0))
        if amount <= 0:
            errors.append("Requested loan amount must be greater than zero.")
    except ValueError:
        errors.append("Requested loan amount must be a valid number.")

    return errors
