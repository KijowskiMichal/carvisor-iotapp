import logging
from configModule import Config
from obdModule import ObdReader
from sendModule import Sender
import time

class CarVisor:

    def __init__(self):
        self.config = Config()
        self.API = self.config.return_API()
        self.send = Sender(self.config.return_send_interval(), self.API)
        self.obd = ObdReader(self.send)
        self.start_logging()
        self.start_obd_reading()


    def start_logging(self):
        logging.basicConfig(filename='carvisor.log',
                         encoding='utf-8',
                          format='%(asctime)s %(levelname)-6s %(message)s',
                           level=logging.DEBUG,
                           datefmt='%Y-%m-%d %H:%M:%S')

    def start_obd_reading(self):
        self.obd.start_read()
        while 1:
            time.sleep(10)

start = CarVisor()