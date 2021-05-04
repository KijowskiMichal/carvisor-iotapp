# module responsible of saving and serving config to the rest of program
import configparser
import os
from APIModule import RequestAPI


class Config:

    def __init__(self):
        # initializing config parser and checking if config file exist
        # if config file doesn't exist, create a new one
        # if file exist, read config
        self.parser = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            self.create_new_config()
        else:
            self.parser.read('config.ini')
            self.get_config_from_server()

    def create_new_config(self):
        self.parser['login'] = {'base_url': '',
                                'license_plate': '',
                                'password': ''}
        self.parser.write(open('config.ini', 'w'))


    def section_returner(self, section):
        return dict(self.parser.items(section))

    def get_config_from_server(self):
        self.server_API_connection = RequestAPI(self.section_returner('login'))
        if self.server_API_connection.check_authorization():
            self.parser['work'] = self.server_API_connection.get_config_from_server()
            self.parser.write(open('config.ini', 'w'))
        else:
            pass
