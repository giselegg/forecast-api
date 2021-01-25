import pytest

from fastapi.testclient import TestClient
from json import dumps

from app import app
from mock import user1, user2


class TestUsers:
    def setup(self):
        self.client = TestClient(app)


    def test_fail_retrieve_all_users(self):
        response = self.client.get("/users")

        assert response.status_code == 404


    def test_success_create_user1(self):
        response = self.client.post("/users", json=user1)

        assert response.status_code == 201


    def test_success_create_user2(self):
        response = self.client.post("/users", json=user2)

        assert response.status_code == 201


    def test_fail_create_user(self):
        response = self.client.post("/users", json=user1)

        assert response.status_code == 400


    def test_success_retrieve_all_users(self):
        response = self.client.get("/users")

        assert response.status_code == 200
        assert len(response.json()) == 2


    def test_success_retrieve_single_user(self):
        response = self.client.get("/users/1")
        sorted_user1 = dumps({
                "id": 1,
                "password": "fidel",
                "username": "gisele"
                },
            sort_keys=True)

        assert response.status_code == 200
        assert dumps(response.json(), sort_keys=True) == sorted_user1


    def test_fail_retrieve_single_user(self):
        response = self.client.get("/users/3")

        assert response.status_code == 400


    def test_success_update_user(self):
        update = {
            "username": "gisele",
            "password": "felix"
        }

        response = self.client.put("/users/1", json=update)
        assert response.status_code == 201


    def test_fail_update_user(self):
        update = {
            "username": "giselegg",
            "password": "felix"
        }

        response = self.client.put("/users/3", json=update)
        assert response.status_code == 400


    def test_success_remove_user(self):
        response = self.client.delete("/users/2")

        assert response.status_code == 204

        response_get = self.client.get("/users/")
        assert len(response_get.json()) == 1


    def test_fail_remove_user(self):
        response = self.client.delete("/users/3")

        assert response.status_code == 400
