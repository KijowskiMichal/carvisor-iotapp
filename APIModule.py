import requests
import json


class RequestAPI:

    def __init__(self, login_data):
        self.session = requests.Session()
        self.base_url = login_data['base_url']
        self.login_data = json.dumps({"licensePlate": login_data['license_plate'], 'password': login_data['password']})
        self.start_session()
        if self.check_authorization():
            self.get_config_from_server()
        else:
            print("Something went wrong")

    def start_session(self):
        req = requests.Request("POST", self.base_url + "API/carAuthorization/authorize", data=self.login_data)
        ready_request = self.session.prepare_request(req)
        response = self.session.send(ready_request)
        if response.status_code == 200:
            print("Device connected to server")
        else:
            print("Server unreachable, error code: " + str(response.status_code))
            if response.status_code == 406:
                print("Wrong licence plate or/and password")

    def check_authorization(self):
        check_request = self.session.request("GET", self.base_url + "API/carAuthorization/status")
        return check_request.json()['logged']

    def get_config_from_server(self):
        config_from_server = self.session.request("POST", self.base_url + "API/carConfiguration/get")
        return config_from_server.json()

    def logout(self):
        # sending request to server to end a session
        self.session.request("GET", self.base_url + "API/carAuthorization/logout")
