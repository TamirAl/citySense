import logging
from station.data_processor.consumer import DataFetcher
from station.data_collector.wifi_sniffer import WifiSniffer
from station.data_collector.environment_data_collector import EnvironmentDataCollector
from station.data_collector.bluetooth_sniffer import BluetoothSniffer


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # when you come back try Wifi sniffer and bluetooth sniffer
    threads = [BluetoothSniffer(1), EnvironmentDataCollector(
        1), WifiSniffer(1), DataFetcher()]

    for thread in threads:
        thread.start()
