import pyautogui
import numpy as np
import cv2
import time
import os
from datetime import datetime
from threading import Thread
from PIL import Image

# === CONFIGURATION ===
base_dir = "C:/Image Check"
notify_folder = os.path.join(base_dir, "notify")
motion_base_folder = os.path.join(base_dir, "img_final")

notify_total = 10
notify_interval = 60  # 1 minute

motion_threshold = 500000
motion_interval = 1  # 1 second

resize_scale = 0.5
jpeg_quality = 85

# === Ensure notify folder exists and is empty ===
os.makedirs(notify_folder, exist_ok=True)
for file in os.listdir(notify_folder):
    file_path = os.path.join(notify_folder, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

print("[INFO] Cleared 'notify' folder.")


# === NOTIFY FUNCTION ===
def run_notify():
    for i in range(1, notify_total + 1):
        screenshot = pyautogui.screenshot()
        width, height = screenshot.size
        resized_img = screenshot.resize(
            (int(width * resize_scale), int(height * resize_scale)),
            Image.Resampling.LANCZOS
        )
        filename = f"img_{i}.jpg"
        filepath = os.path.join(notify_folder, filename)
        resized_img.save(filepath, "JPEG", quality=jpeg_quality, optimize=True)
        print(f"[NOTIFY] Saved {filepath}")
        if i != notify_total:
            time.sleep(notify_interval)


# === MOTION DETECTION FUNCTION ===
def run_motion_detection():
    previous_frame = None
    while True:
        screenshot = pyautogui.screenshot()
        frame_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        if previous_frame is not None:
            diff = cv2.absdiff(previous_frame, frame_gray)
            score = np.sum(diff)

            if score > motion_threshold:
                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                hour_str = now.strftime("%H")
                folder_path = os.path.join(motion_base_folder, date_str, hour_str)
                os.makedirs(folder_path, exist_ok=True)

                resized_img = screenshot.resize(
                    (int(screenshot.width * resize_scale), int(screenshot.height * resize_scale)),
                    Image.Resampling.LANCZOS
                )

                filename = f"img_{now.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                filepath = os.path.join(folder_path, filename)
                resized_img.save(filepath, "JPEG", quality=jpeg_quality, optimize=True)
                print(f"[MOTION] Saved {filepath}")

        previous_frame = frame_gray
        time.sleep(motion_interval)


# === MAIN ===
notify_thread = Thread(target=run_notify)
motion_thread = Thread(target=run_motion_detection)

notify_thread.start()
motion_thread.start()

notify_thread.join()
