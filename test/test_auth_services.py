from unittest import TestCase

from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect, disconnect
import mongomock

from apps.admin.services import Admin
from apps.auth.models import User
from apps.auth.services import AuthService




class TestAuthService(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config["TESTING"] = True
        cls.app.config["JWT_SECRET_KEY"] = "test_secret"
        cls.jwt = JWTManager(cls.app)
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        User.objects.delete()

    def tearDown(self):
        self.app_context.pop()


    def test_that_registration_function_returns_count_one(self):

        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}

        response, status = auth_service.register(data)
        response_json = response.get_json()

        assert status == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "akerele@gmail.com registered successfully"
        assert User.objects(email="akerele@gmail.com").count() == 1


    def test_that_login_function_status_returns_success(self):
        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}

        response, status = auth_service.register(data)
        response_json = response.get_json()

        assert status == 201
        assert response_json["status"] == "success"

        response, status = auth_service.login(data)
        response_json = response.get_json()

        assert status == 200
        assert response_json["status"] == "success"


    def test_that_reset_password_function_status_returns_success(self):
        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}

        response, status = auth_service.register(data)
        response_json = response.get_json()

        assert status == 201
        assert response_json["status"] == "success"

        response, status = auth_service.login(data)
        response_json = response.get_json()

        assert status == 200
        assert response_json["status"] == "success"


        response, status = auth_service.reset_password(data)
        response_json = response.get_json()
        assert status == 201
        assert response_json["status"] == "success"



    def test_that_account_closure_function_returns_success(self):

        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}
        response, status = auth_service.register(data)
        response_json = response.get_json()
        assert status == 201
        assert response_json["status"] == "success"

        response2, status = auth_service.login(data)
        response_json = response2.get_json()
        assert status == 200
        assert response_json["status"] == "success"

        email={"email": "akerele@gmail.com"}
        response3, status = Admin.close_account(email)
        response_json = response3.get_json()
        assert status == 200
        assert response_json["status"] == "success"

    def test_that_account_activation_function_returns_success(self):
        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}
        response, status = auth_service.register(data)
        response_json = response.get_json()
        assert status == 201
        assert response_json["status"] == "success"

        response2, status = auth_service.login(data)
        response_json = response2.get_json()
        assert status == 200
        assert response_json["status"] == "success"

        email = {"email": "akerele@gmail.com"}
        response3, status = Admin.close_account(email)
        response_json = response3.get_json()
        assert status == 200
        assert response_json["status"] == "success"

        response4, status = Admin.activate_account(email)
        response_json = response4.get_json()
        assert status == 200
        assert response_json["status"] == "success"

    def test_that_account_suspension_function_returns_success(self):
        auth_service = AuthService()
        data = {"email": "akerele@gmail.com", "master_password": "password"}
        response, status = auth_service.register(data)
        response_json = response.get_json()
        assert status == 201
        assert response_json["status"] == "success"

        response2, status = auth_service.login(data)
        response_json = response2.get_json()
        assert status == 200
        assert response_json["status"] == "success"

        email = {"email": "akerele@gmail.com"}
        response3, status = Admin.suspend_account(email)
        response_json = response3.get_json()
        assert status == 200
        assert response_json["status"] == "success"


