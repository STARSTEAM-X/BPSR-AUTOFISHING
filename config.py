from dataclasses import dataclass


@dataclass(frozen=True)
class PixelCheck:
    points: tuple
    tolerance: int = 10


class GameStatus:
    START = "START"
    MONTHLY_REWARD = "MONTHLY REWARD"
    NO_FISHING_POLE = "NOT HAVE FISHING POLE"
    NO_BAIT = "NOT HAVE BAIT"
    READY = "READY"
    PLAYING_MINIGAME = "PLAYING MINIGAME"
    WAITING = "WAITING"
    CONTINUE = "CONTINUE"
    UNKNOWN = "UNKNOWN"


DEBUG = False

MINIGAME_MONITOR = {
    "left": 740,
    "top": 480,
    "width": 450,
    "height": 130,
}

ROIS = {
    "left_arrow": (740, 490, 220, 100),
    "right_arrow": (960, 490, 220, 100),
}

SCREEN_CHECKS = {
    "start": PixelCheck((((1432, 565), (255, 255, 255)),)),
    "ui": PixelCheck((((1107, 1005), (242, 246, 246)),)),
    "esc": PixelCheck((((40, 50), (51, 51, 51)),)),
    "play": PixelCheck((((959, 558), (255, 91, 2)),)),
    "exit": PixelCheck((((1127, 978), (232, 232, 232)),)),
    "continue": PixelCheck((((1459, 978), (232, 232, 232)),)),
    "pole": PixelCheck((((1666, 1014), (211, 211, 211)),)),
    "bait": PixelCheck((((1399, 1015), (211, 211, 211)),)),
    "monthly_reward": PixelCheck(
        (
            ((817, 1047), (210, 197, 177)),
            ((892, 1050), (216, 200, 178)),
            ((953, 1045), (218, 201, 178)),
            ((1014, 1046), (219, 201, 178)),
            ((1059, 1049), (216, 200, 177)),
        )
    ),
    "buy_new_bait": PixelCheck(
        (
            ((1001, 902), (232, 232, 232)),
            ((1369, 900), (232, 232, 232)),
        )
    ),
    "buy_pole": PixelCheck(
        (
            ((1270, 902), (232, 232, 232)),
            ((1612, 904), (232, 232, 232)),
        )
    ),
    "close_bait": PixelCheck((((1540, 507), (241, 94, 14)),)),
    "close_pole": PixelCheck((((1808, 507), (251, 97, 2)),)),
}

SHOP_SLOT_CHECKS = (
    ((724, 449), (124, 124, 124)),
    ((952, 450), (124, 124, 124)),
    ((1190, 450), (124, 124, 124)),
    ((1418, 452), (124, 124, 124)),
)

CLICK_POSITIONS = {
    "screen_center": (960, 540),
    "continue": (1459, 978),
    "monthly_reward": (949, 912),
    "bait_icon": (1399, 1015),
    "close_bait": (1540, 507),
    "bait_shop": (1186, 902),
    "bait_close": (1449, 596),
    "pole_icon": (1666, 1014),
    "close_pole": (1808, 507),
    "pole_shop": (1453, 902),
    "pole_close": (1716, 594),
    "buy_max_open": (1564, 729),
    "buy_max_confirm": (1215, 926),
    "buy_max_apply": (1197, 798),
}

POLE_ITEM_POSITIONS = {
    4: (1464, 318),
    3: (1225, 316),
    2: (996, 308),
    1: (772, 317),
    0: (532, 319),
}

BAIT_ITEM_RULES = (
    (3, (771, 309)),
    (1, (544, 322)),
    (0, (309, 310)),
)
