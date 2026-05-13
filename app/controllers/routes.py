"""
Main routes for the loan management system.

This file handles:
- Home page
- Customer pages
- Loan pages
- Analysis reports
- Chart generation
- CRUD operations
"""

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session
)

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from app import db
from app.models.customer import Customer
from app.models.loan import Loan

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


# BLUEPRINT SETUP
main = Blueprint("main", __name__)


def save_bar_chart(labels, values, colors, title, ylabel, path):
    """
    Create and save a simple bar chart.
    This utility formats the chart with custom colors, labels, and 
    a clean aesthetic before saving it to the static folder.
    """

    if not values:
        values = [0]

    plt.figure(figsize=(11, 6))

    bars = plt.bar(
        labels,
        values,
        color=colors,
        edgecolor="#444",
        width=0.6
    )

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + (max(values) * 0.01),
            str(int(height)),
            ha="center",
            fontsize=10,
            fontweight="bold",
            color="#333"
        )

    plt.title(
        title,
        fontsize=16,
        fontweight="bold",
        color="#333",
        pad=28
    )

    plt.ylabel(
        ylabel,
        fontsize=11,
        color="#444"
    )

    plt.ylim(
        0,
        max(values) + 500
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    ax = plt.gca()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#666")
    ax.spines["bottom"].set_color("#666")

    ax.spines["left"].set_linewidth(1.3)
    ax.spines["bottom"].set_linewidth(1.3)

    ax.set_facecolor("#f8f9fb")

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=140,
        bbox_inches="tight"
    )

    plt.close()


@main.route("/")
def home():
    """
    Main dashboard view.
    Calculates total counts and risk distribution to display on the home screen.
    """

    try:

        high_risk = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.credit_score < 600
        ).scalar()

        medium_risk = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.credit_score.between(600, 750)
        ).scalar()

        low_risk = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.credit_score > 750
        ).scalar()

        total_customers = Customer.query.count()

        total_loans = Loan.query.count()

        labels = [
            "High Risk",
            "Medium Risk",
            "Low Risk"
        ]

        values = [
            high_risk,
            medium_risk,
            low_risk
        ]

        colors = [
            "#ff6b6b",
            "#f7b731",
            "#20bf6b"
        ]

        chart_path = os.path.join(
            "app",
            "static",
            "home_chart.png"
        )

        save_bar_chart(
            labels,
            values,
            colors,
            "Loan Risk Distribution",
            "Number of Loans",
            chart_path
        )

        return render_template(
            "home.html",
            total_customers=total_customers,
            total_loans=total_loans
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Database problem occurred.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500

    except Exception as e:

        print(e)

        return render_template(
            "errors/general.html"
        ), 500

@main.route("/login", methods=["GET", "POST"])
def login():
    """
    Simple admin login.
    """

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        if username == "admin" and password == "admin123":

            session["user"] = username

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
                url_for("main.home")
            )

        flash(
            "Invalid username or password.",
            "error"
        )

    return render_template(
        "login.html"
    )

@main.route("/logout")
def logout():
    """
    Logout current user.
    """

    session.pop("user", None)

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("main.login")
    )

