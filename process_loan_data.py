"""
Script used to process
the loan dataset.

Creates:
- customers.csv
- loans.csv
"""

import pandas as pd


# Grab the raw data—make sure the filename matches exactly
df = pd.read_csv("Loan_Default.csv")

# Clean up the column headers because extra spaces are the worst
df.columns = df.columns.str.strip()

# Truncating to 7000 rows so the local DB doesn't get sluggish
df = df.head(7000)


# Peel off the personal info for the Customers table
customers = df[
    ["ID", "age", "income", "Gender"]
].copy()

# Normalizing names so they actually follow the DB schema
customers.rename(
    columns={
        "ID": "customer_id",
        "Gender": "gender"
    },
    inplace=True
)


# Extract the financial data for the Loans table
loans = df[
    ["ID", "loan_amount", "Credit_Score", "Status"]
].copy()

# Syncing these names with the Loan model properties
loans.rename(
    columns={
        "ID": "loan_id",
        "Credit_Score": "credit_score",
        "Status": "default_status"
    },
    inplace=True
)

# Link the loan back to the customer using the ID as a reference
loans["customer_id"] = customers["customer_id"]


# Dump the cleaned dataframes into fresh CSV files
customers.to_csv(
    "customers.csv",
    index=False
)

loans.to_csv(
    "loans.csv",
    index=False
)


# Quick confirmation so we aren't staring at a blank terminal
print("Dataset processed successfully!")

print("Customers:", len(customers))

print("Loans:", len(loans))