import bcrypt
import logging
from app import *
from authentication.email import *
from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from jwt_token import jwt
from models.car import Car
from models.user import User
from schemas.user_schema import UserSchema
from schemas.customized_decorator import validate_schema
from werkzeug.security import check_password_hash

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


# By using this you can sign up and create an account which will be stored in "users" table
@app.route('/user/signup', methods=['POST'])
@validate_schema(UserSchema())
def signup():
    """
    This function allow the user to sign up. User will provide name, email, password for signup and this data will be
    stored in our local database.
    :return: access_token, refresh_token
    """
    if request.method == 'POST':
        data = request.get_json()  # getting data from POSTMAN
        if not data:
            logger.info('Make sure everything is correctly written')
            return Response('Make sure everything is correctly written', status=404)
        # name
        name = data['name']  # get name
        # email
        email = data['email']  # get email
        # password
        password = data['password']  # get password
        # hashed passwords
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_existed = db.session.query(User).filter_by(email=email).first()
        if not user_existed:
            send_email('', email)
            create_user = User(name, email, hashed_password)  # Passing to the user_data
            create_user.create()  # Here calling create functing to store the data in table.
            logger.info('Data Stored')
            return Response('You have successfully signed up. Please check your email for confirmation.', status=201)
        else:
            logger.error("This user is already existed in your database")
            return Response('You already have an account with this email.', status=409)


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
        if not email:
            logger.error("Please check your email")
            return Response('Please check your email', status=404)
        password = data['password']  # get password
        if not password:
            logger.error("Please check your password")
            return Response('Password cannot be empty', status=404)
        userdata = db.session.query(User).filter_by(email=email).first()  # This query will help us
        if not userdata:
            return Response('No User Found', status=404)
        # to search data from users table.
        if not userdata and check_password_hash(userdata.password, password):  # if no record found
            return Response('No record found. Please check your email and password again.', status=404)
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
    return jsonify(access_token=access_token)


@app.route('/dataset/<int:page>/<int:limit>/done', methods=['POST'])
@jwt_required(fresh=True)
def paginated_dataset(page, limit):
    """
    Pagination is implemented in this function. this function is used to display records depends on the pagination.
    :param limit:
    :param page:
    :return: dataset
    """
    results = db.session.query(Car).all()  # This query will help us to search data from cars table.
    if results:
        query_list = []
        for result in results:
            query_list.append(result.display())
        start_index = (page - 1) * limit
        end_index = start_index + limit
        car_dataset = query_list[start_index:end_index]
        byte_to_string = ''
        for item in car_dataset:
            byte_to_string += str(item) + ' ' + '\n' + '\n'
        return Response(byte_to_string, status=200)
    else:
        return Response('No Record Found', status=404)


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
        if data:
            make = data['make']
            if not make:
                return Response('Make can not be empty.', status=404)
            model = data['model']
            if not model:
                return Response('Model can not be empty.', status=404)
            db_data = db.session.query(Car).filter_by(make=make,
                                                      model=model).first()  # This query will help us to search data from cars table.
            if not db_data:  # if no record found
                return Response('No Record Found', status=404)
            return Response(db_data.display(), status=200)  # if record found
        else:
            return Response('Something wrong. Please recheck all details', status=404)

    elif action == 'year':
        data = request.get_json()
        if data:
            make = data['make']
            if not make:
                return Response('Make can not be empty.', status=404)
            year = data['year']
            if not year:
                return Response('Year can not be empty.', status=404)
            db_data = db.session.query(Car).filter_by(make=make,
                                                      year=year).first()  # This query will help us to search data from cars table.
            if not db_data:  # if no record found
                return Response('No Record Found', status=404)
            return Response(db_data.display(), status=200)  # if record found
    else:
        print('Invalid Action')
    return Response(status=200)
