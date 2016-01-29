##
# The MIT License (MIT)
#
# Copyright (c) 2016 Stefan Wendler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##

import telnetlib


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

        # TODO: cache previous speeds to avoid sending same speed multiple times

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