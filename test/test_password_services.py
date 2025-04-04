from unittest import TestCase

import mongomock
from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect

from apps.auth.models import User
from apps.auth.services import AuthService
from apps.auth.views import auth_view
from apps.passwords.models import CredentialsEntry
from apps.passwords.views import password_manager_view


class TestPasswordService(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config["TESTING"] = True
        cls.app.config["JWT_SECRET_KEY"] = "test_secret"
        cls.jwt = JWTManager(cls.app)
        cls.app.register_blueprint(auth_view)
        cls.app.register_blueprint(password_manager_view)
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)


    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        User.objects.delete()

    def tearDown(self):
        self.app_context.pop()


    def test_that_credentials_are_saved_return_count_one(self):
        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}

        response, status = auth_service.register(data)
        response_json = response.get_json()

        assert status == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "akerele@gmail.com registered successfully"
        assert User.objects(email="akerele@gmail.com").count() == 1

        with self.app.test_client() as client:

            access_token = client.post("/login", json=data).get_json()["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}


            credentials = {"website": "facebook.com", "password": "password"}

            response2 = client.post("/save-credentials", json=credentials, headers=headers)

            assert response2.status_code == 201
            user = User.objects(email="akerele@gmail.com").first()
            assert CredentialsEntry.objects(user=user).count() == 1


    def test_that_credentials_retrieved_returns_200_status_code(self):
        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}

        response, status = auth_service.register(data)
        response_json = response.get_json()

        assert status == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "akerele@gmail.com registered successfully"
        assert User.objects(email="akerele@gmail.com").count() == 1

        with self.app.test_client() as client:

            access_token = client.post("/login", json=data).get_json()["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}


            credentials = {"website": "facebook.com", "username":"akerele", "password": "password"}

            response2 = client.post("/save-credentials", json=credentials, headers=headers)


            assert response2.status_code == 201
            user = User.objects(email="akerele@gmail.com").first()
            assert CredentialsEntry.objects(user=user).count() == 1

            response3 = client.get("/retrieve-credentials", headers=headers)


            assert response3.status_code == 201



    def test_that_credentials_deleted_returns_200_status_code_and_count_is_zero(self):
        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}

        response, status = auth_service.register(data)
        response_json = response.get_json()

        assert status == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "akerele@gmail.com registered successfully"
        assert User.objects(email="akerele@gmail.com").count() == 1

        with self.app.test_client() as client:

            access_token = client.post("/login", json=data).get_json()["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}


            credentials = {"website": "facebook.com", "username":"akerele", "password": "password"}

            response2 = client.post("/save-credentials", json=credentials, headers=headers)


            assert response2.status_code == 201
            user = User.objects(email="akerele@gmail.com").first()
            assert CredentialsEntry.objects(user=user).count() == 1

            response3 = client.post("/delete-credential/facebook.com", headers=headers)
            print(response3.get_json())

            assert response3.status_code == 200

            user = User.objects.get(email="akerele@gmail.com")
            assert CredentialsEntry.objects(user=user).count() == 0



