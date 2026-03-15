from requests import request


class TestHealthcheck:
    def test_healthcheck(self):
        get_response = request(method="GET", url="http://localhost:5000/healthcheck")
        assert get_response.status_code == 200
