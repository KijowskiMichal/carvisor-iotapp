import logging
import time

from configModule import Config
from obdModule import ObdReader
from sendModule import Sender
from APIModule import RequestAPI
from savingModule import Saver

class CarVisor:

    def __init__(self):
        self.start_logging()
        self.config = Config()
        if self.config.check_server_credentials():
            self.saver = Saver()
            self.API = RequestAPI(self.config.section_returner('login'),self.saver)
            if self.API.check_authorization():
                # everything is fine, IoT can send data to server
                self.saver.get_API(self.API)
            else:
                # problem with authorization, sending to local storage
                self.server_unreachable_handler()
        else:
            # no config to login to server
            self.server_unreachable_handler()
        self.send = Sender(self.config.return_send_interval(), self.API)
        self.init_obd()

    def start_logging(self):
        logging.basicConfig(filename='carvisor.log',
                          format='%(asctime)s %(levelname)-6s %(message)s',
                           level=logging.WARNING,
                           datefmt='%Y-%m-%d %H:%M:%S')
    def init_obd(self):
        self.obd = ObdReader(self.send)
        while not self.obd.check_connection():
            time.sleep(5)
            self.obd = ObdReader(self.send)
        self.start_obd_reading()

    def start_obd_reading(self):
        self.obd.start_read()
        input("Rozpoczęto odczyt OBD.\n")

    def server_unreachable_handler(self):
        self.API = Saver()
        del (self.saver)

start = CarVisor()