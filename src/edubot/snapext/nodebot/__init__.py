from __future__ import unicode_literals

import threading

import blockext
import blockext.generate

import edubot.snapext
import edubot.snapext.nodebot.remote


class Blocks(threading.Thread):

    __metaclass__ = edubot.snapext.Singleton

    def __init__(self, port=10001):

        threading.Thread.__init__(self)

        self.daemon = True
        self.port = port
        self.bot = None

        self.desc = blockext.Descriptor(
            name=self.name,
            port=self.port,
            blocks=blockext.get_decorated_blocks_from_class(Blocks),
            menus=dict(
                    drive=["forward", "backward", "left", "right"],
                    speed=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
        )

    @property
    def name(self):
        return "nodebot"

    @property
    def description(self):
        return "EduBot NodeMCU"

    def generate_snap(self):
        language = self.desc.translations["en"]
        return blockext.generate.generate_snap(self.desc, language)

    def run(self):
        extension = blockext.Extension(Blocks, self.desc)
        extension.run_forever(debug=True)

    def _problem(self):
        pass

    def _on_reset(self):
        pass

    @blockext.command("NodeBot connect %s", defaults=["192.168.1.122"], is_blocking=True)
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

    @blockext.command("NodeBot drive %m.drive speed %m.speed", defaults=["forward", 80], is_blocking=True)
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

    @blockext.reporter("NodeBot sees obstacle")
    def obstacle(self):

        r = -1

        if self.bot is not None:
            o = self.bot.sees_obstacle()
            if o is not None:
                r = o

        return r
