from sqlalchemy import text
from extensions import db
from constants import DB_USER, DB_PASSWORD, DB_ADDRESS, DB_PORT, DB_NAME


class DatabaseMiddleware:
    def init_database(self, app):
        if not app.config.get("SQLALCHEMY_DATABASE_URI"):
            app.config["SQLALCHEMY_DATABASE_URI"] = (
                f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
            )
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(app)

        with app.app_context():
            try:
                db.session.execute(text("SELECT 1"))
                print("Database connected successfully")
            except Exception as e:
                print(f"Database connection failed: {e}")
                exit(1)

        return db
