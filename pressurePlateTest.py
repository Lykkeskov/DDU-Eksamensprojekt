import asyncio
from bleak import BleakClient
import time

Devices = {
    "StepSensor_Left" : "E0:5A:1B:A0:32:96",
    "StepSensor_Right" : "B4:8A:0A:8F:0D:DA"
}


CHAR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"



def make_handler(name):
    def notification_handler(sender, data):
        values = data.decode()
        print(f"\n[{name}]", values)


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
