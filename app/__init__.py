import datetime
from flask import Flask
from configuration.config import DatabaseCredentials
from database.db import db
app = Flask(__name__)
#Creating connection with Database, here the name of the database is car_app
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DatabaseCredentials.db_user}:' \
                                        f'{DatabaseCredentials.db_password}@' \
                                        f'{DatabaseCredentials.container_name}/{DatabaseCredentials.db_name}'
app.config["JWT_SECRET_KEY"] = "flask123."
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(minutes=1)


from app import api
from models import Car, User

db.init_app(app)

with app.app_context():
    db.create_all()

