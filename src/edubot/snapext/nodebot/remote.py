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

import requests


class Robot:

    def __init__(self, host):

        self.base_url = "http://%s" % host

    def drive(self, speed_a, speed_b):

        r = requests.get("%s/drive?a=%d&b=%d" % (self.base_url, speed_a, speed_b))
        return r.status_code == 200

    def forward(self, speed=100):
        return self.drive(speed, speed)

    def backward(self, speed=100):
        return self.drive(-speed, -speed)

    def left(self, speed=100):
        return self.drive(-speed, speed)

    def right(self, speed=100):
        return self.drive(speed, -speed)

    def stop(self):
        return self.drive(0, 0)

    def sees_obstacle(self):

        d = self.distance()

        if d < 25:
            o = 2
        elif d < 50:
            o = 1
        else:
            o = 0

        return o

    def distance(self):

        d = 0.0

        r = requests.get("http://192.168.1.112/range");

        if r.status_code == 200:
            d = r.json()["d"]

        return d
