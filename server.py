from flask import Flask, request
import logging

from detectors.punch_detector import PunchDetector
from detectors.direction_detector import DirectionDetector
from game.game_input import GameInputMapper
from game.input_buffer import InputBuffer
from output.keyboard_output import send

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

punch_detector = PunchDetector()
direction_detector = DirectionDetector()
mapper = GameInputMapper()
buffer = InputBuffer()


@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    motion = data.get("motion", {})
    lin = data.get("lin", {})

    roll = float(motion.get("roll", 0))
    pitch = float(motion.get("pitch", 0))

    lx = float(lin.get("lx", 0))
    ly = float(lin.get("ly", 0))
    lz = float(lin.get("lz", 0))

    # Detect actions
    punch = punch_detector.detect(lx, ly, lz)
    direction = direction_detector.detect(roll, pitch)

    # Map to game inputs
    inputs = mapper.map(punch=punch, direction=direction)

    # Add to buffer
    for i in inputs:
        buffer.add(i)

    # Send to game
    send(inputs)

    if inputs:
        print("Inputs:", inputs)

    return "OK", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)