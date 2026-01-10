import pyautogui 
import time
import keyboard
import pydirectinput
import mss
import cv2 as cv
import numpy as np

pydirectinput.PAUSE = 0.05


DEBUG = False
STATUS = None
PREV_STATUS = None

LEFT_TEMPLATE  = cv.imread("img/left_arrow.png",  cv.IMREAD_GRAYSCALE)
RIGHT_TEMPLATE = cv.imread("img/right_arrow.png", cv.IMREAD_GRAYSCALE)

MINIGAME_MONITOR = {
    "left": 740,
    "top": 480,
    "width": 450,
    "height": 130
}

rois = {
    "left_arrow":  (740, 490, 220, 100),
    "right_arrow": (960, 490, 220, 100)
}



def check_pixel(position, target_color, tolerance=10):
    x, y = position
    r, g, b = pyautogui.pixel(x, y)

    return (
        abs(r - target_color[0]) <= tolerance and
        abs(g - target_color[1]) <= tolerance and
        abs(b - target_color[2]) <= tolerance
    )

def detect_direction_edge(left_roi, right_roi, left_tpl, right_tpl):
    def score_edge(roi, tpl):
        # blur ลด noise
        roi_blur = cv.GaussianBlur(roi, (5,5), 0)
        tpl_blur = cv.GaussianBlur(tpl, (5,5), 0)

        # edge detection (ไม่สนสี)
        roi_edge = cv.Canny(roi_blur, 80, 160)
        tpl_edge = cv.Canny(tpl_blur, 80, 160)

        # match template
        res = cv.matchTemplate(roi_edge, tpl_edge, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)
        return max_val

    left_score  = score_edge(left_roi,  left_tpl)
    right_score = score_edge(right_roi, right_tpl)

    MIN_SIGNAL = 0.5

    if max(left_score, right_score) < MIN_SIGNAL:
        return None

    print(f"EDGE SCORE  L:{left_score:.3f}  R:{right_score:.3f}")

    DIFF = 0.06   # ปรับได้ 0.04–0.08

    if left_score - right_score > DIFF:
        return "LEFT"
    elif right_score - left_score > DIFF:
        return "RIGHT"
    else:
        return None



def crop_roi(frame_gray, roi, monitor):
    """
    roi: (x, y, w, h) อิงจากจอจริง
    monitor: MINIGAME_MONITOR
    """
    rx, ry, rw, rh = roi

    mx = monitor["left"]
    my = monitor["top"]

    # แปลงเป็นพิกัดภายใน frame
    x = rx - mx
    y = ry - my

    return frame_gray[y:y+rh, x:x+rw]