@main.route("/customers")
def customers():
    """
    List view for all customers.
    Includes functionality for:
    - Searching by customer ID
    - Sorting customers
    - Pagination
    """

    try:

        search = request.args.get("search")

        sort = request.args.get("sort")

        page = request.args.get(
            "page",
            1,
            type=int
        )

        query = Customer.query


        # CUSTOMER ID SEARCH

        if search:

            query = query.filter(
                Customer.id.cast(db.String).contains(search)
            )


        # SORTING OPTIONS

        if sort == "highest_income":

            query = query.order_by(
                Customer.income.desc()
            )

        elif sort == "lowest_income":

            query = query.order_by(
                Customer.income.asc()
            )

        elif sort == "youngest":

            query = query.order_by(
                Customer.age.asc()
            )

        elif sort == "oldest":

            query = query.order_by(
                Customer.age.desc()
            )

        else:

            query = query.order_by(
                Customer.id
            )


        # PAGINATION

        customers_data = query.paginate(
            page=page,
            per_page=20
        )


        # EMPTY RESULT MESSAGE

        if not customers_data.items:

            flash(
                "No customers found.",
                "warning"
            )


        return render_template(
            "customers.html",
            customers=customers_data
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Unable to load customers.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500

    except Exception as e:

        print(e)

        return render_template(
            "errors/general.html"
        ), 500

        customers_data = query.paginate(
            page=page,
            per_page=20
        )

        if not customers_data.items:

            flash(
                "No customers found.",
                "warning"
            )

        return render_template(
            "customers.html",
            customers=customers_data
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Unable to load customers.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500

    except Exception as e:

        print(e)

        return render_template(
            "errors/general.html"
        ), 500


@main.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    """
    Handles the creation of a new customer record.
    """

    if "user" not in session:

        flash(
            "Please login first.",
            "error"
        )

        return redirect(
            url_for("main.login")
        )

    try:

        if request.method == "POST":

            age = request.form.get("age")

            income = float(
                request.form.get("income")
            )

            gender = request.form.get("gender")

            if not age or not gender:

                flash(
                    "All fields are required.",
                    "error"
                )

                return render_template(
                    "add_customer.html"
                )

            if income < 0:

                flash(
                    "Income cannot be negative.",
                    "error"
                )

                return render_template(
                    "add_customer.html"
                )

            customer = Customer(
                age=age,
                income=income,
                gender=gender
            )

            db.session.add(customer)

            db.session.commit()

            flash(
                "Customer added successfully.",
                "success"
            )

            return redirect(
                url_for("main.customers")
            )

        return render_template(
            "add_customer.html"
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Database error occurred.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500


@main.route("/update_customer/<int:id>", methods=["GET", "POST"])
def update_customer(id):
    """
    Updates existing customer details.
    """

    if "user" not in session:

        flash(
            "Please login first.",
            "error"
        )

        return redirect(
            url_for("main.login")
        )

    try:

        customer = Customer.query.get_or_404(id)

        if request.method == "POST":

            income = float(
                request.form.get("income")
            )

            if income < 0:

                flash(
                    "Income cannot be negative.",
                    "error"
                )

                return render_template(
                    "update_customer.html",
                    customer=customer
                )

            customer.income = income

            db.session.commit()

            flash(
                "Customer income updated successfully.",
                "success"
            )

            return redirect(
                url_for("main.customers")
            )

        return render_template(
            "update_customer.html",
            customer=customer
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Unable to update customer.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500


@main.route("/delete_customer/<int:id>")
def delete_customer(id):
    """
    Removes a customer record and clears their linked loan history.
    """

    if "user" not in session:

        flash(
            "Please login first.",
            "error"
        )

        return redirect(
            url_for("main.login")
        )

    try:

        customer = Customer.query.get_or_404(id)

        Loan.query.filter_by(
            customer_id=id
        ).delete()

        db.session.delete(customer)

        db.session.commit()

        flash(
            "Customer deleted successfully.",
            "success"
        )

        return redirect(
            url_for("main.customers")
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Unable to delete customer.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500


@main.route("/customer/<int:id>")
def customer_detail(id):
    """
    Shows a detailed profile of a specific customer along with their loans.
    """

    try:

        customer = Customer.query.get_or_404(id)

        loans = Loan.query.filter_by(
            customer_id=id
        ).all()

        loan_count = len(loans)

        if not loans:

            flash(
                "This customer has no loans yet.",
                "warning"
            )

        return render_template(
            "customer_detail.html",
            customer=customer,
            loans=loans,
            loan_count=loan_count
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Could not load customer data.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500

    except HTTPException as e:

        raise e

    except Exception as e:

        print(e)

        return render_template(
            "errors/general.html"
        ), 500


@main.route("/loans")
def loans():
    """
    List view for all loans.
    Includes:
    - Customer search
    - Credit score filtering
    - Risk filtering
    - Sorting
    - Pagination
    """

    try:

        search = request.args.get("search")

        min_score = request.args.get("score")

        sort = request.args.get("sort")

        risk = request.args.get("risk")

        page = request.args.get(
            "page",
            1,
            type=int
        )

        query = Loan.query


        # CUSTOMER ID SEARCH

        if search:

            query = query.filter(
                Loan.customer_id.cast(db.String).contains(search)
            )


        # MINIMUM CREDIT SCORE FILTER

        if min_score:

            try:

                min_score = int(min_score)

                if min_score < 0:

                    flash(
                        "Credit score cannot be negative.",
                        "error"
                    )

                    return render_template(
                        "errors/400.html"
                    ), 400

                query = query.filter(
                    Loan.credit_score >= min_score
                )

            except ValueError:

                flash(
                    "Enter a valid credit score.",
                    "error"
                )

                return render_template(
                    "errors/400.html"
                ), 400


        # RISK FILTERING

        if risk == "high":

            query = query.filter(
                Loan.credit_score < 600
            )

        elif risk == "medium":

            query = query.filter(
                Loan.credit_score.between(600, 750)
            )

        elif risk == "low":

            query = query.filter(
                Loan.credit_score > 750
            )


        # SORTING OPTIONS

        if sort == "highest_loan":

            query = query.order_by(
                Loan.loan_amount.desc()
            )

        elif sort == "lowest_loan":

            query = query.order_by(
                Loan.loan_amount.asc()
            )

        elif sort == "highest_score":

            query = query.order_by(
                Loan.credit_score.desc()
            )

        elif sort == "lowest_score":

            query = query.order_by(
                Loan.credit_score.asc()
            )

        else:

            query = query.order_by(
                Loan.id
            )


        # PAGINATION

        loans_data = query.paginate(
            page=page,
            per_page=20
        )


        # EMPTY RESULTS

        if not loans_data.items:

            flash(
                "No loans matched the filters.",
                "warning"
            )


        return render_template(
            "loans.html",
            loans=loans_data
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Problem loading loan data.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500

    except Exception as e:

        print(e)

        flash(
            "Unexpected error occurred.",
            "error"
        )

        return render_template(
            "errors/general.html"
        ), 500


@main.route("/add_loan", methods=["GET", "POST"])
def add_loan():
    """
    Registers a new loan for an existing customer.
    """

    if "user" not in session:

        flash(
            "Please login first.",
            "error"
        )

        return redirect(
            url_for("main.login")
        )

    try:

        if request.method == "POST":

            customer_id = int(
                request.form.get("customer_id")
            )

            loan_amount = float(
                request.form.get("loan_amount")
            )

            credit_score = int(
                request.form.get("credit_score")
            )

            default_status = int(
                request.form.get("default_status")
            )

            customer = Customer.query.get(customer_id)

            if not customer:

                flash(
                    "No customer found with that ID.",
                    "error"
                )

                return render_template(
                    "add_loan.html"
                )

            if loan_amount < 0:

                flash(
                    "Loan amount cannot be negative.",
                    "error"
                )

                return render_template(
                    "add_loan.html"
                )

            if credit_score < 0:

                flash(
                    "Credit score cannot be negative.",
                    "error"
                )

                return render_template(
                    "add_loan.html"
                )

            loan = Loan(
                customer_id=customer_id,
                loan_amount=loan_amount,
                credit_score=credit_score,
                default_status=default_status
            )

            db.session.add(loan)

            db.session.commit()

            flash(
                "Loan added successfully.",
                "success"
            )

            return redirect(
                url_for("main.loans")
            )

        return render_template(
            "add_loan.html"
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Database error occurred.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500


@main.route("/update_loan/<int:id>", methods=["GET", "POST"])
def update_loan(id):
    """
    Allows modification of existing loan terms.
    """

    if "user" not in session:

        flash(
            "Please login first.",
            "error"
        )

        return redirect(
            url_for("main.login")
        )

    try:

        loan = Loan.query.get_or_404(id)

        if request.method == "POST":

            loan_amount = float(
                request.form.get("loan_amount")
            )

            credit_score = int(
                request.form.get("credit_score")
            )

            default_status = int(
                request.form.get("default_status")
            )

            if loan_amount < 0:

                flash(
                    "Loan amount cannot be negative.",
                    "error"
                )

                return render_template(
                    "update_loan.html",
                    loan=loan
                )

            if credit_score < 0:

                flash(
                    "Credit score cannot be negative.",
                    "error"
                )

                return render_template(
                    "update_loan.html",
                    loan=loan
                )

            loan.loan_amount = loan_amount

            loan.credit_score = credit_score

            loan.default_status = default_status

            db.session.commit()

            flash(
                "Loan updated successfully.",
                "success"
            )

            return redirect(
                url_for("main.loans")
            )

        return render_template(
            "update_loan.html",
            loan=loan
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Unable to update loan.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500


@main.route("/delete_loan/<int:id>")
def delete_loan(id):
    """
    Deletes a loan entry from the system.
    """

    if "user" not in session:

        flash(
            "Please login first.",
            "error"
        )

        return redirect(
            url_for("main.login")
        )

    try:

        loan = Loan.query.get_or_404(id)

        db.session.delete(loan)

        db.session.commit()

        flash(
            "Loan deleted successfully.",
            "success"
        )

        return redirect(
            url_for("main.loans")
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Unable to delete loan.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500


@main.route("/analysis")
def analysis():
    """
    Statistical analysis view.
    Generates reports on defaults, averages,
    risk distribution, and risky customers.
    """

    try:

        page = request.args.get(
            "page",
            1,
            type=int
        )

        # AVERAGE CUSTOMER INCOME

        avg_income = db.session.query(
            func.avg(Customer.income)
        ).scalar()


        # AVERAGE LOAN

        avg_loan = db.session.query(
            func.avg(Loan.loan_amount)
        ).scalar()


        # MAXIMUM LOAN

        max_loan = db.session.query(
            func.max(Loan.loan_amount)
        ).scalar()


        # AVERAGE CREDIT SCORE

        average_credit_score = db.session.query(
            func.avg(Loan.credit_score)
        ).scalar()


        # TOTAL LOANS

        total_loans = db.session.query(
            func.count(Loan.id)
        ).scalar()


        # TOTAL DEFAULTS

        total_defaults = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.default_status == 1
        ).scalar()


        # DEFAULT RATE

        default_percentage = 0

        if total_loans > 0:

            default_percentage = round(
                (total_defaults / total_loans) * 100,
                2
            )


        # SAFE LOAN RATE

        safe_percentage = round(
            100 - default_percentage,
            2
        )


        # RISK COUNTS

        high_risk = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.credit_score < 600
        ).scalar()


        medium_risk = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.credit_score.between(600, 750)
        ).scalar()


        low_risk = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.credit_score > 750
        ).scalar()


        # RISK PERCENTAGES

        high_risk_percentage = 0
        medium_risk_percentage = 0
        low_risk_percentage = 0

        if total_loans > 0:

            high_risk_percentage = round(
                (high_risk / total_loans) * 100,
                2
            )

            medium_risk_percentage = round(
                (medium_risk / total_loans) * 100,
                2
            )

            low_risk_percentage = round(
                (low_risk / total_loans) * 100,
                2
            )


        # MOST RISKY CUSTOMER

        most_risky_loan = Loan.query.filter(
            Loan.credit_score < 600
        ).order_by(
            Loan.credit_score.asc(),
            Loan.loan_amount.desc()
        ).first()


        # SAFE LOAN COUNT

        safe_loans_count = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.default_status == 0
        ).scalar()


        # AVERAGE DEFAULTED LOAN

        average_defaulted_loan = db.session.query(
            func.avg(Loan.loan_amount)
        ).filter(
            Loan.default_status == 1
        ).scalar()


        # LARGE LOANS ABOVE 1 MILLION

        large_loans = db.session.query(
            func.count(Loan.id)
        ).filter(
            Loan.loan_amount > 1000000
        ).scalar()


        # INSIGHTS SECTION

        insights = []

        if medium_risk > high_risk and medium_risk > low_risk:

            insights.append(
                "Medium risk loans are the largest category."
            )

        if average_credit_score > 700:

            insights.append(
                "Average credit score remains above 700."
            )

        if default_percentage > 20:

            insights.append(
                "Default rate is relatively high."
            )

        if large_loans > 0:

            insights.append(
                f"There are {large_loans} loans above 1 million."
            )


        # DEFAULTS BY AGE

        defaults_by_age = db.session.query(
            Customer.age,
            func.count(Loan.id)
        ).join(
            Loan,
            Customer.id == Loan.customer_id
        ).filter(
            Loan.default_status == 1
        ).group_by(
            Customer.age
        ).all()


        ages = [str(item[0]) for item in defaults_by_age]

        counts = [item[1] for item in defaults_by_age]


        # CHART GENERATION

        chart_path = os.path.join(
            "app",
            "static",
            "chart.png"
        )

        save_bar_chart(
            ages,
            counts,
            ["#4f75ad"] * len(ages),
            "Defaults by Age",
            "Defaults",
            chart_path
        )


        # RISKY CUSTOMERS

        risky_customers = db.session.query(
            Customer
        ).join(
            Loan,
            Customer.id == Loan.customer_id
        ).filter(
            Loan.credit_score < 600
        ).distinct().paginate(
            page=page,
            per_page=10
        )


        if not risky_customers.items:

            flash(
                "No risky customers found.",
                "warning"
            )


        return render_template(
            "analysis.html",

            avg_income=round(avg_income or 0, 2),

            avg_loan=round(avg_loan or 0, 2),

            max_loan=round(max_loan or 0, 2),

            average_credit_score=round(
                average_credit_score or 0,
                2
            ),

            total_defaults=total_defaults or 0,

            default_percentage=default_percentage,

            safe_percentage=safe_percentage,

            high_risk=high_risk or 0,

            medium_risk=medium_risk or 0,

            low_risk=low_risk or 0,

            high_risk_percentage=high_risk_percentage,

            medium_risk_percentage=medium_risk_percentage,

            low_risk_percentage=low_risk_percentage,

            most_risky_loan=most_risky_loan,

            safe_loans_count=safe_loans_count,

            average_defaulted_loan=round(
                average_defaulted_loan or 0,
                2
            ),

            large_loans=large_loans,

            insights=insights,

            defaults_by_age=defaults_by_age,

            risky_customers=risky_customers
        )

    except SQLAlchemyError as e:

        db.session.rollback()

        flash(
            "Analysis data could not be loaded.",
            "error"
        )

        print(e)

        return render_template(
            "errors/500.html"
        ), 500

    except Exception as e:

        print(e)

        return render_template(
            "errors/general.html"
        ), 500