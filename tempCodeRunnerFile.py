"""
Script used to load CSV data
into the database.
"""

import pandas as pd

from sqlalchemy.exc import SQLAlchemyError

from app import create_app, db

from app.models.customer import Customer
from app.models.loan import Loan


# Spin up the app so we can talk to the database
app = create_app()


# We need the app context or SQLAlchemy will complain about being "outside" the app
with app.app_context():

    try:

        # Ensure the tables exist before we try to shove data into them
        db.create_all()

        # Load up the CSVs we generated earlier
        customers_df = pd.read_csv(
            "customers.csv"
        )

        loans_df = pd.read_csv(
            "loans.csv"
        )

        print("CSV files loaded successfully.")

        # Wipe the slate clean so we don't have duplicate or stale data
        Loan.query.delete()

        Customer.query.delete()

        db.session.commit()

        print("Old records removed.")

        # Iterate through customers and convert types on the fly
        for _, row in customers_df.iterrows():

            try:

                customer = Customer(

                    id=int(
                        row["customer_id"]
                    ),

                    age=str(
                        row["age"]
                    ),

                    # Fallback to 0 if income is missing; don't want the script to die
                    income=float(
                        row["income"]
                    )
                    if pd.notna(
                        row["income"]
                    )
                    else 0,

                    gender=str(
                        row["gender"]
                    )
                    if pd.notna(
                        row["gender"]
                    )
                    else None
                )

                db.session.add(customer)

            # If a row is total junk, just skip it and keep moving
            except ValueError:

                print(
                    f"Invalid customer row skipped: {row}"
                )

        db.session.commit()

        print("Customers added successfully.")

        # Now do the same for the loans
        for _, row in loans_df.iterrows():

            try:

                loan = Loan(

                    id=int(
                        row["loan_id"]
                    ),

                    customer_id=int(
                        row["customer_id"]
                    ),

                    loan_amount=float(
                        row["loan_amount"]
                    )
                    if pd.notna(
                        row["loan_amount"]
                    )
                    else 0,

                    credit_score=int(
                        row["credit_score"]
                    )
                    if pd.notna(
                        row["credit_score"]
                    )
                    else 0,

                    default_status=int(
                        row["default_status"]
                    )
                    if pd.notna(
                        row["default_status"]
                    )
                    else 0
                )

                db.session.add(loan)

            # Skip the bad ones here too
            except ValueError:

                print(
                    f"Invalid loan row skipped: {row}"
                )

        db.session.commit()

        print("Loans added successfully.")

        print("Database loading completed.")

    # If the DB chokes, roll back the transaction so we don't leave it in a weird state
    except SQLAlchemyError as e:

        db.session.rollback()

        print(
            f"Database Error: {e}"
        )

    # Check if someone forgot to run the processing script first
    except FileNotFoundError as e:

        print(
            f"File Error: {e}"
        )

    # The 'I have no idea what happened' safety net
    except Exception as e:

        db.session.rollback()

        print(
            f"Unexpected Error: {e}"
        )