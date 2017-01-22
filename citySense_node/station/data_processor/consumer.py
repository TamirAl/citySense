import logging, time, json,pymongo
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from threading import Thread


class DataFetcher(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.kafka_consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest')


    def run(self):

        #self.kafka_consumer.subscribe(['weather'])
        self.kafka_consumer.subscribe(['bluetooth'])
        for message in self.kafka_consumer:
            print (message)

