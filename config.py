import os

import dotenv

dotenv.load_dotenv()

MONGODB_URL = os.environ['MONGODB_URL']
MONGODB_NAME = os.environ['MONGODB_NAME']

MYSQL_URL = os.environ['MYSQL_URL']

RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = int(os.environ['RABBITMQ_PORT'])
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']

SECRET = os.environ['SECRET']
