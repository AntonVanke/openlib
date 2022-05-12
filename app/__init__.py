from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app, default_mediatype="application/json")
from . import routes

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
