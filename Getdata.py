from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    proximity = data.get("proximity")

    accelerometer = data.get("accelerometer", {})
    gyro = data.get("gyro", {})

    ax = accelerometer.get("x")
    ay = accelerometer.get("y")
    az = accelerometer.get("z")

    gx = gyro.get("x")
    gy = gyro.get("y")
    gz = gyro.get("z")

    print("Proximity:", proximity)
    print("Accelerometer:", ax, ay, az)
    print("Gyro:", gx, gy, gz)

    return "OK", 200

app.run(host='0.0.0.0', port=5000)
