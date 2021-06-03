import json
import datetime
import re


class Sender:

    def __init__(self, sendinterval, API,gps):
        self.count_iteration = 0
        self.max_iterations = 3
        self.values = 4
        self.internal_counter = 0
        # self.max_iterations = int(sendinterval)
        self.data = {}
        self.gps = gps
        self.API = API
        self.new_iteration()

    def pack(self, value, name):
        name = str(name)
        try:
            # self.check_if_value_exist(name)
            self.data[self.timestamp]["obd"][name] = float("%.2f" % value.value.magnitude)
        except AttributeError:
            # self.check_if_value_exist(name)
            self.data[self.timestamp]["obd"][name] = 0
        if self.internal_counter >= self.values - 1:
            self.data[self.timestamp]["gps_pos"] = self.gps.get_position()
            self.internal_counter = 0
            self.count_iteration += 1
            if self.count_iteration == self.max_iterations:
                self.prepare_to_send()
            else:
                self.new_iteration()
        else:
            self.internal_counter += 1

    def prepare_to_send(self):
        # clearing variables for next pack of data and sending collected data to API Module to send to server
        self.count_iteration = 0
        data_prep = self.data
        self.data = {}
        self.new_iteration()
        self.API.send_obd_data(data_prep)

    def get_new_timestamp(self):
        # getting new timestamp for naming next iteration of data
        self.timestamp = datetime.datetime.now().strftime("%s")

    def new_iteration(self):
        self.get_new_timestamp()
        self.data[self.timestamp] = {}
        self.data[self.timestamp]["obd"] = {}


    # Functions for testing purposes
    def write_manually(self, data_to_write):
        self.data = data_to_write

    def print_data(self):
        return self.data
