import pyautogui
import keyboard
import time

print(" กด G เพื่ออ่านตำแหน่ง | กด ESC เพื่อออก")

last_pos = None

while True:
    # กด ESC ออก
    if keyboard.is_pressed("esc"):
        print("⛔ ออกจากโปรแกรม")
        break

    # ตรวจการคลิกซ้าย
    if keyboard.is_pressed("g"):
        x, y = pyautogui.position()       

        # กัน spam ถ้าค้างคลิก
        if last_pos != (x, y):
            r, g, b = pyautogui.pixel(x, y)
            print(f"📍 Position: ({x}, {y}) | 🎨 RGB: ({r}, {g}, {b})")
            last_pos = (x, y)

        time.sleep(0.2)

    time.sleep(0.05)
