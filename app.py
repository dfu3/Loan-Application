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

    status = loan_result['status']
    session['status'] = status
    session['name'] = request.form.get('name')
    session['requested_amount'] = request.form.get('requested_amount')

    if status == 'approved':
        session['total_amount'] = loan_result['total_amount']
        session['interest_rate'] = loan_result['interest_rate']
        session['term_months'] = loan_result['term_months']
        session['monthly_payment'] = loan_result['monthly_payment']
    

    session['from_submit'] = True
    return redirect(url_for('offer'))

@app.route('/offer')
def offer():
    if not session.get('from_submit'):
        return redirect(url_for('apply'))
    
    name = session.get('name')
    status = session.get('status')
    requested = session.get('requested_amount')
    if status == 'denied':
        return render_template(
            'loan_denied.html',
            name=name,
            requested_amount=requested
        )
    amount = session.get('total_amount')
    interest = session.get('interest_rate')
    term = session.get('term_months')
    payment = session.get('monthly_payment')

    return render_template(
        'loan_offer.html',
        name=name,
        loan_amount=amount,
        interest_rate=interest,
        term=term,
        monthly_payment=payment
    )


def validate_form_data(form):
    errors = []

    # Name: must not be empty
    name = form.get('name', '').strip()
    if not name:
        errors.append("Name is required.")

    # Address: must not be empty
    address = form.get('address', '').strip()
    if not address:
        errors.append("Address is required.")

    # Email: basic format check
    email = form.get('email', '').strip()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Valid email is required.")

    # Phone: digits only, length check
    phone = form.get('phone', '').strip()
    if not re.fullmatch(r"\d{10}", phone):
        errors.append("Phone number must be 10 digits.")

    # SSN: format XXX-XX-XXXX
    ssn = form.get('ssn', '').strip()
    if not re.fullmatch(r"\d{3}-\d{2}-\d{4}", ssn):
        errors.append("SSN must be in the format XXX-XX-XXXX.")

    # Requested Loan Amount: must be a number > 0
    try:
        print(form.get('requested_amount'))
        amount = float(form.get('requested_amount', 0))
        if amount <= 0:
            errors.append("Requested loan amount must be greater than zero.")
    except ValueError:
        errors.append("Requested loan amount must be a valid number.")

    return errors
