import datetime
import logging

import requests
import json


class RequestAPI:

    def __init__(self, login_data,saver):
        # initialize variables with login data from config file
        self.base_url = login_data['base_url']
        self.saver = saver
        self.connection_retries_number = 3
        self.login_data = json.dumps({"licensePlate": login_data['license_plate'], 'password': login_data['password']})
        self.session = requests.Session()
        self.start_session_car()
        self.start_track()


    # def __del__(self):
    #     self.GET("API/carAuthorization/logout")

    def POST(self,url,data_to_send={}):
        req = requests.Request("POST", self.base_url + url, data=data_to_send)
        ready_request = self.session.prepare_request(req)
        try:
            request =  self.session.send(ready_request)
        except requests.exceptions.RequestException:
            print("ellol")
        return request

    def GET(self,url):
        return self.session.request("GET", self.base_url + url).json()


    def start_session_car(self):
        # starting new session with server
        for i in range(self.connection_retries_number):
            response = self.POST("API/carAuthorization/authorize",self.login_data)
            if response.status_code == 200:
                logging.debug("Device connected to server")
                break
            elif response.status_code == 406:
                logging.warning("Wrong licence plate or/and password in config file")
                break
            else:
                logging.warning("Server unreachable, error code: " + str(response.status_code))


    def send_obd_data(self, obd_data):
        response = self.POST("API/track/updateTrackData/",obd_data)
        print(obd_data)
        if response.status_code == 200:
            logging.debug("Sending obd data finished")
        else:
            print(response.content)
            # self.store_obd_data(obd_data)
            logging.warning("Problem occurred when sending obd data to server, error code: " + str(response.status_code))

    def start_track(self):
        start_data = json.dumps({ "nfc_tag":"AB", "time": datetime.datetime.now().timestamp(),"private": False, "gps_longitude":52.45726,"gps_latitude":16.92397})
        response = self.POST("API/track/start",start_data)
        if response.status_code == 200:
            logging.debug("Track started")
        elif response.status_code == 409:
            logging.debug("Track exist, working on existing track")
        else:
            logging.warning("Problem occurred while starting a new track: " + str(response.status_code))


    def check_authorization(self):
        return self.GET("API/carAuthorization/status")['logged']

    def get_config_from_server(self):
        return self.config

    def store_obd_data(self,data_to_save):
        self.saver.send_obd_data(data_to_save)
