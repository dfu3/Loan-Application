from loan_service import process_loan_req

def test_deny_low_requested_amount():
    result = process_loan_req(9999, 5)
    assert result["status"] == "denied"
    assert result["requested_amount"] == 9999
    assert result["credit_lines"] == 5

def test_deny_high_requested_amount():
    result = process_loan_req(50001, 5)
    assert result["status"] == "denied"
    assert result["requested_amount"] == 50001
    assert result["credit_lines"] == 5

def test_deny_too_many_credit_lines():
    result = process_loan_req(20000, 51)
    assert result["status"] == "denied"
    assert result["requested_amount"] == 20000
    assert result["credit_lines"] == 51

def test_approve_low_credit_lines():
    requested = 20000
    credit_lines = 5
    result = process_loan_req(requested, credit_lines)
    assert result["status"] == "approved"
    assert result["term_months"] == 36
    assert result["interest_rate"] == 0.10
    assert result["monthly_payment"] == 645.34
    assert result["total_amount"] == result["monthly_payment"] * 36

def test_approve_medium_credit_lines():
    requested = 30000
    credit_lines = 25
    result = process_loan_req(requested, credit_lines)
    assert result["status"] == "approved"
    assert result["term_months"] == 24
    assert result["interest_rate"] == 0.20
    assert result["monthly_payment"] == 1526.87
    assert result["total_amount"] == result["monthly_payment"] * 24
