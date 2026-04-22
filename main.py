import asyncio
from Getdata import main as ble_main, vibrate_device
from game.damage_detector import main as damage_main

async def main():
    await asyncio.gather(
        ble_main(),        # BLE system
        damage_main()      # damage detection
    )

asyncio.run(main())