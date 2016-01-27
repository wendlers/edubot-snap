from __future__ import unicode_literals

import threading

import blockext
import blockext.generate

import edubot.snapext
import edubot.snapext.nodebot.remote


class Blocks:

    def __init__(self):
        self.bot = None
        self.speed = {"A": 0, "B": 0}

    def _problem(self):
        pass

    def _on_reset(self):
        pass

    @blockext.command("NodeBot connect %s", defaults=["ESP_06F38E"], is_blocking=True)
    def connect(self, host=None):
        print(host)
        if host is not None:
            try:
                self.bot = edubot.snapext.nodebot.remote.Robot(host=host)
            except Exception as e:
                print(e)
                print("bot", self.bot)

    @blockext.command("NodeBot stop", is_blocking=True)
    def stop(self):

        if self.bot is not None:
            self.bot.stop()

    @blockext.command("NodeBot drive %m.drive speed %n", defaults=["forward", 80], is_blocking=True)
    def drive(self, direction, speed):

        if self.bot is not None:

            print("direction", direction)
            print("speed", speed)

            if direction == "forward":
                self.bot.forward(speed)
            elif direction == "backward":
                self.bot.backward(speed)
            elif direction == "left":
                self.bot.left(speed)
            if direction == "right":
                self.bot.right(speed)

    @blockext.command("NodeBot motor %m.motor speed %n", defaults=["A", 0], is_blocking=True)
    def motor(self, motor, speed):

        self.speed[motor] = speed

        if self.bot is not None:
            self.bot.drive(self.speed["A"], self.speed["B"])

    @blockext.reporter("NodeBot sees obstacle")
    def obstacle(self):

        r = -1

        if self.bot is not None:
            o = self.bot.sees_obstacle()
            if o is not None:
                r = o

        return r


class Extension(edubot.snapext.BaseExtension):

    def __init__(self, port=10001):
        edubot.snapext.BaseExtension.__init__(
                self,
                Blocks,
                port,
                "nodebot",
                "EduBot NodeMCU",
                dict(drive=["forward", "backward", "left", "right"],
                     motor=["A", "B"]))
