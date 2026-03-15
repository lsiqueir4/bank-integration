from errors import APIError
import json


class ErrorMiddleware:
    def init_errors(self, app):
        @app.errorhandler(APIError)
        def handle_api_error(error):
            return error.to_dict(), error.code

        @app.errorhandler(422)
        def handle_validation_422_error(error):
            response = APIError(
                message=json.dumps(error.data.get("messages", {}).get("json", {})),
                status_code=422,
            ).to_dict()
            return response, 422

        @app.errorhandler(500)
        def handle_validation_500_error(error):
            response = APIError(
                message="Internal Error", status_code=error.code
            ).to_dict()
            return response, error.code
