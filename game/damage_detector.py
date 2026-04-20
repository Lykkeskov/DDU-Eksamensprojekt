import cv2
import numpy as np
import mss
import time
import asyncio
from bleak import BleakScanner, BleakClient

# -------------------------------
# BLE SETTINGS
DEVICE_NAME = "CodeCell_1"
COMMAND_UUID = "dcba4321-dcba-4321-dcba-4321fedcba98"

client = None


async def connect_ble():
    global client

    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=10.0)

    for d in devices:
        print(d.name, d.address)

        if d.name == DEVICE_NAME:
            print("Found CodeCell")

            client = BleakClient(d.address)
            await client.connect()

            print("Connected")
            return True

    print("Device not found")
    return False


async def vibrate():
    # Send vibration command ("V") to CodeCell via BLE.

    global client

    try:
        if client and client.is_connected:
            await client.write_gatt_char(COMMAND_UUID, b"V")
        else:
            print("BLE not connected")
    except Exception as e:
        print("BLE error:", e)


# -------------------------------
# SCREEN CAPTURE SETTINGS

# Indstil alt efter hvor det er.
# Lige nu passer det til en video på youtube, hvor browseren kun fylder halvdelen af skærmen.
# Sæt windows resolution til 100%
HEALTH_BAR_REGION = {
    "top": 195,
    "left": 25,
    "width": 360,
    "height": 6
}

# HSV color range for yellow health bar
LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([40, 255, 255])

# -------------------------------
# DAMAGE DETECTION SETTINGS
prev_health_ratio = None

# Minimum change required to consider health loss
THRESHOLD = 0.001

# Require multiple consecutive frames of damage to avoid noise
damage_frames = 0
REQUIRED_FRAMES = 1

# Cooldown to avoid repeated triggers
last_vibration_time = 0
COOLDOWN = 0.1


# -------------------------------
# MAIN LOOP
async def main():
    global prev_health_ratio, damage_frames, last_vibration_time

    # Connect to CodeCell over BLE
    connected = await connect_ble()
    if not connected:
        return

    with mss.mss() as sct:
        while True:
            # Capture screen region
            screenshot = sct.grab(HEALTH_BAR_REGION)
            frame = np.array(screenshot)

            # Show captured area (for debugging)
            cv2.imshow("Capture", frame)

            # Convert to HSV for color filtering
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Create mask for yellow pixels
            mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)

            # Show mask (debugging)
            cv2.imshow("Mask", mask)

            # Count yellow pixels (health amount)
            health_pixels = np.sum(mask > 0)
            total_pixels = HEALTH_BAR_REGION["width"] * HEALTH_BAR_REGION["height"]

            # Normalize to 0–1 range
            health_ratio = health_pixels / total_pixels

            print(f"Health ratio: {health_ratio:.3f}")

            # -------------------------------
            # DAMAGE DETECTION LOGIC
            if prev_health_ratio is not None:
                diff = prev_health_ratio - health_ratio

                # If health decreased significantly
                if diff > THRESHOLD:
                    damage_frames += 1
                else:
                    damage_frames = 0

                # Only trigger if consistent over multiple frames
                if damage_frames >= REQUIRED_FRAMES:
                    now = time.time()

                    if now - last_vibration_time > COOLDOWN:
                        print("DAMAGE DETECTED")
                        await vibrate()
                        last_vibration_time = now

                    damage_frames = 0

            prev_health_ratio = health_ratio

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Small delay to keep loop stable and fast
            await asyncio.sleep(0.01)

    cv2.destroyAllWindows()


# Run that shi
asyncio.run(main())