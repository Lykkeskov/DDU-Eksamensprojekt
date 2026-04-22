import cv2
import numpy as np
import mss
import time
import asyncio
from Getdata import vibrate_device

# SCREEN CAPTURE SETTINGS :)

HEALTH_BAR_REGION = {
    "top": 195,
    "left": 25,
    "width": 360,
    "height": 6
}

LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([40, 255, 255])

# DAMAGE DETECTION SETTINGS
prev_health_ratio = None
THRESHOLD = 0.001
damage_frames = 0
REQUIRED_FRAMES = 1
last_vibration_time = 0
COOLDOWN = 0.1


async def main():
    global prev_health_ratio, damage_frames, last_vibration_time

    with mss.mss() as sct:
        while True:
            screenshot = sct.grab(HEALTH_BAR_REGION)
            frame = np.array(screenshot)

            cv2.imshow("Capture", frame)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)

            cv2.imshow("Mask", mask)

            health_pixels = np.sum(mask > 0)
            total_pixels = HEALTH_BAR_REGION["width"] * HEALTH_BAR_REGION["height"]
            health_ratio = health_pixels / total_pixels

            print(f"Health ratio: {health_ratio:.3f}")

            if prev_health_ratio is not None:
                diff = prev_health_ratio - health_ratio

                if diff > THRESHOLD:
                    damage_frames += 1
                else:
                    damage_frames = 0

                if damage_frames >= REQUIRED_FRAMES:
                    now = time.time()

                    if now - last_vibration_time > COOLDOWN:
                        print("DAMAGE DETECTED")
                        await vibrate_device("CodeCell_Left")
                        last_vibration_time = now

                    damage_frames = 0

            prev_health_ratio = health_ratio

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            await asyncio.sleep(0.01)

    cv2.destroyAllWindows()


asyncio.run(main())