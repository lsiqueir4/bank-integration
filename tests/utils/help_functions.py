import requests_mock


class HelpFunctions:
    def mock_external_request(
        self, mock, method, url, json_response=None, status_code=200
    ):
        getattr(mock, method.lower())(
            url, json=json_response or {}, status_code=status_code
        )
