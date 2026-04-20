import asyncio
import time
from communication.ble_client import BLEClient

ble = BLEClient()

last_vibrate = 0

async def main():
    global last_vibrate

    await ble.connect()

    while True:
        print("Flex:", ble.flex)

        # TEST: vibrate when fist
        if ble.flex < 200:
            now = time.time()

            if now - last_vibrate > 0.5:
                print("FIST → VIBRATE")
                await ble.vibrate()
                last_vibrate = now

        await asyncio.sleep(0.05)

asyncio.run(main())