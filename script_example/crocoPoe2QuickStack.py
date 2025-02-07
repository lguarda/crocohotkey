#!/usr/bin/env python3
import pynput
import pyperclip
import time
import re

from pynput import keyboard

keyboard_sim = keyboard.Controller()
mouse_sim = pynput.mouse.Controller()
ctrl = keyboard.Key.ctrl.value


# number of slot in inventory to parse poe2 is 5 by 12
poe_inventory_x = 5
poe_inventory_y = 10

# distance between inventory slot this could differ base on screen/game resolution
# maybe screen dpi also i'm not sure
poe_x_scale = 70
poe_y_scale = 70

# positon of top left inventory case
# this can be set with custom key bind
# or it will be set automatical to mouse position when tiggering quick stack
top_x = 0
top_y = 0


# currency to quick stack
quick_stack_allowed_currecy = {
    "Regal Orb": True,
    "Orb of Augmentation": True,
    "Orb of Alchemy": True,
    "Chaos Orb": True,
    "Vaal Orb": True,
    "Exalted Orb": True,
    "Armourer's Scrap": True,
    "Artificer's Orb": True,
    "Blacksmith's Whetstone": True,
    "Gemcutter's Prism": True,
    "Glassblower's Bauble": True,
    "Lesser Jeweller's Orb": True,
    "Orb of Transmutation": True,
    "Regal Shard": True,
    "Transmutation Shard": True,
    "Chance Shard": True,
}

# rest of currency to quick stack
quick_stack_regex_currecy = [
    re.compile(r".* Shard"),
    re.compile(r"Distilled .*"),
    re.compile(r"Orb .*"),
    re.compile(r".* Orb"),
    re.compile(r"Essence .*"),
]


def check_currency_regex(name):
    for pattern in quick_stack_regex_currecy:
        if pattern.match(name):
            return True
    return False


def check_listed_currency(name):
    ret = quick_stack_allowed_currecy.get(name, False)
    if not ret:
        return check_currency_regex(name)
    return ret


def detect_currency(item: str):
    if item.startswith("Item Class: Stackable Currency"):
        name = item.splitlines()[2]
        ret = check_listed_currency(name)
        if not ret:
            print(f"Found currency not listed {name}")
        return ret
    return False


def move_mouse_on_inventory(func):
    # If origin position not set, use current position
    if top_y == 0:
        set_top_position_on_mouse()

    for y in range(poe_inventory_y):
        new_y = top_y + (y * poe_y_scale)
        mouse_sim.position = (new_y, top_x)
        for x in range(poe_inventory_x):
            new_x = top_x + (x * poe_x_scale)
            mouse_sim.position = (new_y, new_x)
            time.sleep(0.05)
            func()


def stack_item_on_mouse():
    keyboard_sim.press(ctrl)
    time.sleep(0.02)
    mouse_sim.click(pynput.mouse.Button.left)
    time.sleep(0.02)
    keyboard_sim.release(ctrl)


def get_item_on_mouse():
    keyboard_sim.press(ctrl)
    keyboard_sim.press("c")
    time.sleep(0.02)
    keyboard_sim.release(ctrl)
    keyboard_sim.release("c")

    clipboard_text = pyperclip.paste()
    if detect_currency(clipboard_text):
        stack_item_on_mouse()


def trigger_quick_stack():
    move_mouse_on_inventory(get_item_on_mouse)


def set_top_position_on_mouse():
    pos = mouse_sim.position
    global top_y
    global top_x
    top_y = pos[0]
    top_x = pos[1]
    print(f"set new positon origin to {top_y} {top_x}")


listener = keyboard.GlobalHotKeys(
    {"<ctrl>+<alt>+h": trigger_quick_stack, "<ctrl>+<alt>+i": set_top_position_on_mouse}
)

listener.start().join()
