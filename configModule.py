# module responsible of saving and serving config to the rest of program
import configparser
import logging
import os


class Config:

    def __init__(self, config_filename = 'config.ini'):
        # initializing config parser and checking if config file exist
        # if config file doesn't exist, create a new one
        # if file exist, read config
        self.config_filename = config_filename
        self.parser = configparser.ConfigParser()
        if not os.path.exists(self.config_filename):
            self.create_new_config()
        else:
            self.parser.read(self.config_filename)



    def create_new_config(self):
        # when there is no config file, this function is creating a new file with empty config
        self.parser['login'] = {'base_url': '',
                                'license_plate': '',
                                'password': ''}
        self.parser['server'] = {'sendinterval': '',
                                'locationinterval': ''}
        self.parser.write(open(self.config_filename, 'w'))

    def check_server_credentials(self):
        # looking if there is workable config
        if all([ values == '' for values in self.parser['login'].values()]):
            logging.info('No server connection configured')
            return False
        else:
            logging.debug('Config file have configuration for connection with server')
            return True

    def section_returner(self, section):
        # returning a dictionary of requested section
        return dict(self.parser.items(section))

    def get_config_from_server(self,config):
        # creating an object of API instance with login data from config.ini
        # after successful login get json and save it to config file
        self.parser['server'] = config
        self.parser.write(open(self.config_filename, 'w'))

    def get_config_from_local(self):
        if all([ values == '' for values in self.parser['server'].values()]):
            logging.info('No local configuration saved')
            return False
        else:
            logging.debug('Configuration from local')
            return True
    def return_send_interval(self):
        return self.parser['server']['sendinterval']
