import cv2
import numpy as np
import mss
import time
import requests

# Indstil alt efter hvor det er.
# Lige nu passer det til en video på youtube, hvor browseren kun fylder halvdelen af skærmen.
# Sæt windows resolution til 100%
HEALTH_BAR_REGION = {
    "top": 195,
    "left": 15,
    "width": 410,
    "height": 8
}

# Yellow health bar
LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([40, 255, 255])

prev_health_ratio = None
THRESHOLD = 0.001  # Juster følsomheden hvis det er nødvendigt

last_vibration_time = 0
COOLDOWN = 0.5  # seconds

CODECELL_IP = "YOUR_CODECELL_IP" # Husk at Indsætte

def vibrate():
    try:
        requests.get(f"http://{CODECELL_IP}/vibrate", timeout=0.2)
    except:
        print("Failed to send vibration signal")


with mss.mss() as sct:
    while True:
        screenshot = sct.grab(HEALTH_BAR_REGION)
        frame = np.array(screenshot)

        # Show captured region
        cv2.imshow("Capture", frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)

        # Show mask (til debug)
        cv2.imshow("Mask", mask)

        # Count yellow pixels
        health_pixels = np.sum(mask > 0)
        total_pixels = HEALTH_BAR_REGION["width"] * HEALTH_BAR_REGION["height"]
        health_ratio = health_pixels / total_pixels

        print(f"Health ratio: {health_ratio:.3f}")

        if prev_health_ratio is not None:
            diff = prev_health_ratio - health_ratio

            if diff > THRESHOLD:
                now = time.time()
                if now - last_vibration_time > COOLDOWN:
                    print("---> DAMAGE DETECTED <---")
                    vibrate()
                    last_vibration_time = now

        prev_health_ratio = health_ratio

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.05)

cv2.destroyAllWindows()