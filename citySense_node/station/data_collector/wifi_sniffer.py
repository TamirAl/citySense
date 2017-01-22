from station.resources.config import *
from station.sensor_packets.wifi_sensor_packet import *
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread
from scapy.all import *
from datetime import datetime
import json
import time
import pytz
from subprocess import Popen, call, PIPE
import csv
import logging


class WifiSniffer(Thread):
    def __init__(self, sensor_node_id):
        Thread.__init__(self)
        self.sensor_node_id = sensor_node_id
        self.kafka_topic = 'wifi'
        self.kafka_server = '{}:{}'.format(KAFKA_SERVER,KAFKA_PORT)
        self.kafka_producer = KafkaProducer(bootstrap_servers=['{}:{}'.format(KAFKA_SERVER,KAFKA_PORT) ])


    def start_monitor_mode(self):
        call("sudo airmon-ng stop wlan0mon", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        call("sudo airmon-ng start wlan0 1", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)


    def sniff_airmon(self):
        self.start_monitor_mode()
        output_fname = "output_airodump"
        # setup airodump on a timer
        p = Popen("sudo airodump-ng wlan0mon -o csv -w {}".format(output_fname), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

        with open(output_fname+'-01.csv') as f:
            reader = csv.reader(f)
            columns = ['bssid', 'first_seen', 'last_seen', 'channel', 'speed', 'privacy', 'cipher', 'authentication', 'power', 'beacons', 'ivs', 'lan', 'id-length', 'essid', 'key']
            result = [(columns[i], re.sub('[\s]+$', '', re.sub('^[\s]+', '', row[i]))) for i,row in enumerate(reader)]
        return result

    def scan_packets(self,packet):
        if packet.haslayer(Dot11):
            if packet.type == PROBE_REQUEST_TYPE and packet.subtype == PROBE_REQUEST_SUBTYPE :
                parsed_data = self.parse_data(packet)
                # send data to Kafka
                self.kafka_producer.send(self.kafka_topic, WIFISensorPacket(parsed_data).to_json())


    def get_signal_strength(self,p):
        try:
            e = p.notdecoded
        except:
            e = None
        if e!=None:
            return -(256-ord(e[-4:-3]))
        else:
            #"No signal strength found"
            return -100


    def parse_data(self,packet):
        if (self.get_signal_strength(packet) == -256 ):
            rssi =  0
        else:
            rssi = self.get_signal_strength(packet)

        mac  =   packet.addr2
        target =  packet.addr3
        # minimize any potential collection of data about individuals
        device_data = {"target": hash(target),"mac": hash(mac) , "ssid": hash(packet.getlayer(Dot11ProbeReq).info) , "rssi": hash(rssi)}
        device_data['time'] = datetime.now(pytz.timezone('Asia/Qatar')).strftime("%Y-%m-%d %H:%M:%S %Z")
        device_data['sensor_node_id'] = self.sensor_node_id
        return device_data


    def sniff_devices(self):
        # Enable Monitor Mode
        self.start_monitor_mode()
        # Start Sniffing
        sniff(iface=MONITOR_INTERFACE,prn=self.scan_packets)



    def run(self):
        logging.info('Running WIFI Sniffer from Node {}'.format(self.sensor_node_id))
        self.sniff_devices()
