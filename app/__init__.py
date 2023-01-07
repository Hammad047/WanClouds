import datetime
from flask import Flask
import pymysql
from configuration.config import DatabaseCredentials
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Creating connection with Database, here the name of the database is car_app
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DatabaseCredentials.db_user}:' \
                                        f'{DatabaseCredentials.db_password}@' \
                                        f'{DatabaseCredentials.container_name}/{DatabaseCredentials.db_name}'
app.config["JWT_SECRET_KEY"] = "flask123."
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(minutes=1)


db = SQLAlchemy(app)

from app import api
from app.Model import *

# __all__ = ["app"]


with app.app_context():
    # db.drop_all()
    db.create_all()
