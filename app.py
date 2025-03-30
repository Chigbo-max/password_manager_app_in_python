from flask_cors import CORS
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from mongoengine import connect


from apps.admin.views import admin_view
from apps.auth.views import auth_view
from apps.passwords.views import password_manager_view
from helpers.config import Config

app = Flask(__name__)

CORS(app,resources={r"/api/*": {"origins": "http://localhost:5173"}})

connect(host=Config.MONGO_URI)

app.config.from_object(Config)

jwt = JWTManager(app)
app.register_blueprint(auth_view, url_prefix="/api")
app.register_blueprint(admin_view, url_prefix="/api")

app.register_blueprint(password_manager_view, url_prefix="/api")

if __name__ == '__main__':
    app.run()
