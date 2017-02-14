from station.resources.config import *
from station.sensor_packets.bluetooth_sensor_packet import *
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread
from datetime import datetime
import json
import time
import pytz
from subprocess import Popen, call, PIPE
import csv
import logging



class BluetoothSniffer(Thread):
    def __init__(self, sensor_node_id, kafka_topic= 'bluetooth'):
        Thread.__init__(self)
        self.sensor_node_id = sensor_node_id
        self.kafka_topic = kafka_topic
        self.kafka_server = '{}:{}'.format(KAFKA_SERVER,KAFKA_PORT)
        #self.kafka_producer = KafkaProducer(bootstrap_servers=['{}:{}'.format(KAFKA_SERVER,KAFKA_PORT) ])


    def start_monitor_mode(self):
        # Force Bluetooth device to restart
        call(["sudo","hcitool","dev"])
        call(["sudo","hciconfig","hci0","down"])
        call(["sudo","hciconfig","hci0","up"])
        # Scan bluetooth the devices 
        cmd_scan = "hcitool scan --info --class --flush"
        output, error = Popen(cmd_scan.split(),stdout=PIPE,stderr=PIPE).communicate()

        return output, error

    def parse_data(self,line):
        lines = line.strip("\n")
        device_name = lines.split(' ',1)[1]
        device_addr = lines.split(' ')[0]
        timestamp = time.now()

        device_data = {'timestamp': timestamp , 'device_name':device_name,  'device_addr': device_addr }
        device_data['time'] = datetime.now(pytz.timezone('Asia/Qatar')).strftime("%Y-%m-%d %H:%M:%S %Z")
        device_data['sensor_node_id'] = self.sensor_node_id

        return device_data

    def run(self):
        logging.info('Running Bluetooth Sniffer from Node {}'.format(self.sensor_node_id))
        
        try:
            while True:

                output, error = self.start_monitor_mode()
                for packet in output[0].split('\n\n')[1:-1]:
                    parsed_data = self.parse_data(packet)
                    self.kafka_producer.send(self.kafka_topic, BluetoothSensorPacket(parsed_data).to_json())

                #time.sleep(10)
        
        except Exception, e:
            raise e