def debug_minigame(frame, left_roi, right_roi, text):

    if text == "LEFT": has_left = True
    else: has_left = False
    if text == "RIGHT": has_right = True
    else: has_right = False

    debug = frame.copy()

    # วาดกรอบ ROI (สีฟ้า = ซ้าย, สีเหลือง = ขวา)
    lx, ly, lw, lh = rois["left_arrow"]
    rx, ry, rw, rh = rois["right_arrow"]

    mx = MINIGAME_MONITOR["left"]
    my = MINIGAME_MONITOR["top"]

    cv.rectangle(
        debug,
        (lx - mx, ly - my),
        (lx - mx + lw, ly - my + lh),
        (255, 0, 0),
        2
    )

    cv.rectangle(
        debug,
        (rx - mx, ry - my),
        (rx - mx + rw, ry - my + rh),
        (0, 255, 255),
        2
    )

    # ข้อความผลลัพธ์
    cv.putText(debug, f"LEFT: {has_left}", (10, 20),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.putText(debug, f"RIGHT: {has_right}", (10, 45),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv.imshow("MINIGAME DEBUG", debug)
    cv.waitKey(1)


def find_start():
    return check_pixel((1432, 565), (255, 255, 255))

def find_UI():
    return check_pixel((1107, 1005), (242, 246, 246))

def find_esc():
    return check_pixel((40, 50), (51, 51, 51))

def find_play():
    return check_pixel((959, 558), (255, 91, 2))

def find_exit():
    return check_pixel((1127, 978), (232, 232, 232))

def find_continue():
    return check_pixel((1459, 978), (232, 232, 232))

def find_pole():
    return check_pixel((1666, 1014), (211, 211, 211))

def find_bait():
    return check_pixel((1399, 1015), (211, 211, 211))

def find_minigame_left():
    return (
        check_pixel((870, 536), (236, 76, 34)) or
        check_pixel((942, 538), (194, 67, 36)) or
        check_pixel((868, 539), (186, 63, 38)) or
        check_pixel((836, 539), (185, 95, 40))
    )

def find_monthly_reward():
    return (
        check_pixel((734, 465), (238, 226, 213)) and
        check_pixel((821, 380), (31, 144, 150)) and
        check_pixel((1098, 542), (113, 85, 80))
    )

def find_buynewbait():
    return (
        check_pixel((1001, 902), (232, 232, 232)) and 
        check_pixel((1369, 900), (232, 232, 232)) 
    )

def find_buypole():
    return (
        check_pixel((1270, 902), (232, 232, 232)) and 
        check_pixel((1612, 904), (232, 232, 232)) 
    )

def find_minigame_right():
    return check_pixel((1050, 538), (252, 77, 6))



def click_at(position):
    x, y = position
    time.sleep(0.15)
    pydirectinput.moveTo(x, y)
    time.sleep(0.15)
    print("Mouse at:", pydirectinput.position())
    pydirectinput.mouseDown()
    time.sleep(0.08)
    pydirectinput.mouseUp()
    time.sleep(0.15)

def RUN_START():
    print("STARTING...")
    time.sleep(1)
    keyboard.press_and_release('f')
    time.sleep(1)

def RUN_PLAY():
    print("START FISHINGS...")
    close_bait()
    close_pole()
    time.sleep(1)
    click_at((960, 540))

def RUN_MINIGAME():
    global current_key
    current_key = None

    print("PLAYING MINIGAME...")

    pydirectinput.moveTo(960, 540)
    time.sleep(0.15)
    pydirectinput.mouseDown()

    with mss.mss() as sct:
        while True:
            # ออกจาก minigame (ยังใช้ pixel ได้ก่อน)
            if find_continue() or find_exit() or find_UI():
                break

            # 1️⃣ capture ใหญ่ครั้งเดียว
            shot = sct.grab(MINIGAME_MONITOR)
            frame = np.array(shot)
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)

            # 2️⃣ ตัด ROI ซ้าย / ขวา
            left_roi  = crop_roi(frame_gray, rois["left_arrow"],  MINIGAME_MONITOR)
            right_roi = crop_roi(frame_gray, rois["right_arrow"], MINIGAME_MONITOR)

            # 3️⃣ ตรวจหา arrow
            direction = detect_direction_edge(
                left_roi,
                right_roi,
                LEFT_TEMPLATE,
                RIGHT_TEMPLATE
            )

            if DEBUG:
                debug_minigame(frame, left_roi, right_roi, direction)

            if direction == "LEFT":
                print("LEFT ARROW")
                if current_key != 'a':
                    keyboard.release('d')
                    keyboard.press('a')
                    current_key = 'a'

            elif direction == "RIGHT":
                print("RIGHT ARROW")
                if current_key != 'd':
                    keyboard.release('a')
                    keyboard.press('d')
                    current_key = 'd'

            else:
                current_key = None

            time.sleep(0.03)

    pydirectinput.mouseUp()
    keyboard.release('a')
    keyboard.release('d')
    current_key = None
    time.sleep(0.4)

def RUN_CONTINUE():
    print("CONTINUING...")
    click_at((1459, 978))
    time.sleep(0.3)
    
def find_itemcanbuy():
    return (
        int(not check_pixel((724, 449), (124, 124, 124))) +
        int(not check_pixel((952, 450), (124, 124, 124))) +
        int(not check_pixel((1190, 450), (124, 124, 124))) +
        int(not check_pixel((1418, 452), (124, 124, 124)))
    )

def close_bait():
    if check_pixel((1540, 507), (241, 94, 14)):
        click_at((1540, 507))

def close_pole():
    if check_pixel((1808, 507), (251, 97, 2)):
        click_at((1808, 507))

def buy_MAX():
    click_at((1564, 729))
    time.sleep(0.1)
    click_at((1215, 926))
    time.sleep(0.1)
    click_at((1197, 798))
    time.sleep(0.1)
    keyboard.press_and_release('esc')
    time.sleep(0.1)

def RUN_NEWPOLE():
    keyboard.press('alt')
    time.sleep(0.1)
    click_at((1666, 1014))
    time.sleep(0.3)
    if find_buypole():
        print("BUYING NEW POLE...")
        click_at((1453, 902))
        time.sleep(1)
        itemunlocked = find_itemcanbuy()
        time.sleep(0.1)
        keyboard.release('alt')
        time.sleep(0.1)
        print("ITEMS CAN BUY:", itemunlocked)
        if itemunlocked == 4:
            click_at((1464, 318))
            buy_MAX()
        elif itemunlocked == 3:
            click_at((1225, 316))
            buy_MAX()
        elif itemunlocked == 2:
            click_at((996, 308))
            buy_MAX()
        elif itemunlocked == 1:
            click_at((772, 317))
            buy_MAX()
        elif itemunlocked >= 0:
            click_at((532, 319))
            buy_MAX()
        time.sleep(0.1)
        keyboard.press('alt')
        time.sleep(0.1)
    click_at((1716, 594))
    time.sleep(0.1)
    keyboard.release('alt')
    time.sleep(1)

def RUN_REPLENISH_BAIT():
    time.sleep(0.1)
    keyboard.press('alt')
    time.sleep(0.1)
    click_at((1399, 1015))
    time.sleep(0.3)
    if find_buynewbait():
        print("BUYING BAIT...")
        click_at((1186, 902))
        time.sleep(1)
        itemunlocked = find_itemcanbuy()
        time.sleep(0.1)
        keyboard.release('alt')
        time.sleep(0.1)
        print("ITEMS CAN BUY:", itemunlocked)
        if itemunlocked >= 3:
            click_at((771, 309))
            buy_MAX()
        elif itemunlocked >= 1:
            click_at((544, 322))
            buy_MAX()
        elif itemunlocked == 0:
            click_at((309, 310))
            buy_MAX()
        time.sleep(0.1)
        keyboard.press('alt')
        time.sleep(0.1)
    click_at((1449, 596))
    time.sleep(0.1)
    keyboard.release('alt')
    time.sleep(1)

while True:
    status_start = find_start()
    status_ui = find_UI()
    status_esc = find_esc()
    status_play = find_play()
    status_exit = find_exit()
    status_continue = find_continue()
    status_pole = find_pole()
    status_bait = find_bait()
    status_monthly = find_monthly_reward()

    if status_start:
        STATUS = "START"
    elif status_monthly:
        STATUS = "MONTHLY REWARD"
    elif status_pole and status_ui and status_esc:
        STATUS = "NOT HAVE FISHING POLE"
    elif status_bait and status_ui and status_esc:
        STATUS = "NOT HAVE BAIT"
    elif status_ui and status_esc:
        STATUS = "READY"
    elif status_play:
        STATUS = "PLAYING MINIGAME"
    elif not status_ui and status_esc:
        STATUS = "WAITING"
    elif status_exit and status_continue:
        STATUS = "CONTINUE"
    else:
        STATUS = "UNKNOWN"


    # ---------- ACTION (เฉพาะตอนเปลี่ยนสถานะ) ----------
    if STATUS != PREV_STATUS:
        print("STATE CHANGED →", STATUS)

        if STATUS == "START":
            RUN_START()

        elif STATUS == "PLAYING MINIGAME":
            RUN_MINIGAME()

        elif STATUS == "CONTINUE":
            RUN_CONTINUE()

    PREV_STATUS = STATUS

    if STATUS == "READY":
        RUN_PLAY()

    elif STATUS == "NOT HAVE FISHING POLE":
        RUN_NEWPOLE()

    elif STATUS == "NOT HAVE BAIT":
        RUN_REPLENISH_BAIT()

    elif STATUS == "MONTHLY REWARD":
        print("CLAIMING MONTHLY REWARD...")
        click_at((949, 912))
        time.sleep(1)


    # ---------- DEBUG ----------

    if DEBUG:
        print("START:", status_start)
        print("UI   :", status_ui)
        print("ESC  :", status_esc)
        print("PLAY :", status_play)
        print("STATUS:", STATUS)
        print("-" * 20)

    time.sleep(0.3)