from flask import Flask, request
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Only show errors
app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    accelerometer = data.get("accelerometer", {})
    motion = data.get("motion", {})
    linear_acceleration = data.get("lin", {})

    ax = float(accelerometer.get("x"))
    ay = float(accelerometer.get("y"))
    az = float(accelerometer.get("z"))

    pitch = float(motion.get("pitch")) #Ift hvordan vi vender C3 så skal pitch og roll byttes rundt
    roll = float(motion.get("roll"))
    yaw = float(motion.get("yaw"))

    linx = float(linear_acceleration.get("lx"))
    liny = float(linear_acceleration.get("ly"))
    linz = float(linear_acceleration.get("lz"))



    truepitch = pitch
    trueroll = roll
    trueyaw = yaw

    if truepitch < 0: #Test til at konvertere negative grader i intervallet [-180;180] til intervallet [0:360] bruges måske
        truepitch = 360 + truepitch

    if trueroll < 0:
        trueroll = 360 + trueroll

    if trueyaw < 0:
        trueyaw = 360 + trueyaw


    else:
        print("Accelerometer:", ax, ay, az)
        print("Linear Acceleration:", linx, liny, linz)
        print("Motion:", roll, pitch, yaw)


    return "OK", 200

app.run(host='0.0.0.0', port=5000)
