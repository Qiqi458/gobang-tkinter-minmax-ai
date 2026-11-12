"""Tkinter 主窗口和对局流程。"""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Optional

from configure.settings import config
from core.AI import MinimaxAI
from core.game import GobangGame
from gui.components.board import BoardCanvas
from gui.components.control import ControlPanel


class GobangApp:
    """Qiqi 五子棋桌面应用。"""

    def __init__(self, master: tk.Tk):
        self.master = master
        self.game = GobangGame()
        self.ai: Optional[MinimaxAI] = None
        self._setup_window()
        self._create_widgets()
        self._restart()
        self.master.bind("<Control-n>", lambda _event: self._start())
        self.master.bind("<Escape>", lambda _event: self._quit())

    def _setup_window(self) -> None:
        self.master.title("Qiqi 五子棋")
        self.master.configure(bg=config.APP_BG)
        self.master.resizable(False, False)
        board_side = (config.BOARD_SIZE - 1) * config.GRID_SIZE + 2 * config.MARGIN
        width = board_side + 230 + 3 * 14 + 44
        height = max(board_side + 44, 620)
        self.master.geometry(f"{width}x{height}")
        self.master.minsize(width, height)
        icon_path = Path(__file__).with_name("gobang.ico")
        if icon_path.exists():
            try:
                self.master.iconbitmap(str(icon_path))
            except tk.TclError:
                pass

    def _create_widgets(self) -> None:
        shell = tk.Frame(self.master, bg=config.APP_BG, padx=22, pady=22)
        shell.pack(fill="both", expand=True)
        self.board = BoardCanvas(shell, on_click=self._on_board_click)
        self.board.pack(side="left", padx=(0, 18))
        self.control = ControlPanel(
            shell, on_start=self._start, on_quit=self._quit
        )
        self.control.pack(side="left", fill="y")

    def _on_board_click(self, row: int, col: int) -> None:
        state = self.game.get_current_state()
        if state == config.State.READY:
            return
        if self.ai and state == config.State.WHITE_TURN:
            return
        self._handle_move_result(row, col)

    def _handle_move_result(self, row: int, col: int) -> None:
        result = self.game.make_move(row, col)
        if not result.valid:
            return
        self._update_display(row, col)
        if result.game_over:
            self._handle_game_over(result.game_state)
        elif self.ai and self.game.get_current_state() == config.State.WHITE_TURN:
            self.control.update_status("AI 正在思考…")
            self.master.after(int(config.AI_DELAY * 1000), self._ai_move)

    def _handle_game_over(self, state: int) -> None:
        winning_line = self.game.get_winning_line()
        if winning_line:
            self.board.highlight_winning_line(winning_line)
        message = config.StateText.get(state, config.StateText[config.State.UNKNOWN])
        if messagebox.askyesno("对局结束", f"{message}\n\n要再来一局吗？", parent=self.master):
            self._start()
        else:
            self._quit()

    def _ai_move(self) -> None:
        if not self.ai or self.game.get_current_state() != config.State.WHITE_TURN:
            return
        move = self.ai.get_move()
        if move is not None:
            self._handle_move_result(*move)

    def _update_display(self, row: int, col: int) -> None:
        is_black = self.game.board[row][col] == config.State.BLACK_TURN
        self.board.draw_piece(row, col, is_black=is_black)
        self._update_status()

    def _update_status(self) -> None:
        state = self.game.get_current_state()
        self.control.update_status(
            config.StateText.get(state, config.StateText[config.State.UNKNOWN])
        )

    def _create_ai(self) -> Optional[MinimaxAI]:
        if self.control.get_game_mode() == "pvc":
            return MinimaxAI(self.game, depth=3)
        return None

    def _start(self) -> None:
        self.game.reset_game()
        self.game.set_current_state(config.State.BLACK_TURN)
        self.board.clear_piece()
        self.ai = self._create_ai()
        self._update_status()

    def _restart(self) -> None:
        self.board.clear_piece()
        self.game.reset_game()
        self.ai = None
        self._update_status()

    def _quit(self) -> None:
        self.master.destroy()