from __future__ import unicode_literals

import blockext
import blockext.generate
import threading
import remote


class EduBot(threading.Thread):

    def __init__(self, port=10001):

        threading.Thread.__init__(self)

        self.daemon = True
        self.port = port
        self.bot = None

        self.desc = blockext.Descriptor(
            name=self.name,
            port=self.port,
            blocks=blockext.get_decorated_blocks_from_class(EduBot),
            menus=dict(drive=["forward", "backward", "left", "right"]),
        )

    @property
    def name(self):
        return "edubot"

    @property
    def description(self):
        return "EduBot Blocks"

    def generate_snap(self):
        language = self.desc.translations["en"]
        return blockext.generate.generate_snap(self.desc, language)

    def run(self):

        extension = blockext.Extension(EduBot, self.desc)
        extension.run_forever(debug=True)

    def _problem(self):
        pass

    def _on_reset(self):
        pass

    @blockext.command("Connect to EduBot %s", defaults=["192.168.1.122"], is_blocking=True)
    def connect(self, host=None):
        print(host)
        if host is not None:
            try:
                self.bot = remote.Robot(host=host)
            except Exception as e:
                print(e)
                print("bot", self.bot)

    @blockext.command("Stop", is_blocking=True)
    def stop(self):

        if self.bot is not None:
            self.bot.stop()

    @blockext.command("Drive %m.drive with speed %n", defaults=["forward", 80], is_blocking=True)
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
