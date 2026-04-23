import asyncio
from bleak import BleakClient
import time

Devices = {
    "JumpSensor" : "98:3D:AE:38:32:0E"
}


CHAR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"

jumpCooldown = 1
lastMovement = 0
lastMeasurement = 0
maxValue = -9

def make_handler(name):
    def notification_handler(sender, data):
        global lastMovement, jumpCooldown, lastMeasurement, maxValue
        if time.time()-lastMeasurement:
            value = float(data.decode())
            if value > maxValue:
                maxValue = value


            '''
            print(f"\n{name}: ", value)
            print("Minumum Value",f"\n{name}: ", maxValue)'''

            if value < -18 and time.time()-lastMovement > jumpCooldown:
                print(f"\n{name}: ", "Jump registeret")
                lastMovement = time.time()

            elif value > -1 and time.time()-lastMovement > jumpCooldown:
                print(f"\n{name}: ", "Duck")
                lastMovement = time.time()


            lastMeasurement = time.time()




    return notification_handler


async def connect_device(name, address):
    async with BleakClient(address) as client:
        print(f"{name} connected")

        await client.start_notify(CHAR_UUID, make_handler(name))

        while True:
            await asyncio.sleep(1)


async def main():
    tasks = []

    for name, address in Devices.items():
        tasks.append(connect_device(name, address))
    await asyncio.gather(*tasks)


asyncio.run(main())
