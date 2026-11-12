"""界面和对局共用设置。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    BOARD_SIZE: int = 15
    GRID_SIZE: int = 38
    PIECE_RADIUS: int = 15
    MARGIN: int = 34

    # 深色界面搭配暖木色棋盘。
    APP_BG: str = "#111827"
    PANEL_BG: str = "#1F2937"
    PANEL_RAISED: str = "#273449"
    TEXT_COLOR: str = "#F3F4F6"
    MUTED_TEXT: str = "#C5CDD8"
    ACCENT: str = "#F4B860"
    ACCENT_HOVER: str = "#FFD18A"
    BOARD_COLOR: str = "#D9B779"
    LINE_COLOR: str = "#735B3E"
    BLACK_PIECE: str = "#17202A"
    WHITE_PIECE: str = "#FFFDF7"
    HIGHLIGHT_COLOR: str = "#F06A5B"
    BUTTON_BG: str = "#F4B860"
    BUTTON_FG: str = "#17202A"

    AI_DELAY: float = 0.45
    AI_SEARCH_SECONDS: float = 0.8

    class State:
        READY = 0
        BLACK_TURN = 1
        WHITE_TURN = 2
        BLACK_WIN = 3
        WHITE_WIN = 4
        DRAW = 5
        UNKNOWN = -1

    StateText = {
        State.READY: "点击「开始对局」落下第一子",
        State.BLACK_TURN: "黑棋回合",
        State.WHITE_TURN: "白棋回合",
        State.BLACK_WIN: "黑棋获胜",
        State.WHITE_WIN: "白棋获胜",
        State.DRAW: "平局",
        State.UNKNOWN: "未知状态",
    }


config = GameConfig()