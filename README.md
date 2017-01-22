![MIT license](https://img.shields.io/badge/licence-MIT-blue.svg)

# citySense

citySense is an urban IoT sensing platform, that allows researchers to collect, analyze and visualize real-time data on the city's infrastructure and citizens' activity (with respect to their privacy). 

## What is citySense ? 
The system consists of a IoT sensor nodes placed on streetlight poles and connected to the network. Each IoT node is geographically localized, so that IoT data can be enhanced with context information.

The system is powered by a network of modular IoT sensor nodes (that can be placed on streetlight poles). Each IoT node consists of a set of sensors to sense the pulse of the city. The collected data will be stored in a centralized database, and can be visualized through a map-centeric dashboard. 

In every IoT sensor node, an Arduino (Nano) connected to the Raspberry Pi via USB, is used with a set of sensors to monitor temperature, humidity, carbon monoxide (CO), sound, solar radiation, Bluetooth signals, Wi-Fi hotspots, and battery charge level. The Arduino is powerd through the USB socket and uses the built in USB-to-serial connection to communicate with the Raspberry Pi.

Each station is configured to fetch and pull data to a database. The data is stored in a NoSQL-database (MongoDB), that can be installed on a local or remote server. 

In order to reduce data storage, data is only stored in configurable time interval.  

![ScreenShot](/docs/images/city_sense.png)

## The Hardware prototype
![ScreenShot](/docs/images/citysense_node.png)

## Circuit Diagram 
The full schematic of our completed prototype will look like the following:
![ScreenShot](/docs/images/arduino_circuit_diagram.png)

## Code Structure  
    +- citySense IoT Platform 
    |  +- citySens_nodee: Urban IoT Node
    |  |  +- Station
    |  |  | +- Data Collector
    |  |  | +- Data Processor  
    |  |  +- Arduino 
    |  |  | +- Humidity 
    |  |  | +- Light
    |  |  | +- Rain
    |  |  | +- CO2
    |  |  | +- Noise
    |  |  | +- Camera Monitoring
    |  |  | +- Bluetooth Occupancy Sensing 
    |  |  | +- Wifi Occupancy Sensing 
    |  |  +- 3D Sketch: 3d package design  
    |  +- citySense: Dashboard
    |  +- citySense: Restful API

## Getting Started 
### Remote Server 
- Install mongo database on a server 
```sh
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start
```
- Add server ip address for each node and update Configuration file 

### citySense-Node

- SSH to a connected Raspberry Pi
- Install the required packages (Kafka,scappy .. etc)
```sh
ssh install/install.sh 
```
- Clone github repository
```sh
git clone https://github.com/tzano/pyosio.git
```
- Open new screen, so you can keep the script running on the background. 
```sh
Screen -S citysense
```
- Set up a virtual environment
```sh
virtualenv env
source env/bin/activate
```
- Install the required modules using the requirements.txt. 
```sh
pip install -r requirements.txt
```
- Connect Arduino with your Mac/PC
- Move to arduino sketch folder
```sh
cd citySense_node/arduino_sketch/  
```
- Connect your Arduino using the USB cable.
- Using Arduino IDE, Choose Tools?Board?Arduino Uno to find your board in the Arduino menu. 
- Choose the correct serial port for your board.
- Click the Upload button.
- If you see arduino blinking, it means that you loaded it.
- Connect your Arduino with your Raspberry-Pi
- Run the script run_node_listener.py
```sh
python run_node_listener.py 
```
- At this point, you can disconnect from the Pi. You can use (CRT + D) to leave the screen. 
- Place the station with access to the WIFI, and it will start collecting data. 
- For more convinient, you can use startup script to start data collection automatically without a need to any other interface. The pi can run the script on startup mode. 

## Support
If you are having issues, please let us know or submit a pull request.

## License
The project is licensed under the MIT License.




