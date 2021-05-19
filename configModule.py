# module responsible of saving and serving config to the rest of program
import configparser
import logging
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
            self.check_server_credentials()
            # self.get_config_from_server()

    def create_new_config(self):
        # when there is no config file, this function is creating a new file with empty config
        self.parser['login'] = {'base_url': '',
                                'license_plate': '',
                                'password': ''}
        self.parser['server'] = {'sendinterval': '',
                                'locationinterval': ''}
        self.parser.write(open('config.ini', 'w'))

    def check_server_credentials(self):
        if all([ v == '' for v in self.parser['login'].values()]):
            logging.info('No server connection configured')
            return False
        else:
            logging.debug('Config file have configured connection with server')

    def section_returner(self, section):
        # returning a dictionary of requested section
        return dict(self.parser.items(section))

    def get_config_from_server(self):
        # creating an object of API instance with login data from config.ini
        server_API_connection = RequestAPI(self.section_returner('login'))
        # after successful login get json and save it to config file
        if server_API_connection.check_authorization():
            self.parser['server'] = server_API_connection.get_config_from_server()
            self.parser.write(open('config.ini', 'w'))
            del(server_API_connection)
        else:
            pass

    def return_send_interval(self):
        return self.parser['server']['sendinterval']