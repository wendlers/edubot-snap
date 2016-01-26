from __future__ import unicode_literals

import pygame
import threading

import blockext
import blockext.generate

import edubot.snapext


class Blocks(threading.Thread):

    __metaclass__ = edubot.snapext.Singleton

    def __init__(self, port=10002):

        threading.Thread.__init__(self)

        self.daemon = True
        self.port = port

        self.desc = blockext.Descriptor(
            name=self.name,
            port=self.port,
            blocks=blockext.get_decorated_blocks_from_class(Blocks),
            menus=dict(joysticks=[],
                       axis=["x-axis1", "y-axis1", "x-axis2", "y-axis2"],
                       buttons=["button1", "button2", "button3", "button4"]),
        )

        pygame.init()
        pygame.joystick.init()

        js_count = pygame.joystick.get_count()

        self.joysticks = {}
        self.desc.menus.joysticks = []

        for i in range(js_count):
            js = pygame.joystick.Joystick(i)
            js.init()

            print("Init JS % d (%s)" % (i, js.get_name()))

            js_id = "js%d" % i

            if js.get_numaxes() >= 1:
                # TODO: JS/Gamepad specific mappings
                self.joysticks[js_id] = {
                    "js": js,
                    "axis": {"x-axis1": 0, "y-axis1": 1, "x-axis2": 2, "y-axis2": 3},
                    "buttons": {"button1": 12, "button2": 13, "button3": 14, "button4": 15},
                }

                print(self.joysticks)
                self.desc.menus.joysticks.append(js_id)

    @property
    def name(self):
        return "joysitck"

    @property
    def description(self):
        return "Joystick and Gamepad"

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