from configuration import config
from database.db import db
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config.DatabaseCredentials)
# Creating connection with database, here the name of the database is car_app
# engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/car_app'

from app import api
from models.car import Car
from models.user import User

db.init_app(app)
migrate = Migrate(app, db)
