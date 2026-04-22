from flask import Flask, request
from game.action_processor import ActionProcessor
from game.input_buffer import InputBuffer
from game.combo_detector import ComboDetector
from output.keyboard_output import send

app = Flask(__name__)

processor = ActionProcessor()
buffer = InputBuffer()
combo_detector = ComboDetector()


@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    # TEMP: simulate actions (skift med rigtige senere)
    actions = data.get("actions", [])

    inputs = processor.process(actions)

    buffer.add(inputs)

    combo = combo_detector.detect(buffer.get())

    if combo:
        print("COMBO:", combo)

    send(inputs)

    if inputs:
        print("Inputs:", inputs)

    return "OK", 200

from communication.ble_client import BLEClient
import asyncio

ble = BLEClient()

async def main():
    await ble.connect()

    while True:
        # Access flex
        if ble.flex < 200:
            print("FIST")

        await asyncio.sleep(0.01)

asyncio.run(main())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)