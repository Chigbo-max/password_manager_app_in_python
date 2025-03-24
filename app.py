from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from mongoengine import connect

from apps.admin.views import auth_view
from helpers.config import Config, init_database

app = Flask(__name__)

connect(host=Config.MONGO_URI)

app.config.from_object(Config)

jwt = JWTManager(app)
app.register_blueprint(auth_view, url_prefix="/api")

if __name__ == '__main__':
    app.run()
