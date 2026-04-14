import asyncio
from bleak import BleakClient

CHAR_UUID = "abcd5678-abcd-5678-abcd-56789abcdef0"

LEFT_ADDRESS = "98:3D:AE:38:32:0E" #hvis den ikke kan connecte med bluetooth, tjek om korrekt addrese ved begge
RIGHT_ADDRESS = "28:37:2F:C7:C5:D2"

def make_notification_handler(label): #Funktionen får data fra ino filen, og printer den ud, med hvilken codecell der sender dataen
    def handler(sender, data):
        try:
            text = data.decode()
        except UnicodeDecodeError:
            text = str(data)
        print(f"{label}: {text}")
    return handler

async def connect_device(address, label):
    try:
        async with BleakClient(address) as client:
            print(f"{label} connected to {address}")

            await client.start_notify(
                CHAR_UUID,
                make_notification_handler(label)
            )

            await asyncio.sleep(30)

            await client.stop_notify(CHAR_UUID)
            print(f"{label} disconnected")

    except Exception as e:
        print(f"{label} error: {e}")

async def main():
    await asyncio.gather(
        connect_device(LEFT_ADDRESS, "LEFT"),
        connect_device(RIGHT_ADDRESS, "RIGHT")
    )

asyncio.run(main())
