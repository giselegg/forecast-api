from fastapi.testclient import TestClient

from app import app


class TestForecast:
    def setup(self):
        self.client = TestClient(app)


    def test_success_get_forecast(self):
        response = self.client.get("forecast/palhoça")
        assert response.status_code == 200


    def test_fail_get_forecast(self):
        response = self.client.get("/forecast")
        assert response.status_code == 404
