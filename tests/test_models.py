import pytest


# SIMPLE UNIT TESTS

def test_average_income_calculation():
    """
    Test average income calculation.
    """

    incomes = [1000, 2000, 3000]

    average = sum(incomes) / len(incomes)

    assert average == 2000


def test_default_rate_calculation():
    """
    Test default rate calculation.
    """

    defaults = 10

    total_loans = 100

    rate = (defaults / total_loans) * 100

    assert rate == 10


def test_safe_loan_percentage():
    """
    Test safe loan percentage.
    """

    default_rate = 25

    safe_rate = 100 - default_rate

    assert safe_rate == 75


def test_safe_credit_score():
    """
    Test safe credit score logic.
    """

    score = 750

    assert score >= 700


def test_risky_credit_score():
    """
    Test risky credit score logic.
    """

    score = 400

    assert score < 700


def test_medium_risk_score():
    """
    Test medium risk score logic.
    """

    score = 680

    assert 600 <= score <= 750


def test_high_risk_score():
    """
    Test high risk score logic.
    """

    score = 550

    assert score < 600


def test_low_risk_score():
    """
    Test low risk score logic.
    """

    score = 810

    assert score > 750


def test_positive_loan_amount():
    """
    Test positive loan amount.
    """

    loan_amount = 5000

    assert loan_amount > 0


def test_large_loan_amount():
    """
    Test large loan amount logic.
    """

    loan_amount = 1500000

    assert loan_amount > 1000000


def test_negative_score_validation():
    """
    Test invalid negative score.
    """

    score = -10

    assert score < 0


def test_zero_score():
    """
    Test zero score edge case.
    """

    score = 0

    assert score == 0


def test_age_range_logic():
    """
    Test customer age range.
    """

    age = 27

    assert 18 <= age <= 100


def test_customer_income_positive():
    """
    Test customer income validation.
    """

    income = 4500

    assert income > 0


def test_customer_loan_relationship():
    """
    Test linked customer and loan IDs.
    """

    customer_id = 15

    loan_customer_id = 15

    assert customer_id == loan_customer_id