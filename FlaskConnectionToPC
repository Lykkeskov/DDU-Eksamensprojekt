from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    taldata = float(str(data).rstrip("}").replace("{'proximity': ", ""))
    print("Received:", taldata)

    return "OK", 200

app.run(host='0.0.0.0', port=5000)
