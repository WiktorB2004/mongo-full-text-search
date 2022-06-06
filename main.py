# Imports
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import json
from pprint import PrettyPrinter
# Env variables load and declaration
load_dotenv(find_dotenv())
mongo_pwd = os.environ.get('MONGODB_PWD')
# Global variables
printer = PrettyPrinter()
# Mongo connection
connection_string = f'mongodb+srv://WiktorB2004:{mongo_pwd}@data.g6nqmlw.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
# Database and questions collection
db = client.db
question = db.question

