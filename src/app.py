from flask import Flask
from controllers import HealthCheckController, AccountController
from middlewares import (
    DatabaseMiddleware,
    LoggerMiddleware,
    DocumentationMiddleware,
    ErrorMiddleware,
)
from constants import DEBUG

app = Flask(__name__)
db = DatabaseMiddleware().init_database(app)
LoggerMiddleware().init_logger(app)

api = DocumentationMiddleware().init_docs(app)

ErrorMiddleware().init_errors(app)

api.register_blueprint(HealthCheckController().healthcheck_bp)
api.register_blueprint(AccountController().account_bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        db.session.rollback()
    db.session.remove()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=DEBUG)
