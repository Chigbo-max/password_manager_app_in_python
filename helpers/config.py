import os

from flask.cli import load_dotenv
from mongoengine import connect

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    FRONTEND_URI = os.environ.get('FRONTEND_URI')


def init_database():
    try:
        connect(host=Config.MONGO_URI)
        print("Database connection successful")
    except Exception as e:
        print("Error while connecting to MongoDB", e)
        exit(1)