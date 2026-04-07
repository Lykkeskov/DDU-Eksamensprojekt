from flask import Flask, request
import logging
import time

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Only show errors
app = Flask(__name__)

slagAktiv = False
lastSlagTime = 0  #Tidspunkt for sidste slag
cooldown = 0.3  #Cooldown mellem slag i sekunder (300 ms)
@app.route('/data', methods=['POST'])
def receive_data():
    global slagAktiv, lastSlagTime, cooldown
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

    slag_condition = (              #Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
            abs(ay) > 5 and
            abs(liny) > 0 and
            145 <= abs(roll) <= 180 and
            120 <= abs(pitch) <= 180
    )

    guard_condition = (abs(liny) < 2 and    #Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
                       -110 < roll < 70 and
                       5 < abs(ay))

    if slag_condition and slagAktiv == False:
        slagAktiv = True #Bruges til at forhindre dobbelt registrering af slag
        lastSlagTime = time.time() #Definerer nu tidspunktet for slaget så cooldown kan bruges korrekt
        print("Slag registreret ",
              "\n"
              "\n"
              "\n")
    elif guard_condition:
        print("Guard registreret ",
              "\n"
              "\n"
              "\n")

    else:
        print("Accelerometer: ", ax, ay, az)
        print("Linear Acceleration: ", linx, liny, linz)
        print("Motion: ", roll, pitch, yaw)
        print("Tid: ", time.time()-lastSlagTime)

    if time.time()-lastSlagTime >= cooldown:
        slagAktiv = False

    return "OK", 200

app.run(host='0.0.0.0', port=5000)
