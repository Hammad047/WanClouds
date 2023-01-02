from flask import Flask, request, jsonify, make_response
import pymysql
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Creating connection with Database, here the name of the database is car_app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/car_app'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

from app import api
from app.Model import *
db.create_all()

