import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "CodeCell_1"

SENSOR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"
COMMAND_UUID = "dcba4321-dcba-4321-dcba-4321fedcba98"


class BLEClient:
    def __init__(self):
        self.client = None
        self.flex = 0
        self.motion = None

    async def connect(self):
        print("Searching for device...")
        device = await BleakScanner.find_device_by_name(DEVICE_NAME)

        if device is None:
            print("Device not found")
            return

        self.client = BleakClient(device)
        await self.client.connect()

        print("Connected to CodeCell")

        await self.client.start_notify(SENSOR_UUID, self.notification_handler)

    def notification_handler(self, sender, data):
        values = data.decode().split(",")

        self.flex = int(values[0])
        self.motion = list(map(float, values[1:]))

    async def vibrate(self):
        if self.client:
            await self.client.write_gatt_char(COMMAND_UUID, b"V")