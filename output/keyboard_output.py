from pynput.keyboard import Controller, Key

keyboard = Controller()

key_map = {
    "→": "d",
    "←": "a",
    "↓": "s",
    "↑": "w",
    "1": "j",
    "2": "i",
    "3": "k",
    "4": "l",
    "BL": "space"
}

def send(inputs):
    for i in inputs:
        key = key_map.get(i)
        if key:
            keyboard.press(key)
            keyboard.release(key)