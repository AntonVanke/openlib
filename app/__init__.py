from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api

from .config import Config
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(Config)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app, default_mediatype="application/json")
from . import routes

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
