import json
import requests
import urllib
from app import celery
from app.api import logger
from database.db import db
from models.car import Car


@celery.task(name="create_dataset")
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
        'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',
        # This is the fake app's application id
        'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'
        # This is the fake app's readonly master key
    }
    try:
        response = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout,
            requests.exceptions.InvalidURL, requests.exceptions.ConnectionError) as err:
        logger.error('Invalid URL')
        return 'Something wrong, Please try again!'
    for data in response['results']:
        car_report = db.session.query(Car).filter_by(object_id=data['objectId']).first()
        if car_report is None:
            car_report = Car(data['objectId'], data['Year'], data['Make'], data['Model'], data['Category'],
                             data['createdAt'], data['updatedAt'])
            car_report.create()
        else:
            pass
    return 'Record Stored'
