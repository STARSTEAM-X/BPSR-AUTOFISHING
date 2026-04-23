import keyboard
import pydirectinput
import pyautogui   # ✅ เพิ่มตัวนี้
import time
import os

RUNNING = False

pydirectinput.PAUSE = 0.05


def scroll_down(amount=800):
    """
    Scroll ลงก่อนกด F
    """
    print("SCROLLING DOWN...")
    pyautogui.scroll(-amount)   # ✅ ใช้ pyautogui แทน
    time.sleep(0.3)


def RUN_START():
    print("STARTING...")
    time.sleep(1)

    scroll_down(800)

    time.sleep(0.5)

    print("PRESSING T...")
    keyboard.press_and_release('t')   # ✅ กด T ก่อน
    time.sleep(0.3)

    print("PRESSING F...")
    keyboard.press_and_release('f')   # ✅ แล้วค่อยกด F

    time.sleep(1)

def start_bot():
    global RUNNING
    RUNNING = True
    print("BOT STARTED (F1)")


def stop_bot():
    global RUNNING
    RUNNING = False
    print("BOT STOPPED (F2)")


def hard_kill():
    print("HARD KILL (F4)")
    os._exit(0)


keyboard.add_hotkey('F1', start_bot)
keyboard.add_hotkey('F2', stop_bot)
keyboard.add_hotkey('F4', hard_kill)

print("BPSR_AUTO_F")
print("DEV : STARSTEAM_X")
print("Press F1 to START | F2 to STOP | F4 to EXIT")

while True:
    if not RUNNING:
        time.sleep(0.3)
        continue

    RUN_START()
    time.sleep(1)
    