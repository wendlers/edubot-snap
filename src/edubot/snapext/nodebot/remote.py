import telnetlib

__author__ = 'stefan'

# TODO: error handling (response from robot is "OK" or "ERROR" => map to True or False


class Robot:

    def __init__(self, host):
        self.tn = telnetlib.Telnet(host)

    def __check_response(self):
        # FIXME blocks every now and then :-(

        """
        idx, _, _ = self.tn.expect([r"OK\n", r"ERROR\n"])
        return idx == 0
        """

        return True

    def drive(self, speed_a, speed_b):
        self.tn.write("d%+04d%+04d\n" % (speed_a, speed_b))
        return self.__check_response()

    def forward(self, speed=100):
        self.drive(speed, speed)
        return self.__check_response()

    def backward(self, speed=100):
        self.drive(-speed, -speed)
        return self.__check_response()

    def left(self, speed=100):
        self.drive(-speed, speed)
        return self.__check_response()

    def right(self, speed=100):
        self.drive(speed, -speed)
        return self.__check_response()

    def stop(self):
        self.drive(0, 0)
        return self.__check_response()

    def sees_obstacle(self):
        # FIXME blocks every now and then :-(

        """
        self.tn.write("o")
        idx, _, _ = self.tn.expect([r"NO\n", r"FAR\n", r"CLOSE\n", r"ERROR\n"])
        return None if idx == 3 else idx
        """

        return 0