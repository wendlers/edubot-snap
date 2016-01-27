from __future__ import unicode_literals

import pygame

import blockext
import edubot.snapext


# map JS functions to axis and buttons
JS_MAPPINGS = {
    "Generic": {
        "axis": {"x-axis1": 0, "y-axis1": 1},
        "buttons": {"button1": 0, "button2": 1},
    },
    "Sony PLAYSTATION(R)3 Controller": {
        "axis": {"x-axis1": 0, "y-axis1": 1, "x-axis2": 2, "y-axis2": 3},
        "buttons": {
            "button1": 10, "button2": 11,
            "lup": 4, "ldown": 6, "lleft": 7, "lright": 5,
            "rup": 12, "rdown": 14, "rleft": 15, "rright": 13,
            "l1": 10, "l2": 8, "r1": 11, "r2": 9,
            "select": 0, "start": 3},
    },
    "Microsoft X-Box 360 pad": {
        "axis": {"x-axis1": 0, "y-axis1": 1, "x-axis2": 3, "y-axis2": 4, "x-axis3": 2, "y-axis3": 5},
        "buttons": {
            "button1": 4, "button2": 5,
            "rup": 3, "rdown": 0, "rleft": 2, "rright": 1,
            "l1": 4, "r1": 5,
            "select": 6, "start": 7},
    },
}


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

            js_id = "js%d" % i

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

    @blockext.reporter("Joystick %m.joysticks axis %m.axis", defaults=["js0", "x-axis1"], is_blocking=True)
    def axis(self, js_id, axis):

        try:

            pygame.event.get()
            js = self.joysticks[js_id]["js"]
            axis_id = self.joysticks[js_id]["axis"][axis]
            value = js.get_axis(axis_id)

        except KeyError:
            value = 0.0

        print("Joystick %s %s: %f" % (js_id, axis, value))
        return round(value, 3)

    @blockext.reporter("Joystick %m.joysticks button %m.buttons", defaults=["js0", "button1"], is_blocking=True)
    def buttons(self, js_id, button):

        try:

            pygame.event.get()
            js = self.joysticks[js_id]["js"]
            button_id = self.joysticks[js_id]["buttons"][button]
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
                    joysticks=["js0", "js1"],
                    axis=[
                        # all known axis must be listed here
                        "x-axis1", "y-axis1", "x-axis2", "y-axis2", "x-axis3", "y-axis3"
                    ],
                    buttons=[
                        # all known button must be listed here
                        "lup", "ldown", "lleft", "lright",
                        "rup", "rdown", "rleft", "rright",
                        "l1", "l2", "r1", "r2",
                        "select", "start",
                        "button1", "button2"
                    ]))
