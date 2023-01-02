# This file contains the APIs that I created to solve the problem.
from functools import wraps

import bcrypt
from werkzeug.security import check_password_hash

from app.Model import user_data, car_data
import urllib
import requests
import json
from app import app, db
from flask import request, jsonify
import jwt
import datetime
from authentication.configuration import token_required, send_email

# By using this you can sign up and create an account which will be stored in "users" table
@app.route('/user/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()  # getting data from POSTMAN
        name = data['name']  # get name
        email = data['email']  # get email
        password = data['password']  # get password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        send_email('', email)
        adddata = user_data(name, email, hashed_password)  # Passing to the user_data
        db.session.add(adddata)
        db.session.commit()
        # adddata.create()  # Here calling create functing to store the data in table.
        return 'Congratulation! You have signed-up successfully.'


# By using this user can log in by providing email and password which they entered during signup process.
@app.route('/user/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()  # get data from postman
        email = data['email']  # get email
        password = data['password']  # get password
        userdata = db.session.query(user_data).filter_by(
            email=email).first()  # This query will help us to search data from users table.
        if not userdata and check_password_hash(userdata.password, password):  # if no record found
            return f'Warning! {data["email"]} Invalid email or {data["password"]} password'
        else:
            # Based on the name of the user a Token will be generated which will be valid for 30 minutes
            token = jwt.encode(
                {'name': userdata.name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'], "HS256")
            return token
        return f' Hi {userdata.name}'  # if record found


# By using this user can create a dataset using the url given, this link is available in "contstants.py" file
@app.route('/dataset/createdataset', methods=['GET'])
@token_required
def createdataset():
    where = urllib.parse.quote_plus("""
    {
        "Year": {
            "$lte": 2032
        }
    }
    """)
    url = 'https://parseapi.back4app.com/classes/Car_Model_List?limit=10'
    headers = {
        'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',  # This is the fake app's application id
        'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'  # This is the fake app's readonly master key
    }
    response = json.loads(
        requests.get(url, headers=headers).content.decode('utf-8'))
    for data in response['results']:
        print(f'data fetched: {data}')
        check = db.session.query(car_data).filter_by(object_id=data['objectId']).first()
        if check == None:
            adddata = car_data(data['objectId'], data['Year'], data['Make'], data['Model'], data['Category'],
                               data['createdAt'], data['updatedAt'])
            adddata.create()
        else:
            pass
    return 'Create Dataset Returned'

# We can see the dataset using this.
@app.route('/dataset', methods=['GET'])  # this will execute as /database/search?action=year or model
def dataset():
    query_list = []
    results = db.session.query(car_data).all()  # This query will help us to search data from cars table.
    for result in results:
        query_list.append(result.display())
    return query_list

# Using this user can search the car registration report using "year" and "model" as well
@app.route('/database/search/<int:page>',
           methods=['POST'])  # this will execute as /database/search?action=year or model
def search(page):
    action = request.args.get('action')
    if action == 'model':
        data = request.get_json()
        make = data['make']
        model = data['model']
        db_data = db.session.query(car_data).filter_by(make=make,
                                                       model=model).first()  # This query will help us to search data from cars table.
        if not db_data:  # if no record found
            return "Car not found"
        return db_data.display()  # if record found

    elif action == 'year':
        data = request.get_json()
        make = data['make']
        year = data['year']
        db_data = db.session.query(car_data).filter_by(make=make,
                                                       year=year).first()  # This query will help us to search data from cars table.
        if not db_data:  # if no record found
            return "Car not found"
        return db_data.display()  # if record found
    else:
        print('Invalid Action')
    return
