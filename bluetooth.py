import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "CodeCell_BLE"
CHAR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"

def notification_handler(sender, data):
    print("Received:", data.decode())

async def main():
    device = await BleakScanner.find_device_by_name(DEVICE_NAME, timeout=10.0)
    if device is None:
        print("Device not found")
        return

    async with BleakClient(device) as client:
        print("Connected")
        await client.start_notify(CHAR_UUID, notification_handler)
        await asyncio.sleep(30)
        await client.stop_notify(CHAR_UUID)

asyncio.run(main())
