import json
import pymongo
from pymongo import MongoClient, errors
import logging

class DBConnector:
	
    def __init__(self,config_file):
    	self.config = config_file
        self.host = self.config["host"]
        self.port = self.config["port"]
        self.db_name = self.config["db_name"]
        self.connection =  MongoClient(self.host, self.port)

    def connect(self):

		try:
		    self.connection = MongoClient(self.host, self.port,connect=False)
		except errors.ConnectionFailure, e:
		    logging.warn('%s : Connection Problem!', self.db_name)

		return self.connection

    def connect_to_collection(self,collection_name ):
		try:
		    connection = MongoClient(self.host, self.port)
		    records = connection[self.config["db_name"]][collection_name]
		except errors.ConnectionFailure, e:
		    logging.warn('%s : Connection Problem!', self.config["db_name"])
		    records = None

		return records
