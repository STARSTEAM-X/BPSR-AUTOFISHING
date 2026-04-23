import argparse
import time

import pyautogui
import pydirectinput


pydirectinput.PAUSE = 0.05


def get_position_and_color():
    x, y = pyautogui.position()
    r, g, b = pyautogui.pixel(x, y)
    return x, y, r, g, b


def move_mouse(x, y, duration):
    pydirectinput.moveTo(x, y, duration=duration)


def click_mouse():
    pydirectinput.mouseDown()
    time.sleep(0.08)
    pydirectinput.mouseUp()


def parse_position(value):
    cleaned = value.strip()
    if "=" in cleaned:
        _, cleaned = cleaned.split("=", 1)

    cleaned = cleaned.strip().replace("(", "").replace(")", "")
    parts = [part.strip() for part in cleaned.split(",")]

    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            "Position must be in the form 'x,y', '(x, y)', or 'position = (x, y)'."
        )

    try:
        return int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Position values must be integers."
        ) from exc


def build_parser():
    parser = argparse.ArgumentParser(
        description="Move mouse to a position and optionally click."
    )
    parser.add_argument(
        "position",
        nargs="?",
        type=parse_position,
        help="Target position in the form 'x,y', '(x, y)', or 'position = (x, y)'",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=0.15,
        help="Move duration in seconds",
    )
    parser.add_argument(
        "--click",
        action="store_true",
        help="Click after moving the mouse",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=0.0,
        help="Wait this many seconds before moving",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show current mouse position and RGB color",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.show or args.position is None:
        x, y, r, g, b = get_position_and_color()
        print(f"Position: ({x}, {y}) | RGB: ({r}, {g}, {b})")
        if args.position is None:
            return

    if args.wait > 0:
        print(f"Waiting {args.wait:.2f}s before move...")
        time.sleep(args.wait)

    x, y = args.position
    print(f"Moving mouse to ({x}, {y})")
    move_mouse(x, y, args.duration)

    x, y, r, g, b = get_position_and_color()
    print(f"Current: ({x}, {y}) | RGB: ({r}, {g}, {b})")

    if args.click:
        print("Clicking mouse")
        click_mouse()


if __name__ == "__main__":
    main()
