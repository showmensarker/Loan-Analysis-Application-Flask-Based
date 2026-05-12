# app/__init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()


def create_app():
    """
    Create Flask application.
    """

    app = Flask(__name__)

    # Change the secret key for production or the sessions won't be secure
    app.config["SECRET_KEY"] = "loanapp-secret-key"

    # SQLite is fine for local dev, but we'll need something beefier for scale
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///database.sqlite3"
    )

    # Silence the FS_TRACK_MODIFICATIONS warning to keep the logs clean
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Fire up the database connection
    db.init_app(app)

    # Writing errors to a file so we don't have to hunt through terminal history
    logging.basicConfig(
        filename="app.log",
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    app.logger.info("Application started")

    # Importing the blueprint here to prevent the app from choking on circular imports
    from app.controllers.routes import main

    app.register_blueprint(main)

    # Catching a 400 when the client sends us something weird
    @app.errorhandler(400)
    def bad_request(e):

        app.logger.error(f"400 Error: {e}")

        return render_template(
            "errors/400.html"
        ), 400

    # Standard 'Access Denied' handler
    @app.errorhandler(403)
    def forbidden(e):

        app.logger.error(f"403 Error: {e}")

        return render_template(
            "errors/403.html"
        ), 403

    # If they go looking for a page that doesn't exist
    @app.errorhandler(404)
    def not_found(e):

        app.logger.error(f"404 Error: {e}")

        return render_template(
            "errors/404.html"
        ), 404

    # Someone tried a POST on a GET-only route
    @app.errorhandler(405)
    def method_not_allowed(e):

        app.logger.error(f"405 Error: {e}")

        return render_template(
            "errors/405.html"
        ), 405

    # The 'Internal Server Error' fallback
    @app.errorhandler(500)
    def server_error(e):

        app.logger.error(f"500 Error: {e}")

        return render_template(
            "errors/500.html"
        ), 500

    # The ultimate safety net for anything we didn't specifically catch
    @app.errorhandler(Exception)
    def handle_exception(e):

        app.logger.error(f"Unexpected Error: {e}")

        return render_template(
            "errors/general.html",
            error=e
        ), 500

    return app