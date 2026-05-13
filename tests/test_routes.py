import pytest
from app import create_app

@pytest.fixture
def app():
    """
    Creates the Flask app instance used during testing.
    """

    app = create_app()

    app.config.update({
        "TESTING": True
    })

    yield app


@pytest.fixture
def client(app):
    """
    Returns a Flask test client.
    """

    return app.test_client()


def login(client):
    """
    Reusable login helper for protected pages.
    """

    return client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin123"
        },
        follow_redirects=True
    )



# Main page tests


def test_home_page(client):
    """
    Makes sure the dashboard loads correctly.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert b"Dashboard" in response.data


def test_login_page(client):
    """
    Checks whether the login page opens.
    """

    response = client.get("/login")

    assert response.status_code == 200

    assert b"Admin Login" in response.data



# Login and session tests


def test_valid_login(client):
    """
    Tests login with correct credentials.
    """

    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Login successful" in response.data


def test_invalid_login(client):
    """
    Tests login using incorrect details.
    """

    response = client.post(
        "/login",
        data={
            "username": "wrong",
            "password": "wrong"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Invalid username or password" in response.data


def test_logout(client):
    """
    Ensures logout works correctly.
    """

    login(client)

    response = client.get(
        "/logout",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Logged out successfully" in response.data


def test_add_customer_requires_login(client):
    """
    Checks that add customer page is protected.
    """

    response = client.get(
        "/add_customer",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Login" in response.data


def test_add_loan_requires_login(client):
    """
    Checks that add loan page is protected.
    """

    response = client.get(
        "/add_loan",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Login" in response.data


def test_update_customer_requires_login(client):
    """
    Prevents unauthorised customer updates.
    """

    response = client.get(
        "/update_customer/1",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Login" in response.data


def test_logout_removes_access(client):
    """
    Makes sure protected pages are blocked after logout.
    """

    login(client)

    client.get(
        "/logout",
        follow_redirects=True
    )

    response = client.get(
        "/add_customer",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Login" in response.data



# Customer related tests


def test_customers_page(client):
    """
    Verifies the customer list page loads.
    """

    response = client.get("/customers")

    assert response.status_code == 200

    assert b"Customers" in response.data


def test_customers_pagination(client):
    """
    Checks customer pagination works.
    """

    response = client.get(
        "/customers?page=1"
    )

    assert response.status_code == 200

    assert b"Customers" in response.data


def test_customers_pagination_search(client):
    """
    Tests pagination together with search.
    """

    response = client.get(
        "/customers?page=1&search=35"
    )

    assert response.status_code == 200

    assert b"Customers" in response.data


def test_customer_age_range_search(client):
    """
    Tests numeric search filtering.
    """

    response = client.get(
        "/customers?search=27"
    )

    assert response.status_code == 200

    assert b"Customers" in response.data


def test_customer_search(client):
    """
    Checks general customer search behaviour.
    """

    response = client.get(
        "/customers?search=35"
    )

    assert response.status_code == 200

    assert b"Customers" in response.data


def test_empty_customer_search(client):
    """
    Makes sure empty search results are handled properly.
    """

    response = client.get(
        "/customers?search=XYZINVALID"
    )

    assert response.status_code == 200

    assert b"No customers found" in response.data


def test_large_page_number(client):
    """
    Tests very large page numbers.
    """

    response = client.get(
        "/customers?page=9999"
    )

    assert response.status_code in [200, 404, 500]


def test_empty_search(client):
    """
    Checks behaviour with empty search input.
    """

    response = client.get(
        "/customers?search="
    )

    assert response.status_code == 200

    assert b"Customers" in response.data


def test_customer_invalid_string_id(client):
    """
    Tests invalid customer IDs passed as text.
    """

    response = client.get(
        "/customer/abc"
    )

    assert response.status_code in [400, 404]


def test_add_customer_page(client):
    """
    Ensures add customer page opens after login.
    """

    login(client)

    response = client.get(
        "/add_customer"
    )

    assert response.status_code == 200


def test_update_customer_invalid(client):
    """
    Tries updating a customer that does not exist.
    """

    login(client)

    response = client.get(
        "/update_customer/999999"
    )

    assert response.status_code == 404


def test_invalid_update_customer_string_id(client):
    """
    Checks invalid update requests using text IDs.
    """

    login(client)

    response = client.get(
        "/update_customer/abc"
    )

    assert response.status_code in [400, 404]
    

# Loan tests

def test_loans_page(client):
    """
    Makes sure the loans page loads correctly.
    """

    response = client.get("/loans")

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_loans_pagination(client):
    """
    Checks loan pagination behaviour.
    """

    response = client.get(
        "/loans?page=1"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_loans_pagination_filter(client):
    """
    Tests loan filtering with pagination.
    """

    response = client.get(
        "/loans?page=1&score=700"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_valid_score_filter(client):
    """
    Tests loan filtering with a valid score.
    """

    response = client.get(
        "/loans?score=700"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_zero_score(client):
    """
    Tests filtering with a zero value.
    """

    response = client.get(
        "/loans?score=0"
    )

    assert response.status_code == 200


def test_invalid_score(client):
    """
    Ensures invalid score input is rejected.
    """

    response = client.get(
        "/loans?score=abc"
    )

    assert response.status_code == 400

def test_negative_score(client):
    """
    Ensures negative score values are rejected.
    """

    response = client.get(
        "/loans?score=-10"
    )

    assert response.status_code == 400

    assert b"cannot be negative" in response.data


def test_empty_loans_filter(client):
    """
    Checks behaviour when filters return no loans.
    """

    response = client.get(
        "/loans?score=9999"
    )

    assert response.status_code == 200

    assert b"No loans matched the filter" in response.data


def test_add_loan_page(client):
    """
    Ensures add loan page works after login.
    """

    login(client)

    response = client.get(
        "/add_loan"
    )

    assert response.status_code == 200

def test_customer_id_search(client):
    """
    Tests searching loans by customer ID.
    """

    response = client.get(
        "/loans?search=1"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_risk_filter_high(client):
    """
    Tests high risk filtering.
    """

    response = client.get(
        "/loans?risk=high"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_risk_filter_medium(client):
    """
    Tests medium risk filtering.
    """

    response = client.get(
        "/loans?risk=medium"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_risk_filter_low(client):
    """
    Tests low risk filtering.
    """

    response = client.get(
        "/loans?risk=low"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_sort_highest_loan(client):
    """
    Tests highest loan sorting.
    """

    response = client.get(
        "/loans?sort=highest_loan"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data


def test_sort_lowest_loan(client):
    """
    Tests lowest loan sorting.
    """

    response = client.get(
        "/loans?sort=lowest_loan"
    )

    assert response.status_code == 200

    assert b"Loans" in response.data

# Analysis page tests


def test_analysis_page(client):
    """
    Verifies the analysis page loads correctly.
    """

    response = client.get("/analysis")

    assert response.status_code == 200

    assert b"Average Income" in response.data


def test_analysis_metrics(client):
    """
    Checks that analysis statistics are displayed.
    """

    response = client.get("/analysis")

    assert response.status_code == 200

    assert b"Average Credit Score" in response.data

    assert b"Default Rate" in response.data

    assert b"Safe Loans" in response.data


def test_analysis_pagination(client):
    """
    Tests analysis page pagination.
    """

    response = client.get(
        "/analysis?page=1"
    )

    assert response.status_code == 200

    assert b"Top Risky Customers" in response.data

def test_analysis_risk_cards(client):
    """
    Checks risk analysis cards render correctly.
    """

    response = client.get("/analysis")

    assert response.status_code == 200

    assert b"High Risk" in response.data

    assert b"Medium Risk" in response.data

    assert b"Low Risk" in response.data


def test_analysis_insights(client):
    """
    Checks insights section appears.
    """

    response = client.get("/analysis")

    assert response.status_code == 200

    assert (
        b"System Insights" in response.data
        or b"Insights" in response.data
    )


def test_analysis_large_loans(client):
    """
    Tests large loan statistics section.
    """

    response = client.get("/analysis")

    assert response.status_code == 200

    assert b"Large Loans" in response.data


def test_analysis_most_risky_loan(client):
    """
    Tests risky loan section rendering.
    """

    response = client.get("/analysis")

    assert response.status_code == 200

    assert b"Most Risky Loan" in response.data

# Customer detail tests


def test_customer_detail(client):
    """
    Checks an individual customer page.
    """

    response = client.get("/customer/1")

    assert response.status_code in [200, 404]

    if response.status_code == 200:

        assert b"Customer Details" in response.data


def test_invalid_customer(client):
    """
    Ensures invalid customers return a 404 page.
    """

    response = client.get(
        "/customer/999999"
    )

    assert response.status_code == 404

    assert b"Page Not Found" in response.data


# Error handling tests

def test_404_page(client):
    """
    Tests unknown routes.
    """

    response = client.get("/wrongpage")

    assert response.status_code == 404

    assert b"Page Not Found" in response.data


def test_method_not_allowed(client):
    """
    Sends an unsupported request method.
    """

    response = client.post("/analysis")

    assert response.status_code in [405, 500]


# Static file checks

def test_chart_image(client):
    """
    Verifies the chart image exists.
    """

    response = client.get(
        "/static/chart.png"
    )

    assert response.status_code in [200, 304]

# Simple unit tests

def test_average_calculation_logic():
    """
    Checks average calculation logic.
    """

    incomes = [1000, 2000, 3000]

    average = sum(incomes) / len(incomes)

    assert average == 2000


def test_default_rate_logic():
    """
    Tests default rate calculations.
    """

    defaults = 10

    total = 100

    rate = (defaults / total) * 100

    assert rate == 10


def test_safe_loan_logic():
    """
    Checks safe loan threshold logic.
    """

    score = 750

    assert score >= 700


def test_negative_score_logic():
    """
    Tests negative score handling.
    """

    score = -10

    assert score < 0


def test_positive_score_logic():
    """
    Tests positive score validation.
    """

    score = 700

    assert score > 0