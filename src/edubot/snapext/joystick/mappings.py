from edubot.snapext.joystick.constants import *

# map JS functions to axis and buttons
JS_MAPPINGS = {
    "Generic": {
        AXIS: {
            X_AXIS_1: 0,
            Y_AXIS_1: 1,
        },
        BUTTONS: {
            BUTTON_1: 0,
            BUTTON_2: 1,
            BUTTON_3: 2,
            BUTTON_4: 3,
        },
    },
    "Sony PLAYSTATION(R)3 Controller": {
        AXIS: {
            X_AXIS_1: 0,
            Y_AXIS_1: 1,
            X_AXIS_2: 2,
            Y_AXIS_2: 3
        },
        BUTTONS: {
            BUTTON_1: 10,
            BUTTON_2: 11,
            BUTTON_3: 8,
            BUTTON_4: 9,
            L_UP: 4,
            L_DOWN: 6,
            L_LEFT: 7,
            L_RIGHT: 5,
            R_UP: 12,
            R_DOWN: 14,
            R_LEFT: 15,
            R_RIGHT: 13,
            L_1: 10,
            L_2: 8,
            R_1: 11,
            R_2: 9,
            SELECT: 0,
            START: 3
        },
    },
    "Microsoft X-Box 360 pad": {
        AXIS: {
            X_AXIS_1: 0,
            Y_AXIS_1: 1,
            X_AXIS_2: 3,
            Y_AXIS_2: 4,
            X_AXIS_3: 2,
            Y_AXIS_3: 5
        },
        BUTTONS: {
            BUTTON_1: 4,
            BUTTON_2: 5,
            BUTTON_3: 3,
            BUTTON_4: 0,
            R_UP: 3,
            R_DOWN: 0,
            R_LEFT: 2,
            R_RIGHT: 1,
            L_1: 4,
            R_1: 5,
            SELECT: 6,
            START: 7
        },
    },
}
