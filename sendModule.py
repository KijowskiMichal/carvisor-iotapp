import json
import datetime

class Sender:

    def __init__(self, sendinterval,API):
        self.count_iteration = 0
        self.max_iterations = 3
        self.values = 3
        # self.max_iterations = int(sendinterval)
        self.internal_counter = 0
        self.data = {}
        self.API = API
        self.actual_time = datetime.datetime.now().timestamp()
        self.data[self.actual_time] = {}
        self.names = {"12": "RPM","13": "Speed","17": "Throttle Pos"}
        self.longitude = 52.45726
        self.latitude = 16.92397

    def pack(self,value,name):
        # assign value from obd to dict
        try:
            self.data[self.actual_time][self.names[str(name)]] = value.value.magnitude
        except AttributeError:
            self.data[self.actual_time][self.names[str(name)]] = 0
        if len(self.data[self.actual_time]) >= self.values-1:
            self.gpsdata(self.data[self.actual_time])
            self.get_time_to_iteration()
            if len(self.data) >= self.max_iterations:
                self.prepare_to_send()
            else:
                self.data[self.actual_time] = {}

    def gpsdata(self,iteration):
        #generating fake gps data
        iteration['gps_longitude'] = ("%.5f" % self.longitude)
        iteration['gps_latitude'] = ("%.5f" % self.latitude)
        self.latitude -= 0.00060

    def prepare_to_send(self):
        data_prep = self.data
        self.data = {}
        self.get_time_to_iteration()
        self.data[self.actual_time] = {}
        self.API.send_obd_data(data_prep)
        # print(data_prep)

    def write_manually(self, data_to_write):
        self.data = data_to_write

    def print_data(self):
        return self.data

    def get_time_to_iteration(self):
        self.actual_time = datetime.datetime.now().timestamp()