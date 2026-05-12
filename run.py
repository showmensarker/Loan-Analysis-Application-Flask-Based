"""
Main file used to start
the Flask application.
"""

from app import create_app


# Create Flask app
app = create_app()


# Run application
if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )