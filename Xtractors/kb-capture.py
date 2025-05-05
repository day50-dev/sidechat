#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-xlib",
#     "ipdb"
# ]
# ///




from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq

local_display = display.Display()
record_display = display.Display()

captured_string = ""

def lookup_keycode(keycode):
    keysym = local_display.keycode_to_keysym(keycode, 0)
    return XK.keysym_to_string(keysym) if keysym else None

def callback(data):
    global captured_string
    if not data or data.category != record.FromServer or data.client_swapped or not len(data.data):
        return

    if data.data.startswith(b'\x02') or data.data.startswith(b'\x03'):
        event = data.data[0]
        if event == X.KeyPress or data.data.startswith(b'\x02'):
            keycode = data.data[1]
            state = data.data[2]
            shift_pressed = state & 1
            keysym = local_display.keycode_to_keysym(keycode, 1 if shift_pressed else 0)
            key = XK.keysym_to_string(keysym) if keysym else None

            if key:
                if key == ";" or key == ":":
                    print(captured_string)
                    exit(0)
                elif key == "BackSpace":
                    captured_string = captured_string[:-1]
                else:
                    captured_string += key

if not record_display.has_extension("RECORD"):
    print("X server does not support the RECORD extension")
    exit(1)

# Fix the record context creation
ctx = record_display.record_create_context(
    0,
    [record.AllClients],
    [{
        'core_requests': (0, 0),
        'core_replies': (0, 0),
        'ext_requests': (0, 0, 0, 0),
        'ext_replies': (0, 0, 0, 0),
        'delivered_events': (0, 0),
        'device_events': (X.KeyPress, X.KeyRelease),  # Captures key events
        'errors': (0, 0),
        'client_started': False,
        'client_died': False,
    }]
)

record_display.record_enable_context(ctx, callback)

