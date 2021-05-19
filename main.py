import logging
from configModule import Config
from obdModule import ObdReader
from sendModule import Sender
import time

logging.basicConfig(filename='carvisor.log',
                    encoding='utf-8',
                    format='%(asctime)s %(levelname)-6s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
config = Config()
send = Sender(config.return_send_interval())
obd = ObdReader(send)
obd.start_read()
while 1:
    time.sleep(10)