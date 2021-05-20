import obd
import time


class ObdReader:

    def __init__(self,send):
        # self.logging()
        self.connection = obd.Async('/dev/pts/1', fast=False, delay_cmds=1)
        self.commands_watching = [obd.commands.RPM,obd.commands.SPEED,obd.commands.THROTTLE_POS]
        self.sender = send


    def logging(self):
        obd.logger.setLevel(obd.logging.DEBUG)

    def start_read(self):
        # connecting to OBD module and
        for i in self.commands_watching:
            self.connection.watch(i, callback=self.sender.pack)
        self.connection.start()

    def check_DTC_codes(self):
        dtc_codes = self.connection.query(obd.commands.GET_DTC)
        if str(dtc_codes) == "None":
            print("No DTC codes")
        else:
            print(dtc_codes)

    def check_supported_commands(self):
        #checking which commands are supported by obd
        commands = self.connection.supported_commands
        for i in commands:
            print(i)

