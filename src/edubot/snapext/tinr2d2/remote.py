import serial
import time


class Robot:

    def __init__(self, port="/dev/rfcomm3"):

        self.s = serial.Serial(port=port, timeout=10)

        self.last_send = ""
        self.last_received = None

        time.sleep(1)

        self.send("+p")

    def send(self, msg):

        if self.last_send == msg and msg not in ["+p", "+r"]:
            return len(self.last_send)

        # self.s.flushInput()
        l = self.s.write(msg + "\r")

        self.last_send = msg
        self.last_received = None

        return l

    def receive(self):

        if self.last_received is not None:
            return self.last_received

        result = ""

        while True:

            c = self.s.read(1)

            # print("%d" % ord(c))

            if len(c) == 0 or ord(c) == 10:
                break

            if ord(c) != 13:
                result += c

        if result.startswith("!ERR "):
            raise Exception("TinR2D2 returned an error: %s" % result[5:])

        self.last_received = result[6:]

        return self.last_received

    def stop(self):

        self.send("+d s")
        return self.receive()

    def forward(self):

        self.send("+d f")
        return self.receive()

    def backward(self):

        self.send("+d b")
        return self.receive()

    def left(self):

        self.send("+d l")
        return self.receive()

    def right(self):

        self.send("+d r")
        return self.receive()

    def sound(self):

        self.send("+p")

    def range(self):

        self.send("+r")
        try:
            r = int(self.receive()[7:])
        except:
            r = 0

        return r
