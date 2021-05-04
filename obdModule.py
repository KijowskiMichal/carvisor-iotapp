import obd
import time


class ObdReader:

    def __init__(self):
        self.connection = obd.Async('/dev/pts/1', fast=False)

    # update value of
    def new_value(self,r):
        print(r.value)

    def logging(self):
        obd.logger.setLevel(obd.logging.DEBUG)

    def start_read(self):
        # connecting to OBD module and
        # commands = connection.supported_commands
        # for i in commands:
        #     print(i)
        # resp = obd.commands.GET_DTC
        # print(self.connection.query(obd.commands.GET_DTC))
        self.connection.watch(obd.commands[1][12], callback=self.new_value)
        self.connection.watch(obd.commands[1][13], callback=self.new_value)
        self.connection.start()


