# -------------------------- #
# RPI-Arduino Connectivity 
# -------------------------- #
PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# -------------------------- #
# Kafka 
# -------------------------- #
KAFKA_SERVER = 'localhost'
KAFKA_PORT = 9092
# -------------------------- #
# Mongodb 
# -------------------------- #
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_SERVER = 'mongodb://'
DBS_NAME = ""
COLLECTION_WIFIDEVICES = ""
COLLECTION_WEATHER = ""
COLLECTION_BLTDEVICES = "" 
MONITOR_INTERFACE = ""

# ----------------------------- #
# Configuration for WIFI Sniffer
# ----------------------------- #
NODE_NBR = 1
PROBE_REQUEST_TYPE=0
# wlan.fc.type_subtype == 4   Probe request
# wlan.fc.type_subtype == 5   Probe response
# wlan.fc.type_subtype == 8   Beacon

PROBE_REQUEST_SUBTYPE=4


WHITELIST = [] 


# ----------------------------- #
# Configuration for Bluetooth Sniffer
# ----------------------------- #
SLEEP_TIME = 60