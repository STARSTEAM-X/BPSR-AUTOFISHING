import pyautogui
import time

MINIGAME_REGION = (740, 450, 450, 130)  # (x, y, w, h)

time.sleep(2)  # ให้คุณ alt-tab กลับเข้าเกมก่อน

img = pyautogui.screenshot(region=MINIGAME_REGION)
img.save("minigame_region.png")

print("✅ Saved: minigame_region.png")
