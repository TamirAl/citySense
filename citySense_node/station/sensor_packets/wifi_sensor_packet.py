import json



class WIFISensorPacket:
    def __init__(self,sensor_packet):
        self.sensor_id = sensor_packet.get('sensor_node_id',None)
        self.timestamp = sensor_packet.get('timestamp',None)
        self.target = sensor_packet.get('target',None)
        self.mac = sensor_packet.get('mac',None)
        self.ssid = sensor_packet.get('ssid',None)
        self.rssi = sensor_packet.get('rssi',None)

    def __str__(self):
        return "Sensor: {} | Target: {} | Mac: {} | SSID: {} | RSSI: {} ".format(self.sensor_id,self.target,self.mac,self.ssid,self.rssi)

    def to_json(self):
        data = {"sensor_id":self.sensor_id, "timestamp":self.timestamp,"target":self.target,"mac":self.mac,"ssid":self.ssid,"rssi":self.rssi}
        return json.dumps(data).encode('utf-8')
