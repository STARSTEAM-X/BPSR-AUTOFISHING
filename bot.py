import os
import time

import keyboard
import mss
import pydirectinput

from config import (
    BAIT_ITEM_RULES,
    CLICK_POSITIONS,
    DEBUG,
    GameStatus,
    MINIGAME_MONITOR,
    POLE_ITEM_POSITIONS,
    SHOP_SLOT_CHECKS,
)
from vision import VisionService


pydirectinput.PAUSE = 0.05


class AutoFishingBot:
    def __init__(self):
        self.running = False
        self.current_key = None
        self.prev_status = None
        self.vision = VisionService()

    def determine_status(self, flags):
        if flags["start"]:
            return GameStatus.START
        if flags["monthly_reward"]:
            return GameStatus.MONTHLY_REWARD
        if flags["pole"] and flags["ui"] and flags["esc"]:
            return GameStatus.NO_FISHING_POLE
        if flags["bait"] and flags["ui"] and flags["esc"]:
            return GameStatus.NO_BAIT
        if flags["ui"] and flags["esc"]:
            return GameStatus.READY
        if flags["play"]:
            return GameStatus.PLAYING_MINIGAME
        if not flags["ui"] and flags["esc"] and not flags["continue"]:
            return GameStatus.WAITING
        if flags["exit"] and flags["continue"]:
            return GameStatus.CONTINUE
        return GameStatus.UNKNOWN

    def click_at(self, position):
        x, y = position
        time.sleep(0.15)
        pydirectinput.moveTo(x, y)
        time.sleep(0.15)
        print("Mouse at:", pydirectinput.position())
        pydirectinput.mouseDown()
        time.sleep(0.08)
        pydirectinput.mouseUp()
        time.sleep(0.15)

    def click_named(self, name):
        self.click_at(CLICK_POSITIONS[name])

    def close_bait(self):
        if self.vision.match_check("close_bait"):
            self.click_named("close_bait")

    def close_pole(self):
        if self.vision.match_check("close_pole"):
            self.click_named("close_pole")

    def buy_max(self):
        self.click_named("buy_max_open")
        time.sleep(0.1)
        self.click_named("buy_max_confirm")
        time.sleep(0.1)
        self.click_named("buy_max_apply")
        time.sleep(0.1)
        keyboard.press_and_release("esc")
        time.sleep(0.1)

    def find_items_can_buy(self):
        return sum(
            int(not self.vision.check_pixel(position, color))
            for position, color in SHOP_SLOT_CHECKS
        )

    def run_start(self):
        print("STARTING...")
        time.sleep(1)
        keyboard.press_and_release("f")
        time.sleep(1)

    def run_play(self):
        print("START FISHINGS...")
        self.close_bait()
        self.close_pole()
        time.sleep(1)
        self.click_named("screen_center")

    def hold_direction(self, direction):
        if direction == "LEFT":
            print("LEFT ARROW")
            if self.current_key != "a":
                keyboard.release("d")
                keyboard.press("a")
                self.current_key = "a"
            return

        if direction == "RIGHT":
            print("RIGHT ARROW")
            if self.current_key != "d":
                keyboard.release("a")
                keyboard.press("d")
                self.current_key = "d"
            return

        keyboard.release("a")
        keyboard.release("d")
        self.current_key = None

    def should_exit_minigame(self):
        return (
            self.vision.match_check("continue")
            or self.vision.match_check("exit")
            or self.vision.match_check("ui")
            or self.vision.match_check("monthly_reward")
        )

    def run_minigame(self):
        print("PLAYING MINIGAME...")
        self.current_key = None

        pydirectinput.moveTo(*CLICK_POSITIONS["screen_center"])
        time.sleep(0.15)
        pydirectinput.mouseDown()

        with mss.mss() as sct:
            while True:
                if self.should_exit_minigame():
                    self.click_named("screen_center")
                    time.sleep(0.1)
                    break

                shot = sct.grab(MINIGAME_MONITOR)
                frame = self.vision.frame_from_shot(shot)
                direction = self.vision.detect_direction_edge(frame)

                if DEBUG:
                    self.vision.debug_minigame(frame, direction)

                self.hold_direction(direction)
                time.sleep(0.03)

        pydirectinput.mouseUp()
        keyboard.release("a")
        keyboard.release("d")
        self.current_key = None
        time.sleep(0.4)

    def run_continue(self):
        print("CONTINUING...")
        self.click_named("continue")
        time.sleep(0.3)

    def choose_pole_item(self, unlocked_items):
        position = POLE_ITEM_POSITIONS.get(unlocked_items, POLE_ITEM_POSITIONS[0])
        self.click_at(position)

    def run_new_pole(self):
        keyboard.press("alt")
        time.sleep(0.1)
        self.click_named("pole_icon")
        time.sleep(0.3)

        if self.vision.match_check("buy_pole"):
            print("BUYING NEW POLE...")
            self.click_named("pole_shop")
            time.sleep(1)
            item_unlocked = self.find_items_can_buy()
            time.sleep(0.1)
            keyboard.release("alt")
            time.sleep(0.1)
            print("ITEMS CAN BUY:", item_unlocked)
            self.choose_pole_item(item_unlocked)
            self.buy_max()
            time.sleep(0.1)
            keyboard.press("alt")
            time.sleep(0.1)

        self.click_named("pole_close")
        time.sleep(0.1)
        keyboard.release("alt")
        time.sleep(1)

    def choose_bait_item(self, unlocked_items):
        for minimum_items, position in BAIT_ITEM_RULES:
            if unlocked_items >= minimum_items:
                self.click_at(position)
                return

    def run_replenish_bait(self):
        time.sleep(0.1)
        keyboard.press("alt")
        time.sleep(0.1)
        self.click_named("bait_icon")
        time.sleep(0.3)

        if self.vision.match_check("buy_new_bait"):
            print("BUYING BAIT...")
            self.click_named("bait_shop")
            time.sleep(1)
            item_unlocked = self.find_items_can_buy()
            time.sleep(0.1)
            keyboard.release("alt")
            time.sleep(0.1)
            print("ITEMS CAN BUY:", item_unlocked)
            self.choose_bait_item(item_unlocked)
            self.buy_max()
            time.sleep(0.1)
            keyboard.press("alt")
            time.sleep(0.1)

        self.click_named("bait_close")
        time.sleep(0.1)
        keyboard.release("alt")
        time.sleep(1)

    def claim_monthly_reward(self):
        print("CLAIMING MONTHLY REWARD...")
        self.click_named("monthly_reward")
        time.sleep(0.5)
        self.click_named("monthly_reward")
        time.sleep(1)

    def release_controls(self):
        keyboard.release("a")
        keyboard.release("d")
        keyboard.release("alt")
        pydirectinput.mouseUp()
        self.current_key = None

    def start(self):
        self.running = True
        print("BOT STARTED (F1)")

    def stop(self):
        self.running = False
        print("BOT STOPPED (F2)")
        self.release_controls()

    def hard_kill(self):
        print("HARD KILL (F4)")
        os._exit(0)

    def handle_status_change(self, status):
        if status == self.prev_status:
            return

        print("STATE CHANGED ->", status)

        if status == GameStatus.START:
            self.run_start()
        elif status == GameStatus.PLAYING_MINIGAME:
            self.run_minigame()

    def handle_status_action(self, status):
        if status == GameStatus.READY:
            self.run_play()
        elif status == GameStatus.CONTINUE:
            self.run_continue()
        elif status == GameStatus.NO_FISHING_POLE:
            self.run_new_pole()
        elif status == GameStatus.NO_BAIT:
            self.run_replenish_bait()
        elif status == GameStatus.MONTHLY_REWARD:
            self.claim_monthly_reward()

    def print_debug(self, flags, status):
        print("START:", flags["start"])
        print("UI   :", flags["ui"])
        print("ESC  :", flags["esc"])
        print("PLAY :", flags["play"])
        print("STATUS:", status)
        print("-" * 20)

    def tick(self):
        flags = self.vision.capture_status_flags()
        status = self.determine_status(flags)
        self.handle_status_change(status)
        self.prev_status = status
        self.handle_status_action(status)

        if DEBUG:
            self.print_debug(flags, status)

    def run_forever(self):
        keyboard.add_hotkey("F1", self.start)
        keyboard.add_hotkey("F2", self.stop)
        keyboard.add_hotkey("F4", self.hard_kill)

        print("BPSR_AUTOFISHING")
        print("DEV : STARSTEAM_X")
        print("Press F1 to START | F2 to STOP | F4 to EXIT")

        while True:
            if not self.running:
                time.sleep(0.5)
                continue

            self.tick()
            time.sleep(0.3)
