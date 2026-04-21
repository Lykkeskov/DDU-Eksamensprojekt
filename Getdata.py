import asyncio
from bleak import BleakClient
import time

devices = {
    "CodeCell_Right": "28:37:2F:C7:C5:D2",
    "CodeCell_Left": "98:3D:AE:38:32:0E",
    "StepSensor_Left" : "E0:5A:1B:A0:32:96",
    "StepSensor_Right" : "B4:8A:0A:8F:0D:DA"
}


CHAR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"


slagAktiv = False
lastSlagTime = 0  #Tidspunkt for sidste slag
cooldown = 1  #Cooldown mellem slag i sekunder (300 ms)

def codecellHandler(name, data):
    global slagAktiv, lastSlagTime, cooldown

    values = data.decode().split(",")

    xAcceleratinon = float(values[0])  # Acceleratinoerne hen af de forskellige akser
    yAcceleration = float(values[1])
    zAcceleration = float(values[2])

    roll = float(values[3])  # Rotation af codecellen
    pitch = float(values[4])
    yaw = float(values[5])

    xLinAcceleration = float(values[6])  # Den linæer acceleration hvilket trækker tyngdekraften
    yLinAcceleration = float(values[7])
    zLinAcceleration = float(values[8])

    slag_condition = (  # Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
            abs(yAcceleration) > 6 and
            abs(yLinAcceleration) > 7)

    # and 145 <= abs(roll) <= 180 and 110 <= abs(pitch) <= 180'''

    guard_condition = (abs(yLinAcceleration) < 2 and abs(yAcceleration) > 6
                       # Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
                       # -110 < roll < -70 and
                       )

    if slag_condition and slagAktiv == False:
        slagAktiv = True  # Bruges til at forhindre dobbelt registrering af slag
        lastSlagTime = time.time()  # Definerer nu tidspunktet for slaget så cooldown kan bruges korrekt
        print(f"\n[{name}] ", "Slag registreret"
                              "\n"
                              "\n"
                              "\n")

    elif guard_condition and slagAktiv == False:
        print(f"\n[{name}] ", "Guard registreret"
                              "\n"
                              "\n"
                              "\n")
    else:
        print(f"\n[{name}]")
        print("Accel:", "x", xAcceleratinon, "y", yAcceleration, "z", zAcceleration)
        print("Rot  :", "Roll", roll, "Pitch", pitch, "Yaw", yaw)
        print("Lin  :", "x", xLinAcceleration, "y", yLinAcceleration, "z", zLinAcceleration)

    if time.time() - lastSlagTime >= cooldown:
        slagAktiv = False

def pressurePlateHandler(name, data):
    values = data.decode()
    print(f"\n[{name}]", values)

def make_handler(name):
    def notification_handler(sender, data):

        if "Codecell" in name:
            codecellHandler(name, data)

        elif "StepSensor" in name:
            pressurePlateHandler(name, data)

    return notification_handler


async def connect_device(name, address):
    async with BleakClient(address) as client:
        print(f"{name} connected")

        await client.start_notify(CHAR_UUID, make_handler(name))

        while True:
            await asyncio.sleep(1)


async def main():
    tasks = []

    for name, address in devices.items():
        tasks.append(connect_device(name, address))
    await asyncio.gather(*tasks)


asyncio.run(main())