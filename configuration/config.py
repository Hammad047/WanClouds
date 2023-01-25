import os
from datetime import timedelta


class DatabaseCredentials(object):
    db_name = os.environ.get('MYSQL_DATABASE', 'car_app')
    db_user = os.environ.get('MYSQL_USER', 'root')
    db_password = os.environ.get('MYSQL_PASSWORD', 'root')
    db_root_password = os.environ.get('MYSQL_ROOT_PASSWORD', 'root')
    container_name = os.environ.get('container_name', 'db')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{container_name}/{db_name}'


class CeleryConfigurations(DatabaseCredentials):
    Celery_Config = {
        'broker_url': 'redis://redis:6379/0',
        'result_backend': 'redis://redis:6379/0',
    }

    CELERY_BEAT_SCHEDULE = {
        'create_dataset': {
            'task': 'create_dataset',
            'schedule': timedelta(hours=24),
        },
    }
