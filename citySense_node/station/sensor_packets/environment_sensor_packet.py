import json

class EnvironmentSensorPacket:
    def __init__(self,sensor_packet):
        self.sensor_id = sensor_packet.get('battery_capacity', None)
        self.timestamp = sensor_packet.get('time', None)
        self.humidity = sensor_packet.get('humidity', None)
        self.temperature = sensor_packet.get('temperature', None)
        self.pressure = sensor_packet.get('pressure', None)
        self.light_level = sensor_packet.get('light', None)
        self.co2 = sensor_packet.get('co2', None)
        self.noise = sensor_packet.get('noise', None)
        self.location = {"latitude": 25.29, "longitude": 51.53} #sensor_packet.get('location', None) 
        self.battery_capacity = sensor_packet.get('volts', None)
        
    def __str__(self):
        return "Sensor: {} | Humidity: {} | Temperature: {} | Pressure: {} | Light level: {} | Battery capacity: {} | CO2: {} | Location: ({},{}) | Noise: {} ".format(self.sensor_id,self.humidity,self.temperature, self.pressure,self.light_level ,self.battery_capacity, self.co2, self.location.get("latitude",None), self.location.get("longitude",None) , self.noise )

    def to_json(self):
        data = {"sensor_id":self.sensor_id, "timestamp":self.timestamp,"humidity":self.humidity,"temperature":self.temperature,"pressure":self.pressure,"light":self.light_level,"co2":self.co2, "location":self.location, "battery_capacity":self.battery_capacity, "noise": self.noise}
        return json.dumps(data).encode('utf-8')



