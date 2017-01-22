from station.resources.config import * 
from station.sensor_packets.environment_sensor_packet import *

import json
import threading
from datetime import datetime
import time
from os import listdir
from os.path import isfile, join, dirname, abspath

import pytz
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread
import logging
import serial


class EnvironmentDataCollector(Thread):
    def __init__(self, sensor_node_id):
        Thread.__init__(self)
        self.sensor_node_id = sensor_node_id
        self.kafka_topic = 'weather'
        self.kafka_server = '{}:{}'.format(KAFKA_SERVER,KAFKA_PORT) 
        self.kafka_producer = KafkaProducer(bootstrap_servers=['{}:{}'.format(KAFKA_SERVER,KAFKA_PORT) ])

    def parse_data(self,str_response):
        data = [ tuple(x.lower().split('|')) for x in str_response.split('#')]
        parsed_data = dict(data)
        # adding time information
        parsed_data['time'] = datetime.now(pytz.timezone('Asia/Qatar')).strftime("%Y-%m-%d %H:%M:%S %Z")
        parsed_data['sensor_node_id'] = self.sensor_node_id
        return parsed_data



    def run(self):
        logging.info('Getting Data from Node {}'.format(self.sensor_node_id))
        connPi = serial.Serial(PORT, BAUD_RATE,  timeout=1)

        if connPi.isOpen():
            connPi.flushInput()
            connPi.flushOutput()
            time.sleep(10)

            while True:
                try: 
                    str_response = connPi.readline()
                    # sanity check 
                    if '#' in str_response:

                        parsed_data = self.parse_data(str_response)
                        
                        # Send data to Kafka 
                        self.kafka_producer.send(self.kafka_topic, EnvironmentSensorPacket(parsed_data).to_json())

                except Exception, e:
                    raise e
                    pass
        else:
            logging.warn("Can\'t connect to RaspberyPi ")



