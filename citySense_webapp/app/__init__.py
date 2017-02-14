import os
from flask import Flask,render_template
from pymongo import MongoClient
import time
import yaml
from datetime import datetime
from app.db_connector.db_connector import DBConnector

# Current Location
current_loc = os.path.join(os.path.dirname( __file__ ), 'config' )

# Configuration files
MONGO_DB_CONFIG = yaml.load(open("{}/{}".format(current_loc, "/db.yml") ))

# # Connect to MongoDb 
# db_connector = DBConnector(MONGO_DB_CONFIG)
# environment_collection = db_connector.connect_to_collection(MONGO_DB_CONFIG['collections']['environment'])
# wifidevices_collection = db_connector.connect_to_collection(MONGO_DB_CONFIG['collections']['wifidevices'])


app = Flask(__name__)

from app import views

