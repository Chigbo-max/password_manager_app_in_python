import unittest

import mongomock
from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect

from apps.admin.services import Admin
from apps.admin.views import admin_view
from apps.auth.models import User
from apps.auth.services import AuthService


class AdminServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config["TESTING"] = True
        cls.app.config["JWT_SECRET_KEY"] = "test_secret"
        cls.jwt = JWTManager(cls.app)
        cls.app.register_blueprint(admin_view)

        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        User.objects.delete()

    def tearDown(self):
        self.app_context.pop()



    def test_that_admin_can_view_audit_logs(self):
        pass


