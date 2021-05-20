import json
import datetime

class Sender:

    def __init__(self, sendinterval, API):
        self.count_iteration = 0
        # self.max_iterations = 3
        self.values = 3
        self.max_iterations = int(sendinterval)
        self.internal_counter = 0
        self.data = {}
        self.API = API
        self.data[self.count_iteration] = {}
        self.names = {"12": "RPM","13": "Speed","17": "Throttle Pos"}
        self.longitude = 52.45726
        self.latitude = 16.92397
        self.speedc= 0
        self.rpmc= 0


    def pack(self,value,name):
        self.data[self.count_iteration][self.names[str(name)]] = value.value.magnitude
        if self.names[str(name)] =="Speed":
            self.speedc+=int(value.value.magnitude)
        if self.names[str(name)] =="RPM":
            self.rpmc+=int(value.value.magnitude)
        if self.internal_counter >=self.values-1:
            self.gpsdata(self.data[self.count_iteration])
            self.internal_counter=0
            self.count_iteration+=1
            if self.count_iteration == self.max_iterations:
                self.prepare_to_send()
            else:
                self.data[self.count_iteration] = {}
        else:
            self.internal_counter+=1

    def gpsdata(self,iteration):
        iteration['gps_longitude'] = ("%.5f" % self.longitude)
        iteration['gps_latitude'] = ("%.5f" % self.latitude)
        self.latitude -= 0.00060

    def prepare_to_send(self):
        self.count_iteration=0
        self.data['time'] = {"time": (datetime.datetime.now() - datetime.timedelta(seconds=self.max_iterations)).timestamp()}
        data_prep = json.dumps(self.data)
        self.data = {}
        self.data[self.count_iteration] = {}
        self.API.send_data_to_server(data_prep)
