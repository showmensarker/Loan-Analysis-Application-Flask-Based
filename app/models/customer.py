"""
Customer model used in the loan system.
Stores customer details and links
customers with their loans.
"""

from app import db


class Customer(db.Model):
    """
    Represents a customer within the lending platform.
    This model tracks demographic data and financial standing, 
    acting as the parent entity for all issued loans.
    """

    # Unique identifier for each customer record.
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Stores the age of the customer; kept as a string to allow 
    # for potential age range brackets or categories.
    age = db.Column(
        db.String(20)
    )

    # Total annual or monthly income used for credit assessment.
    income = db.Column(
        db.Float
    )

    # Demographic field to store customer gender.
    gender = db.Column(
        db.String(10)
    )

    # Establishes a one-to-many link to the Loan model.
    # backref="customer" allows us to access the customer directly 
    # from a loan object.
    loans = db.relationship(
        "Loan",
        backref="customer",
        lazy=True
    )