import asyncio
from bleak import BleakClient, BleakScanner
import time
import json
from output.keyboard_output import press, release, tap
from game.game_input import GameInputMapper

mapper = GameInputMapper()

ble_clients = {}
COMMAND_UUID = "dcba4321-dcba-4321-dcba-4321fedcba98"

Devices = {
    "CodeCell_Right": "28:37:2F:C7:C5:D2",
    "CodeCell_Left": "98:3D:AE:38:32:0E",
    "StepSensor_Left": "E0:5A:1B:A0:32:96",
    "StepSensor_Right": "B4:8A:0A:8F:0D:DA",
    "JumpSensor": "E0:5A:1B:A0:32:96" # <--- Indsæt rigtig værdi
}

# Forbind kun til devices der er tændt (undgå crash hvis de nene ikke er tændt)
async def discover_devices():
    found = await BleakScanner.discover(timeout=5.0)

    available = {}

    for d in found:
        print("FOUND:", d.name, d.address)
        if d.name in Devices:
            available[d.name] = d.address

    return available

CHAR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"

damage_flag = False

slagAktiv = False
lastSlagTime = 0  # Tidspunkt for sidste slag
cooldown = 1  # Cooldown mellem slag i sekunder (300 ms)

# Bevægelses stuff
last_step_time = 0
last_jump_time = 0
jump_cooldown = 0.5

async def trigger_vibration_all():
    for name in list(ble_clients.keys()):
        await vibrate_device(name)

def make_handler(name):
    def notification_handler(sender, data):
        global slagAktiv, lastSlagTime, cooldown

        text = data.decode().strip()
        print(f"[{name}] RAW:", text)

        # Step sensor input
        if "StepSensor" in name:
            try:
                stepValue = int(text)

                if "Right" in name:
                    direction = "RIGHT"
                else:
                    direction = "LEFT"

                inputs = mapper.map(direction=direction)

                if stepValue == 1:
                    press(inputs)
                    print(f"[{name}] HOLD → {inputs}")
                else:
                    release(inputs)
                    print(f"[{name}] RELEASE → {inputs}")

            except Exception as e:
                print("Step parse error:", e)

            return

        # Jump sensor input
        if "JumpSensor" in name:
            global last_jump_time

            try:
                jumpValue = float(text)
                now = time.time()

                if now - last_jump_time > jump_cooldown:

                    # Hop bruger tap for enkelt bevægelse
                    if jumpValue < -18:
                        last_jump_time = now
                        inputs = mapper.map(direction="UP")
                        tap(inputs)
                        print(f"[{name}] JUMP → {inputs}")

                    # Duck bruger press og release for vedvarende bevægelse indtil den stoppes
                    elif jumpValue > -1:
                        inputs = mapper.map(direction="DOWN")
                        press(inputs)
                        print(f"[{name}] DUCK HOLD → {inputs}")

                    else:
                        inputs = mapper.map(direction="DOWN")
                        release(inputs)

            except Exception as e:
                print("Jump parse error:", e)

            return


        # CodeCell hanske input
        try:
            parsed = json.loads(data.decode())
        except Exception as e:
            print("JSON error:", e)
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

        print(f"[{name}] Flex: {flexValue} | Fist: {isFist}")

        slag_condition = (  # Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
                abs(yAcceleration) > 6 and
                abs(yLinAcceleration) > 7)


            #and 145 <= abs(roll) <= 180 and 110 <= abs(pitch) <= 180'''

        guard_condition = (
                abs(yLinAcceleration) < 2 and
                abs(yAcceleration) > 6) # Sat op så det ser lidt pænere ud og hvis den skal bruges til andre ting
                           #-110 < roll < -70 and


        if slag_condition and isFist and not slagAktiv:
            slagAktiv = True  # Bruges til at forhindre dobbelt registrering af slag
            lastSlagTime = time.time()  # Definerer nu tidspunktet for slaget så cooldown kan bruges korrekt

            print(f"\n[{name}] Slag registreret"
                  "\n"
                  "\n"
                  "\n")

            # Sender inputs så vi kan konvertere til keyboard input
            inputs = mapper.map(punch=True)
            send(inputs)
            print(f"[{name}] Slag → {inputs}")

        elif guard_condition and not slagAktiv:
            print(f"\n[{name}] ", "Guard registreret"
                  "\n"
                  "\n"
                  "\n")

            inputs = mapper.map(guard=True)
            send(inputs)

            print(f"[{name}] GUARD")

        if time.time() - lastSlagTime >= cooldown:
            slagAktiv = False
        '''
        else:
            print(f"\n[{name}]")
            print("Accel:", "x", xAcceleration, "y", yAcceleration, "z", zAcceleration)
            print("Rot  :", "Roll", roll, "Pitch",pitch, "Yaw",yaw)
            print("Lin  :","x" ,xLinAcceleration, "y", yLinAcceleration, "z",zLinAcceleration)
        '''

        if time.time() - lastSlagTime >= cooldown:
            slagAktiv = False
    return notification_handler

def pressurePlateHandler(name, data):
    try:
        value = data.decode().strip()
        print(f"[{name}] Pressure:", value)

        if value == "1":
            inputs = mapper.map(forward=True)
            send(inputs)
            print(f"[{name}] STEP DETECTED")
            print(f"[{name}] STEP → {inputs}")

    except Exception as e:
        print("Pressure parse error:", e)

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
    while True:  # Auto-reconnect loop hvis codecell disconnecter :)
        try:
            print(f"Connecting to {name}...")

            client = BleakClient(address, timeout=20.0)
            await asyncio.sleep(3) # Er det nødvendigt?
            await client.connect()

            print(f"{name} connected")

            ble_clients[name] = client

            # def handle_disconnect(_):
            #    print(f"{name} DISCONNECTED")

            # client.set_disconnected_callback(handle_disconnect)

            await client.start_notify(CHAR_UUID, make_handler(name))

            # Stay alive while connected
            while client.is_connected:
                await asyncio.sleep(1)

        except Exception as e:
            print(f"{name} ERROR:", e)

        print(f"{name} retrying in 3s...\n")
        await asyncio.sleep(3)

async def main():
    tasks = []
    available_devices = await discover_devices()

    for name, address in available_devices.items():
        tasks.append(connect_device(name, address))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())