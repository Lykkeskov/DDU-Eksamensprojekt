from pynput.keyboard import Controller, Key

keyboard = Controller()

key_map = {
    "→": Key.right,
    "←": Key.left,
    "↑": Key.up,
    "↓": Key.down,
    "1": "j"   # map punch to J key
}

def send(inputs):
    for i in inputs:
        key = key_map.get(i)
        if key:
            keyboard.press(key)
            keyboard.release(key)