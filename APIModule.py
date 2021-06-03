import datetime
import logging
import asyncio
import requests
import json

class RequestAPI:

    def __init__(self, login_data,saver,gps):
        # initialize variables with login data from config file
        self.gps = gps
        self.base_url = login_data['base_url']
        self.saver = saver
        self.connection_retries_number = 3
        self.login_data = json.dumps({"licensePlate": login_data['license_plate'], 'password': login_data['password']})
        self.create_own_response()
        self.session = requests.Session()
        self.start_session_car()

    def POST(self,url,data_to_send={}):
        req = requests.Request("POST", self.base_url + url, data=data_to_send)
        ready_request = self.session.prepare_request(req)
        try:
            request =  self.session.send(ready_request)
        except requests.exceptions.RequestException:
            return self.failure_response
        return request

    def GET(self,url):
        try:
            request = self.session.request("GET", self.base_url + url)
        except requests.exceptions.RequestException:
            return self.failure_response
        return request


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
        # self.store_obd_data(obd_data)

        response = self.POST("API/track/updateTrackData/",json.dumps(obd_data))
        print(datetime.datetime.now())
        if response.status_code == 200:
            logging.debug("Sending obd data finished")
            asyncio.run(self.start_sending_from_db())
        else:
            self.store_obd_data(obd_data)
            logging.warning("Problem occurred when sending obd data to server, error code: " + str(response.status_code))

    def send_saved_data(self, obd_data):
        response = self.POST("API/track/updateTrackData/",json.dumps(obd_data))
        if response.status_code == 200:
            logging.debug("Sending obd data finished")
            return True
        else:
            logging.warning("Problem occurred when sending obd data to server, error code: " + str(response.status_code))
            return False

    def start_track(self):
        gps_pos = self.gps.get_only_position_values()
        start_data = json.dumps({ "nfc_tag":"ABB", "time": datetime.datetime.now().strftime("%s"),"private": False, "gps_longitude":gps_pos[0],"gps_latitude":gps_pos[1]})
        for i in range(self.connection_retries_number):
            response = self.POST("API/track/start",start_data)
            if response.status_code == 200:
                logging.debug("Track started")
                break
            elif response.status_code == 409:
                logging.debug("Track exist, working on existing track")
                break
            else:
                logging.warning("Problem occurred while starting a new track: " + str(response.status_code))


    def check_authorization(self):
        response = self.GET("API/carAuthorization/status")
        if response.status_code == 200:
            logging.debug("Track started")
            return response.json()["logged"]
        elif response.status_code == 409:
            logging.debug("Track exist, working on existing track")
            return False
        else:
            logging.warning("Problem occurred while starting a new track: " + str(response.status_code))
            return False

    def get_config_from_server(self):
        return self.config

    def store_obd_data(self,data_to_save):
        self.saver.send_obd_data(data_to_save)

    def create_own_response(self):
        self.failure_response = requests.models.Response()
        self.failure_response.code = "expired"
        self.failure_response.error_type = "expired"
        self.failure_response.status_code = 400

    async def start_sending_from_db(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.saver.send_payload())
        loop.close()
