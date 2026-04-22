import asyncio
from bleak import BleakClient, BleakScanner
import time
import json

ble_clients = {}
COMMAND_UUID = "dcba4321-dcba-4321-dcba-4321fedcba98"


Devices = {
    "CodeCell_Right": "28:37:2F:C7:C5:D2",
    "CodeCell_Left": "98:3D:AE:38:32:0E"
}

# Forbind kun til devices der er tændt (undgå crash hvis de nene ikke er tændt)
async def discover_devices():
    found = await BleakScanner.discover(timeout=5.0)

    available = {}

    for d in found:
        if d.name in Devices:
            available[d.name] = d.address

    return available

CHAR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"

damage_flag = False

slagAktiv = False
lastSlagTime = 0  #Tidspunkt for sidste slag
cooldown = 1  #Cooldown mellem slag i sekunder (300 ms)

async def trigger_vibration_all():
    for name in list(ble_clients.keys()):
        await vibrate_device(name)

def make_handler(name):
    def notification_handler(sender, data):
        global slagAktiv, lastSlagTime, cooldown
        '''
        values = data.decode().split(",")

        xAcceleratinon = float(values[0]) #Acceleratinoerne hen af de forskellige akser
        yAcceleration = float(values[1])
        zAcceleration = float(values[2])

        roll = float(values[3]) #Rotation af codecellen
        pitch = float(values[4])
        yaw = float(values[5])

        xLinAcceleration = float(values[6]) #Den linæer acceleration hvilket trækker tyngdekraften
        yLinAcceleration = float(values[7])
        zLinAcceleration = float(values[8])
        '''

        try:
            decoded = data.decode()
            parsed = json.loads(decoded)
        except Exception as e:
            print("JSON parse error:", e)
            print("Raw data:", data)
            return


        # Extract values
        flexValue = parsed["flex"]
        isFist = parsed["fist"]

        xAcceleration = parsed["ax"]
        yAcceleration = parsed["ay"]
        zAcceleration = parsed["az"]

        roll = parsed["rx"]
        pitch = parsed["ry"]
        yaw = parsed["rz"]

        xLinAcceleration = parsed["lx"]
        yLinAcceleration = parsed["ly"]
        zLinAcceleration = parsed["lz"]

        slag_condition = (  # Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
                abs(yAcceleration) > 6 and
                abs(yLinAcceleration) > 7)


            #and 145 <= abs(roll) <= 180 and 110 <= abs(pitch) <= 180'''

        guard_condition = (abs(yLinAcceleration) < 2 and abs(yAcceleration) > 6 # Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
                           #-110 < roll < -70 and
                           )

        if slag_condition and isFist and slagAktiv == False:
            slagAktiv = True  # Bruges til at forhindre dobbelt registrering af slag
            lastSlagTime = time.time()  # Definerer nu tidspunktet for slaget så cooldown kan bruges korrekt
            print(f"\n[{name}] Slag registreret\n")

            asyncio.create_task(trigger_vibration_all())

        elif guard_condition and slagAktiv == False:
            print(f"\n[{name}] ", "Guard registreret"
                  "\n"
                  "\n"
                  "\n")
        else:
            print(f"\n[{name}]")
            print("Accel:", "x", xAcceleration, "y", yAcceleration, "z", zAcceleration)
            print("Rot  :", "Roll", roll, "Pitch",pitch, "Yaw",yaw)
            print("Lin  :","x" ,xLinAcceleration, "y", yLinAcceleration, "z",zLinAcceleration)




        if time.time() - lastSlagTime >= cooldown:
            slagAktiv = False
    return notification_handler


async def vibrate_device(name):
    if name in ble_clients:
        client = ble_clients[name]

        if client.is_connected:
            try:
                await client.write_gatt_char(COMMAND_UUID, b"V")
                print(f"{name} VIBRATE")
            except Exception as e:
                print("BLE error:", e)

async def connect_device(name, address):
    try:
        client = BleakClient(address)
        await client.connect(timeout=10.0)

        print(f"{name} connected")

        ble_clients[name] = client

        await client.start_notify(CHAR_UUID, make_handler(name))

        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"{name} FAILED:", e)


async def main():
    tasks = []
    available_devices = await discover_devices()

    for name, address in available_devices.items():
        tasks.append(connect_device(name, address))

    await asyncio.gather(*tasks)


asyncio.run(main())
