import pydirectinput

key_map = {
    "→": "d",
    "←": "a",
    "↓": "s",
    "↑": "w",
    "1": "j",
    "2": "i",
    "3": "k",
    "4": "l",
    "BL": "o"
}

# Hold øje med hvilken tast det bliver trykket på
held_keys = set()

def press(inputs):
    for i in inputs:
        key = key_map.get(i)
        if key and key not in held_keys:
            pydirectinput.keyDown(key)
            held_keys.add(key)

def release(inputs):
    for i in inputs:
        key = key_map.get(i)
        if key and key in held_keys:
            pydirectinput.keyUp(key)
            held_keys.remove(key)

def tap(inputs):
    for i in inputs:
        key = key_map.get(i)
        if key:
            pydirectinput.press(key)