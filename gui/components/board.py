"""五子棋棋盘的绘制与鼠标输入。"""

import tkinter as tk
from typing import Callable, List, Tuple

from configure.settings import config


class BoardCanvas(tk.Canvas):
    """绘制 15×15 棋盘并处理鼠标落子。"""

    def __init__(self, master, on_click: Callable[[int, int], None]):
        side = (config.BOARD_SIZE - 1) * config.GRID_SIZE + 2 * config.MARGIN
        super().__init__(
            master,
            width=side,
            height=side,
            bg=config.BOARD_COLOR,
            highlightthickness=0,
            cursor="crosshair",
        )
        self.on_click = on_click
        self.last_click_time = 0.0
        self._draw_grid()
        self.bind("<Button-1>", self._handle_click)

    def _point(self, row: int, col: int) -> Tuple[int, int]:
        return (
            config.MARGIN + col * config.GRID_SIZE,
            config.MARGIN + row * config.GRID_SIZE,
        )

    def _draw_grid(self) -> None:
        end = config.MARGIN + (config.BOARD_SIZE - 1) * config.GRID_SIZE
        for index in range(config.BOARD_SIZE):
            offset = config.MARGIN + index * config.GRID_SIZE
            self.create_line(offset, config.MARGIN, offset, end, fill=config.LINE_COLOR, width=1)
            self.create_line(config.MARGIN, offset, end, offset, fill=config.LINE_COLOR, width=1)
        for row in (3, 7, 11):
            for col in (3, 7, 11):
                x, y = self._point(row, col)
                self.create_oval(x - 3, y - 3, x + 3, y + 3, fill=config.LINE_COLOR, outline="")

    def draw_piece(self, row: int, col: int, is_black: bool) -> None:
        self.delete("last_move")
        x, y = self._point(row, col)
        fill = config.BLACK_PIECE if is_black else config.WHITE_PIECE
        outline = "#0B1118" if is_black else "#C8C1B3"
        self.create_oval(
            x - config.PIECE_RADIUS + 2,
            y - config.PIECE_RADIUS + 3,
            x + config.PIECE_RADIUS + 2,
            y + config.PIECE_RADIUS + 3,
            fill="#8B7356",
            outline="",
            tags=("piece",),
        )
        self.create_oval(
            x - config.PIECE_RADIUS,
            y - config.PIECE_RADIUS,
            x + config.PIECE_RADIUS,
            y + config.PIECE_RADIUS,
            fill=fill,
            outline=outline,
            width=1,
            tags=("piece",),
        )
        self.create_oval(x - 3, y - 3, x + 3, y + 3, fill=config.HIGHLIGHT_COLOR, outline="", tags=("last_move",))

    def clear_piece(self) -> None:
        self.delete("piece", "highlight", "last_move")

    def _nearest_cell(self, x: int, y: int):
        col = round((x - config.MARGIN) / config.GRID_SIZE)
        row = round((y - config.MARGIN) / config.GRID_SIZE)
        if not (0 <= row < config.BOARD_SIZE and 0 <= col < config.BOARD_SIZE):
            return None
        px, py = self._point(row, col)
        if abs(x - px) > config.GRID_SIZE * 0.48 or abs(y - py) > config.GRID_SIZE * 0.48:
            return None
        return row, col

    def _handle_click(self, event) -> None:
        cell = self._nearest_cell(event.x, event.y)
        if cell is not None:
            self.on_click(*cell)

    def highlight_winning_line(self, winning_line: List[Tuple[int, int]]) -> None:
        for row, col in winning_line:
            x, y = self._point(row, col)
            radius = config.PIECE_RADIUS + 3
            self.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                outline=config.HIGHLIGHT_COLOR, width=3, tags=("highlight",),
            )