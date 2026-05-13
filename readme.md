# Loan Analysis Flask Application

This project is a Flask web application created to analyse customer and loan data from a loan default dataset. The system allows users to manage customers and loans, view reports, paginate large datasets, authenticate administrators, and analyse loan risk using charts and statistics.

The application was built using Flask, SQLAlchemy, SQLite, HTML, CSS, and Matplotlib.

---

# Features

## Authentication
- Admin login system
- Session-based authentication
- Protected add, update, and delete operations
- Secure logout functionality

## Customer Management
- View all customers
- Add new customers
- Update customer income
- Delete customers
- View customer loan history
- Customer pagination support
- Sort customers by highest or lowest income

## Loan Management
- View all loans
- Add new loans
- Update loan information
- Delete loans
- View detailed loan records
- Loan pagination support
- Loan risk categorisation
- Loan filtering and sorting

## Analysis Dashboard
- Average customer income
- Average loan amount
- Maximum loan amount
- Total defaulted loans
- Risk distribution analysis
- Risky customer identification
- Paginated risky customer table

## Charts
- Loan risk distribution chart
- Defaults by age chart

## Filtering and Search
- Search customers by customer ID
- Filter loans using minimum credit score, customer ID, and loan risk category

## Error Handling
Custom error pages for:
- 400 Error
- 403 Error
- 404 Error
- 405 Error
- 500 Error

---

# Project Structure

```text
loan_analysis_project/
├── app/
│   ├── controllers/
│   │   └── routes.py
│   │
│   ├── models/
│   │   ├── customer.py
│   │   └── loan.py
│   │
│   ├── static/
│   │   ├── background.png
│   │   ├── chart.png
│   │   ├── favicon.png
│   │   ├── home_chart.png
│   │   └── style.css
│   │
│   ├── templates/
│   │   ├── errors/
│   │   ├── add_customer.html
│   │   ├── add_loan.html
│   │   ├── analysis.html
│   │   ├── base.html
│   │   ├── customer_detail.html
│   │   ├── customers.html
│   │   ├── home.html
│   │   ├── loans.html
│   │   ├── login.html
│   │   ├── update_customer.html
│   │   └── update_loan.html
│   │
│   └── __init__.py
│
├── instance/
│   └── database.sqlite3
│
├── tests/
│   ├── test_models.py
│   └── test_routes.py
│
├── customers.csv
├── Loan_Default.csv
├── loans.csv
├── process_loan_data.py
├── load_data.py
├── pytest.ini
├── requirements.txt
├── run.py
├── readme.md
├── .gitignore
```

---

# Installation

## Requirements

- Python 3
- Flask
- SQLite

---

# Setup

## Clone the repository

```bash
git clone https://github.com/showmensarker/Loan-Analysis-Application-Flask-Based
cd loan_analysis_project
```

## Create virtual environment

```bash
python -m venv venv
```

## Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the application

```bash
python run.py
```

Open the browser and go to:

```text
http://127.0.0.1:5000/
```

---

# Login Credentials

The application uses a simple administrator login system.

```text
Username: admin
Password: admin123
```

Protected routes include:
- Add customer
- Update customer
- Delete customer
- Add loan
- Update loan
- Delete loan

---

# Dataset

The project uses customer and loan datasets containing:

### Customer Data
- Age range
- Income
- Gender

### Loan Data
- Loan amount
- Credit score
- Default status
- Customer ID

---

# Main Pages

## Dashboard
Shows summary cards and loan risk charts.

## Customers
Displays customer records, pagination, and customer management options.

## Customer Details
Shows detailed information about a customer and their loans.

## Loans
Displays loan records with filtering, pagination, and risk analysis.

## Analysis
Shows statistics, charts, risky customer information, and paginated risky customer tables.

## Login
Allows administrators to access protected management features.

---

# Technologies Used

## Backend
- Flask
- SQLAlchemy
- Python

## Frontend
- HTML
- CSS
- Jinja Templates

## Database
- SQLite

## Libraries
- Matplotlib
- Pandas
- Pytest

---

# Testing

Pytest was used for automated testing across multiple parts of the application.

The testing suite includes:

- Route testing
- Functional testing
- Unit testing
- Authentication and session testing
- Validation testing
- Error handling tests
- Pagination and filtering tests
- Boundary and edge-case testing
- Customer detail testing
- Loan filtering tests
- Analysis page testing
- Static file testing

The application includes over 60 automated tests covering both isolated logic and full route behaviour.

Examples of tested features include:
- Login and logout functionality
- Protected route access
- Invalid input handling
- Customer and loan searches
- Pagination behaviour
- Credit score validation
- Analysis statistics rendering
- Custom error pages
- Chart availability

Run tests using:

```bash
pytest -v
```

Optional cleaner output:

```bash
pytest -q
```

# Deployment

The application was deployed on Render using Gunicorn.

Production start command:

```bash
gunicorn run:app
```

---

# Future Improvements

Some improvements that can be added later:
- Password hashing
- Interactive charts and real-time analytics
- Export reports
- PostgreSQL database support
- Docker deployment
- Advanced filtering and analytics

---

# Notes

Some generated files were excluded using `.gitignore`:

venv/
__pycache__/
*.pyc
.env
app.log
tempCodeRunnerFile.py
---

# License

This project was created for educational purposes.