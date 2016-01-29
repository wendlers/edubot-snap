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

import pygame

import blockext
import edubot.snapext

from edubot.snapext.joystick.constants import ALL_JS, ALL_AXIS, ALL_BUTTONS, AXIS, BUTTONS
from edubot.snapext.joystick.mappings import JS_MAPPINGS


class Blocks:

    def __init__(self):

        pygame.init()
        pygame.joystick.init()

        js_count = pygame.joystick.get_count()

        # support a maximum of two joysticks
        if js_count > 2:
            js_count = 2

        self.joysticks = {}

        for i in range(js_count):
            js = pygame.joystick.Joystick(i)
            js.init()

            print("Init JS % d (%s)" % (i, js.get_name()))

            js_id = "js%d" % (i + 1)

            if js.get_numaxes() >= 1:

                if js.get_name() in JS_MAPPINGS:
                    self.joysticks[js_id] = JS_MAPPINGS[js.get_name()]
                else:
                    self.joysticks[js_id] = JS_MAPPINGS["Generic"]

                self.joysticks[js_id]["js"] = js

                # print(self.joysticks)

    def _problem(self):
        pass

    def _on_reset(self):
        pass

    @blockext.reporter("Joystick %m.joysticks axis %m.axis", defaults=[ALL_JS[0], ALL_AXIS[0]], is_blocking=True)
    def axis(self, js_id, axis):

        try:

            pygame.event.get()
            js = self.joysticks[js_id]["js"]
            axis_id = self.joysticks[js_id][AXIS][axis]
            value = js.get_axis(axis_id)

        except KeyError:
            value = 0.0

        print("Joystick %s %s: %f" % (js_id, axis, value))
        return round(value, 3)

    @blockext.reporter("Joystick %m.joysticks button %m.buttons", defaults=[ALL_JS[0], ALL_BUTTONS[0]], is_blocking=True)
    def buttons(self, js_id, button):

        try:

            pygame.event.get()
            js = self.joysticks[js_id]["js"]
            button_id = self.joysticks[js_id][BUTTONS][button]
            value = js.get_button(button_id)

        except KeyError:
            value = 0

        print("Joystick %s %s: %d" % (js_id, button, value))
        return value


class Extension(edubot.snapext.BaseExtension):

    def __init__(self, port=10002):

        edubot.snapext.BaseExtension.__init__(
                self,
                Blocks,
                port,
                "Joystick",
                "Joystick and Gamepad",
                dict(
                    joysticks=ALL_JS,
                    axis=ALL_AXIS,
                    buttons=ALL_BUTTONS
                ))
