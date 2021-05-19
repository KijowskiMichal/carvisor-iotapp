import json
import datetime

class Sender:

    def __init__(self, sendinterval):
        self.count_iteration = 0
        self.max_iterations = 3
        self.values = 3
        # self.max_iterations = int(sendinterval)
        self.internal_counter = 0
        self.data = {}
        self.data[self.count_iteration] = []
        self.names = {"12": "RPM","13": "Speed","17": "Throttle Pos"}

    def pack(self,value,name):
        self.data[self.count_iteration].append({self.names[str(name)]: value.value.magnitude})
        if self.internal_counter >=self.values-1:
            self.internal_counter=0
            self.count_iteration+=1
            if self.count_iteration == self.max_iterations:
                self.data['time'] = []
                self.prepare_to_send()
            else:
                self.data[self.count_iteration] = []
        else:
            self.internal_counter+=1

    def prepare_to_send(self):
        self.count_iteration=0
        self.data['time'].append({"time": (datetime.datetime.now() - datetime.timedelta(seconds=self.max_iterations)).timestamp()})
        data_prep = json.dumps(self.data)
        self.data = {}
        self.data[self.count_iteration] = []
        print(data_prep)
