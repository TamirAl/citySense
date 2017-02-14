import logging
from station.data_processor.consumer import DataFetcher
from station.data_collector.wifi_sniffer import WifiSniffer
from station.data_collector.environment_data_collector import EnvironmentDataCollector
from station.data_collector.bluetooth_sniffer import BluetoothSniffer
from station.db_connector.db_connector import DBConnector
from station.resources.config import *

import os


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

	# Current Location
	current_loc = os.path.join(os.path.dirname( __file__ ), 'config' )


	# Connect to MongoDb 
	db_connector = DBConnector({"host": MONGODB_HOST, "port": MONGODB_PORT, "db_name": DBS_NAME})
	environment_collection = db_connector.connect_to_collection(COLLECTION_ENVIRONMENT)
	wifidevices_collection = db_connector.connect_to_collection(COLLECTION_WIFIDEVICES)
	bltdevices_collection = db_connector.connect_to_collection(COLLECTION_BLTDEVICES)


    # when you come back try Wifi sniffer and bluetooth sniffer
    threads = [BluetoothSniffer(1, "bltdevices"), EnvironmentDataCollector(
        1, "environment"), WifiSniffer(1, "wifidevices"), DataFetcher(environment_collection,"environment"), DataFetcher(wifidevices_collection,"wifidevices"), DataFetcher(bltdevices_collection,"bltdevices")]

    for thread in threads:
        thread.start()


