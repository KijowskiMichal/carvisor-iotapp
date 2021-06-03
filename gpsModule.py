import re

class gps:

        def __init__(self):
                self.prepare_for_fake_gps()

        def prepare_for_fake_gps(self):
                self.longitude = 16.92397
                self.latitude = 52.45726

        def get_current_position_from_phone(self):
                location_file = open("location", 'r').readlines()[-2]
                gps_real = re.findall('[0-9]*[\.]{1}[0-9]*', location_file)
                return {'longitude': float("%.5f" % float(gps_real[0])),
                                        "latitude": float("%.5f" % float(gps_real[1]))}

        def get_fake_gps_position(self):
                position = {'longitude': float("%.5f" % self.longitude),
                 "latitude": float("%.5f" % self.latitude)}
                self.latitude -= 0.00060
                return position

        def get_only_position_values(self):
                return [self.longitude,self.latitude]

        def get_position(self):
                # return self.get_current_position_from_phone()
                return self.get_fake_gps_position()