class APIError(Exception):

    def __init__(self, message, status_code=400, payload={}):
        super().__init__(message)
        self.message = message
        self.status = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            422: "Unprocessable Entity",
            500: "Internal Server Error",
        }.get(status_code, "Error")
        self.code = status_code
        self.payload = payload or {}

    def to_dict(self):
        error_dict = {"message": self.message, "status": self.status, "code": self.code}
        if self.payload:
            error_dict["details"] = self.payload
        return error_dict
