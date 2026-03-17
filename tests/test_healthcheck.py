from requests import request


class TestHealthcheck:
    def test_healthcheck(self, client):
        get_response = client.get("/healthcheck/")
        assert get_response.status_code == 200
