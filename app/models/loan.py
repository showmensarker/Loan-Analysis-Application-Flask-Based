"""
Loan model for storing
loan-related information.
"""

from app import db


class Loan(db.Model):
    """
    Represents an individual loan agreement.
    This model tracks the financial specifics of the loan, the 
    risk profile of the borrower, and the eventual outcome.
    """

    # Unique identifier for each specific loan record.
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # The total principal amount granted to the borrower.
    loan_amount = db.Column(
        db.Float
    )

    # The borrower's credit rating at the time of the loan application.
    credit_score = db.Column(
        db.Integer
    )

    # Indicator for repayment success (e.g., 0 for paid, 1 for defaulted).
    default_status = db.Column(
        db.Integer
    )

    # Links this loan back to a specific person in the Customer table.
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.id")
    )