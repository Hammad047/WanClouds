import datetime
import json
import urllib
import bcrypt
import requests
from app import *
from flask import request, jsonify
from models import user, car
from authentication.email import *
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)


# By using this you can sign up and create an account which will be stored in "users" table
@app.route('/user/signup', methods=['POST'])
def signup():
    """
    This function allow the user to sign up. User will provide name, email, password for signup and this data will be
    stored in our local database.
    :return: access_token, refresh_token
    """
    if request.method == 'POST':
        data = request.get_json()  # getting data from POSTMAN
        name = data['name']  # get name
        email = data['email']  # get email
        password = data['password']  # get password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        send_email('', email)
        adddata = user.User(name, email, hashed_password)  # Passing to the user_data
        adddata.create()  # Here calling create functing to store the data in table.
        return 'Congratulation! You have signed-up successfully.'


# By using this user can log in by providing email and password which they entered during signup process.
@app.route('/user/signin', methods=['POST'])
def signin():
    """
    This function allow the user to access the APIs. It will match the user email & password with the data stored in
    our local database and then access token and refresh token will be assigned to the user.
    :return: access_token, refresh_token
    """

    if request.method == 'POST':
        data = request.get_json()  # get data from postman
        email = data['email']  # get email
        password = data['password']  # get password
        userdata = db.session.query(user.User).filter_by(
            email=email).first()  # This query will help us to search data from users table.
        if not userdata and check_password_hash(userdata.password, password):  # if no record found
            return f'Warning! {data["email"]} Invalid email or {data["password"]} password'
        else:
            access_token = create_access_token(identity=data['email'], fresh=True)
            refresh_token = create_refresh_token(identity=data['email'])
            return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    This function is used to refresh the token which we create when a user log in.
    :return: token
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=True)
    return jsonify(access_token=access_token, fresh=True)


# By using this user can create a dataset using the url given
@app.route('/dataset/createdataset', methods=['POST'])
@jwt_required(fresh=True)
def create_dataset():
    """
    Here we are fetching dataset from the url https://parseapi.back4app.com/classes/Car_Model_List?limit=10 and then
    this data being stored in our local database.
    :return: dataset
    """
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
        check = db.session.query(car.Car).filter_by(object_id=data['objectId']).first()
        if check == None:
            adddata = car.Car(data['objectId'], data['Year'], data['Make'], data['Model'], data['Category'],
                              data['createdAt'], data['updatedAt'])
            adddata.create()
        else:
            pass
    return


@app.route('/dataset/<int:page>/<int:limit>/done', methods=['POST'])
@jwt_required(fresh=True)
def paginated_dataset(page, limit):
    """
    Pagination is implemented in this function. this function is used to display records depends on the pagination.
    :param limit:
    :param page:
    :return: dataset
    """
    results = db.session.query(car.Car).all()  # This query will help us to search data from cars table.
    query_list = []
    for result in results:
        query_list.append(result.display())
    start_index = (page - 1) * limit
    end_index = start_index + limit
    car_dataset = query_list[start_index:end_index]
    byte_to_string = ''
    for item in car_dataset:
        byte_to_string += str(item) + ' ' + '\n' + '\n'
    return byte_to_string


# Using this user can search the car registration report using "year" and "model" as well
@app.route('/database/search', methods=['POST'])  # this will execute as /database/search?action=year or model
@jwt_required(refresh=True)
def search_registration_report():
    """
     This function allow the user search the car registration report that are stored in our database. Using this
     user can search the car registration report using "year" and "model" as well
     :return: registration_report
     """
    action = request.args.get('action')
    if action == 'model':
        data = request.get_json()
        make = data['make']
        model = data['model']
        db_data = db.session.query(car.Car).filter_by(make=make,
                                                      model=model).first()  # This query will help us to search data from cars table.
        if not db_data:  # if no record found
            return "Car not found"
        return db_data.display()  # if record found

    elif action == 'year':
        data = request.get_json()
        make = data['make']
        year = data['year']
        db_data = db.session.query(car.Car).filter_by(make=make,
                                                      year=year).first()  # This query will help us to search data from cars table.
        if not db_data:  # if no record found
            return "Car not found"
        return db_data.display()  # if record found
    else:
        print('Invalid Action')
    return
