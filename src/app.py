from flask import Flask
from controllers import (
    HealthCheckController,
    AccountController,
    InvoiceController,
    WebhookController,
)
from middlewares import (
    DatabaseMiddleware,
    LoggerMiddleware,
    DocumentationMiddleware,
    ErrorMiddleware,
)


def create_app(config=None):

    app = Flask(__name__)

    if config:
        app.config.update(config)

    db = DatabaseMiddleware().init_database(app)
    LoggerMiddleware().init_logger(app)

    api = DocumentationMiddleware().init_docs(app)
    ErrorMiddleware().init_errors(app)

    api.register_blueprint(HealthCheckController().healthcheck_bp)
    api.register_blueprint(AccountController().account_bp)
    api.register_blueprint(InvoiceController().invoice_bp)
    api.register_blueprint(WebhookController().webhook_bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if exception:
            db.session.rollback()
        db.session.remove()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
