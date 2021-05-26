import unittest
from configModule import Config
from sendModule import Sender

class CarVisor_test(unittest.TestCase):

    def test_sending(self):
        data = {"0": {"RPM": 1236.0, "Speed": 0.0, "Throttle Pos": 5.882352941176471, "gps_longitude": "52.45726", "gps_latitude": "16.90597", "time": {"time": 1621537473.529005}}, "1": {"RPM": 963.0, "Speed": 3.0, "Throttle Pos": 0.39215686274509803, "gps_longitude": "52.45726", "gps_latitude": "16.90537", "time": {"time": 1621537474.799595}}, "2": {"RPM": 823.0, "Speed": 5.0, "Throttle Pos": 1.9607843137254901, "gps_longitude": "52.45726", "gps_latitude": "16.90477", "time": {"time": 1621537476.068971}}, "3": {"RPM": 925.0, "Speed": 7.0, "Throttle Pos": 3.5294117647058822, "gps_longitude": "52.45726", "gps_latitude": "16.90417", "time": {"time": 1621537477.338757}}, "4": {"RPM": 1068.0, "Speed": 9.0, "Throttle Pos": 10.196078431372548, "gps_longitude": "52.45726", "gps_latitude": "16.90357", "time": {"time": 1621537478.608094}}, "5": {"RPM": 1189.0, "Speed": 10.0, "Throttle Pos": 0.0, "gps_longitude": "52.45726", "gps_latitude": "16.90297", "time": {"time": 1621537479.879662}}, "6": {"RPM": 811.0, "Speed": 7.0, "Throttle Pos": 0.0, "gps_longitude": "52.45726", "gps_latitude": "16.90237", "time": {"time": 1621537481.147938}}, "7": {"RPM": 792.0, "Speed": 7.0, "Throttle Pos": 3.1372549019607843, "gps_longitude": "52.45726", "gps_latitude": "16.90177", "time": {"time": 1621537482.417252}}, "8": {"RPM": 949.0, "Speed": 8.0, "Throttle Pos": 1.9607843137254901, "gps_longitude": "52.45726", "gps_latitude": "16.90117", "time": {"time": 1621537483.686081}}, "9": {"RPM": 978.0, "Speed": 8.0, "Throttle Pos": 6.2745098039215685, "gps_longitude": "52.45726", "gps_latitude": "16.90057", "time": {"time": 1621537484.956556}}, "10": {"RPM": 866.0, "Speed": 8.0, "Throttle Pos": 5.098039215686274, "gps_longitude": "52.45726", "gps_latitude": "16.89997", "time": {"time": 1621537486.228146}}, "11": {"RPM": 1053.0, "Speed": 9.0, "Throttle Pos": 4.705882352941177, "gps_longitude": "52.45726", "gps_latitude": "16.89937", "time": {"time": 1621537487.496225}}, "12": {"RPM": 1104.0, "Speed": 9.0, "Throttle Pos": 3.5294117647058822, "gps_longitude": "52.45726", "gps_latitude": "16.89877", "time": {"time": 1621537488.766741}}, "13": {"RPM": 990.0, "Speed": 9.0, "Throttle Pos": 2.7450980392156863, "gps_longitude": "52.45726", "gps_latitude": "16.89817", "time": {"time": 1621537490.034804}}, "14": {"RPM": 1036.0, "Speed": 9.0, "Throttle Pos": 1.1764705882352942, "gps_longitude": "52.45726", "gps_latitude": "16.89757", "time": {"time": 1621537491.305126}}}
        config = Config()
        API = config.return_API()
        send = Sender(config.return_send_interval())
        send.write_manually(data)
        self.assertEqual(data,send.print_data())
        API.logout()
        del (API)
        del(send)

    def test_logging(self):
        config = Config()
        API = config.return_API()
        self.assertEqual(API.check_authorization(), True)
        API.logout()
        del (API)


if __name__ == '__main__':
    unittest.main()