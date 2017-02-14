import logging, time, json,pymongo
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from threading import Thread
import json

class DataFetcher(Thread):

    def __init__(self):
        Thread.__init__(self, mongo_db, topic)
        self.kafka_consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest')
        self.mongo_db = mongo_db
        self.topic = topic


    def run(self):
        self.kafka_consumer.subscribe(self.topic)
        for message in self.kafka_consumer:
            self.mongo_db.insert(json.load(message))

