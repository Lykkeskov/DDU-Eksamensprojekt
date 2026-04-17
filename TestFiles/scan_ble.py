import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"Name: {d.name}, Address: {d.address}")

asyncio.run(main())

#GUIDE: Sådan gør jeg; Læg denne fil ind i din desktop på computeren og åben terminal. 
#Når terminal er åben run: 'cd desktop' og dette åbener op ind til ens fil. 
#Derefter skrev: 'python scan_ble.py' VIGTIGT man ikke har skiftet navnet på filen. 
#Det kan tage noget tid, men ellers finder din computer alle bluetooth devices
#Led efter; 'Codecell_Right' og 'Codecell_Left' og det er disse addreser man skal bruge

