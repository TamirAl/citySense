import json


class BluetoothSensorPacket:
	def __init__(self, sensor_packet):
		self.sensor_id = sensor_packet.get('sensor_node_id',None)
		self.timestamp = sensor_packet.get('time',None)
		self.device_name = sensor_packet.get('device_name',None)
		self.device_addr = sensor_packet.get('device_addr',None)

	def __str__(self):
		return "Sensor: {} | Bluetooth Device: {}".format(self.sensor_id,self.device_name)

   	def to_json(self):
		data = {"sensor_id":self.sensor_id, "timestamp": self.timestamp, "device_name": self.device_name , "device_addr": self.device_addr }
		return json.dumps(data).encode('utf-8')





