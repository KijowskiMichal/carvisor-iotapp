import logging

import requests
import json


class RequestAPI:

    def __init__(self, login_data):
        # initialize variables with login data from config file
        self.base_url = login_data['base_url']
        self.login_data = json.dumps({"licensePlate": login_data['license_plate'], 'password': login_data['password']})
        self.session = requests.Session()
        self.start_session()
        if self.check_authorization():
            self.get_config_from_server()
            # self.start_track()
        else:
            logging.warning("Something went wrong with authorization")

    def __del__(self):
        self.logout()

    def start_session(self):
        # starting new session with server
        req = requests.Request("POST", self.base_url + "API/carAuthorization/authorize", data=self.login_data)
        ready_request = self.session.prepare_request(req)
        response = self.session.send(ready_request)
        if response.status_code == 200:
            logging.debug("Device connected to server")
        else:
            logging.warning("Server unreachable, error code: " + str(response.status_code))
            if response.status_code == 406:
                logging.warning("Wrong licence plate or/and password in config file")

    def check_authorization(self):
        check_request = self.session.request("GET", self.base_url + "API/carAuthorization/status")
        return check_request.json()['logged']

    def get_config_from_server(self):
        config_from_server = self.session.request("GET", self.base_url + "API/carConfiguration/get/")
        return config_from_server.json()

    def send_data_to_server(self,obd_data):
        # starting new session with server
        req = requests.Request("POST", self.base_url + "API/track/updateTrack/", data=obd_data)
        ready_request = self.session.prepare_request(req)
        response = self.session.send(ready_request)
        if response.status_code == 200:
            logging.debug("Sending obd data finished")
        else:
            logging.warning("Problem occurred when sending obd data to server, error code: " + str(response.status_code))

    def start_track(self):
        req = requests.Request("POST", self.base_url + "API/track/start/")
        ready_request = self.session.prepare_request(req)
        response = self.session.send(ready_request)
        if response.status_code == 200:
            logging.debug("Track started")
        else:
            logging.warning("Problem occurred while starting a new track: " + str(response.status_code))

    def logout(self):
        # sending request to server to end a session
        self.session.request("GET", self.base_url + "API/carAuthorization/logout")
