from flask_smorest import Api


class DocumentationMiddleware:
    def init_docs(self, app):
        app.config["API_TITLE"] = "Stark Integration API"
        app.config["API_VERSION"] = "1.0"
        app.config["OPENAPI_VERSION"] = "3.1.0"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
        app.config["OPENAPI_SWAGGER_UI_URL"] = (
            "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        )

        api = Api(app)

        return api
