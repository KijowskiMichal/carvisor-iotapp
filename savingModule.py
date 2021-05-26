from tinydb import TinyDB, Query


class Saver:

    def __init__(self):
        self.db = TinyDB('obd_data.json')

    def send_obd_data(self, obd_data):
        self.db.insert(obd_data)

    def get_all_data(self):
        for item in self.db:
            print(item)

    def get_API(self,API):
        self.API = API
