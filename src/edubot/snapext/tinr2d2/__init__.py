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

from __future__ import unicode_literals

import blockext
import blockext.generate

import edubot.snapext
import edubot.snapext.tinr2d2.remote


class Blocks:

    def __init__(self):
        self.bot = None

    def _problem(self):
        pass

    def _on_reset(self):
        pass

    @blockext.command("TinR2D2 connect %s", defaults=["/dev/rfcomm3"], is_blocking=True)
    def connect(self, port=None):
        print(port)
        if port is not None:
            try:
                self.bot = edubot.snapext.tinr2d2.remote.Robot(port=port)
            except Exception as e:
                print(e)
                print("bot", self.bot)

    @blockext.command("TinR2D2 stop", is_blocking=True)
    def stop(self):

        if self.bot is not None:
            self.bot.stop()

    @blockext.command("TinR2D2 drive %m.drive", defaults=["forward"], is_blocking=True)
    def drive(self, direction):

        if self.bot is not None:

            print("direction", direction)

            if direction == "forward":
                self.bot.forward()
            elif direction == "backward":
                self.bot.backward()
            elif direction == "left":
                self.bot.left()
            if direction == "right":
                self.bot.right()

    @blockext.command("TinR2D2 play sound", is_blocking=True)
    def sound(self):

        if self.bot is not None:
            self.bot.sound()

    @blockext.reporter("TinR2D2 ultrasonic range")
    def range(self):

        r = 0

        if self.bot is not None:
            r = self.bot.range()

        print("range: %d" % r)

        return r


class Extension(edubot.snapext.BaseExtension):

    def __init__(self, port=10003):
        edubot.snapext.BaseExtension.__init__(
                self,
                Blocks,
                port,
                "TinR2D2",
                "EduBot TinR2D2",
                dict(drive=["forward", "backward", "left", "right"]))
