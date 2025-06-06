
# middleware to process and save loan data
import random

def get_num_credit_lines():
    return random.randint(0, 100)

def process_loan_req(requested_amount, credit_lines):

    # Deny based on requested loan amount
    if requested_amount < 10000 or requested_amount > 50000:
        return {
            "status": "denied",
            "credit_lines": credit_lines,
            "requested_amount": requested_amount,
        }

    # Determine term and interest based on number of open credit lines
    if credit_lines < 10:
        term_months = 36
        annual_interest_rate = 0.10
    elif 10 <= credit_lines <= 50:
        term_months = 24
        annual_interest_rate = 0.20
    else:
        return {
            "status": "denied",
            "credit_lines": credit_lines,
            "requested_amount": requested_amount,
        }
    
    monthly_payment = calculate_monthly_payment(requested_amount, annual_interest_rate, term_months)
    total_loan_amount = monthly_payment * term_months
    # Return the computed offer
    return {
        "status": "approved",
        "credit_lines": credit_lines,
        "requested_amount": requested_amount,
        "total_amount": total_loan_amount,
        "interest_rate": annual_interest_rate,
        "term_months": term_months,
        "monthly_payment": monthly_payment
    }


def calculate_monthly_payment(amount, annual_interest_rate, term_months):

    monthly_rate = annual_interest_rate / 12

    rate_power = (1 + monthly_rate) ** -term_months

    denominator = 1 - rate_power
    numerator = amount * monthly_rate
    monthly_payment = numerator / denominator

    return round(monthly_payment, 2)