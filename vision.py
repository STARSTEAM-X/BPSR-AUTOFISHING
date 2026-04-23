import os
import sys

import cv2 as cv
import numpy as np
import pyautogui

from config import MINIGAME_MONITOR, ROIS, SCREEN_CHECKS


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


class VisionService:
    def __init__(self):
        self.left_template = self._load_template("img/left_arrow.png")
        self.right_template = self._load_template("img/right_arrow.png")

    def _load_template(self, path):
        template = cv.imread(resource_path(path), cv.IMREAD_GRAYSCALE)
        if template is None:
            raise FileNotFoundError(f"Template not found: {path}")
        return template

    def check_pixel(self, position, target_color, tolerance=10):
        x, y = position
        r, g, b = pyautogui.pixel(x, y)
        return (
            abs(r - target_color[0]) <= tolerance
            and abs(g - target_color[1]) <= tolerance
            and abs(b - target_color[2]) <= tolerance
        )

    def match_check(self, check_name):
        check = SCREEN_CHECKS[check_name]
        return all(
            self.check_pixel(position, color, check.tolerance)
            for position, color in check.points
        )

    def capture_status_flags(self):
        return {name: self.match_check(name) for name in SCREEN_CHECKS}

    def crop_roi(self, frame_gray, roi):
        rx, ry, rw, rh = roi
        x = rx - MINIGAME_MONITOR["left"]
        y = ry - MINIGAME_MONITOR["top"]
        return frame_gray[y : y + rh, x : x + rw]

    def detect_direction_edge(self, frame):
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
        left_roi = self.crop_roi(frame_gray, ROIS["left_arrow"])
        right_roi = self.crop_roi(frame_gray, ROIS["right_arrow"])

        def score_edge(roi, tpl):
            roi_blur = cv.GaussianBlur(roi, (5, 5), 0)
            tpl_blur = cv.GaussianBlur(tpl, (5, 5), 0)
            roi_edge = cv.Canny(roi_blur, 80, 160)
            tpl_edge = cv.Canny(tpl_blur, 80, 160)
            result = cv.matchTemplate(roi_edge, tpl_edge, cv.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv.minMaxLoc(result)
            return max_val

        left_score = score_edge(left_roi, self.left_template)
        right_score = score_edge(right_roi, self.right_template)
        min_signal = 0.5
        diff_threshold = 0.06

        if max(left_score, right_score) < min_signal:
            return None

        print(f"EDGE SCORE  L:{left_score:.3f}  R:{right_score:.3f}")

        if left_score - right_score > diff_threshold:
            return "LEFT"
        if right_score - left_score > diff_threshold:
            return "RIGHT"
        return None

    def debug_minigame(self, frame, direction):
        has_left = direction == "LEFT"
        has_right = direction == "RIGHT"
        debug_frame = frame.copy()

        lx, ly, lw, lh = ROIS["left_arrow"]
        rx, ry, rw, rh = ROIS["right_arrow"]
        mx = MINIGAME_MONITOR["left"]
        my = MINIGAME_MONITOR["top"]

        cv.rectangle(
            debug_frame,
            (lx - mx, ly - my),
            (lx - mx + lw, ly - my + lh),
            (255, 0, 0),
            2,
        )
        cv.rectangle(
            debug_frame,
            (rx - mx, ry - my),
            (rx - mx + rw, ry - my + rh),
            (0, 255, 255),
            2,
        )
        cv.putText(
            debug_frame,
            f"LEFT: {has_left}",
            (10, 20),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
        cv.putText(
            debug_frame,
            f"RIGHT: {has_right}",
            (10, 45),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
        cv.imshow("MINIGAME DEBUG", debug_frame)
        cv.waitKey(1)

    def frame_from_shot(self, shot):
        return np.array(shot)
