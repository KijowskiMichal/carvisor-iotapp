import json
import datetime
import re


class Sender:

    def __init__(self, sendinterval, API):
        self.count_iteration = 0
        self.max_iterations = 3
        self.values = 3
        self.internal_counter = 0
        # self.max_iterations = int(sendinterval)
        self.data = {}
        self.API = API
        self.new_iteration()
        self.longitude = 52.45726
        self.latitude = 16.92397

    def pack(self, value, name):
        name = str(name)
        try:
            # self.check_if_value_exist(name)
            self.data[self.timestamp]["obd"][name] = float("%.2f" % value.value.magnitude)
        except AttributeError:
            # self.check_if_value_exist(name)
            self.data[self.timestamp]["obd"][name] = 0
        if self.internal_counter >= self.values - 1:
            self.gpsdata(self.data[self.timestamp])
            self.internal_counter = 0
            self.count_iteration += 1
            if self.count_iteration == self.max_iterations:
                self.prepare_to_send()
            else:
                self.new_iteration()
        else:
            self.internal_counter += 1

    def gpsdata(self, iteration):
        # generating fake gps data
        location_file = open("location",'r').readlines()[-2]
        gps_real = re.findall('[0-9]*[\.]{1}[0-9]*',location_file)
        iteration['gps_pos'] = {'longitude': float("%.5f" % float(gps_real[0])), "latitude": float("%.5f" % float(gps_real[1]))}
        self.latitude -= 0.00005

    def prepare_to_send(self):
        self.count_iteration = 0
        data_prep = self.data
        self.data = {}
        self.new_iteration()
        self.API.send_obd_data(json.dumps(data_prep))
        # print(json.dumps(data_prep))

    def get_new_timestamp(self):
        self.timestamp = datetime.datetime.now().strftime("%s")

    def new_iteration(self):
        self.get_new_timestamp()
        self.data[self.timestamp] = {}
        self.data[self.timestamp]["obd"] = {}

    def check_if_value_exist(self, name):
        if name in self.data[self.timestamp]["obd"].keys():
            self.gpsdata(self.data[self.timestamp])
            self.check_number_of_iterations()
            self.new_iteration()
            self.count_iteration += 1

    def check_number_of_iterations(self):
        if self.count_iteration >= self.max_iterations:
            self.prepare_to_send()

    # Functions for testing purposes
    def write_manually(self, data_to_write):
        self.data = data_to_write

    def print_data(self):
        return self.data
