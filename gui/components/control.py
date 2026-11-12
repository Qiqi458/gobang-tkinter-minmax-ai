"""显示模式、状态和操作的控制面板。"""

import tkinter as tk
from typing import Callable

from configure.settings import config


class ControlPanel(tk.Frame):
    """与深色主窗口配套的游戏控制面板。"""

    def __init__(self, master, on_start: Callable[[], None], on_quit: Callable[[], None]):
        super().__init__(master, bg=config.PANEL_BG, padx=22, pady=22, width=230)
        self.pack_propagate(False)
        self.on_start = on_start
        self.on_quit = on_quit
        self.mode_var = tk.StringVar(value="pvp")
        self.status_var = tk.StringVar(value=config.StateText[config.State.READY])
        self._create_widgets()

    def _create_widgets(self) -> None:
        tk.Label(
            self, text="QIQI  /  五子棋", bg=config.PANEL_BG,
            fg=config.ACCENT, font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            self, text="五子棋", bg=config.PANEL_BG, fg=config.TEXT_COLOR,
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w", pady=(3, 18))

        tk.Label(
            self, text="当前状态", bg=config.PANEL_BG, fg=config.MUTED_TEXT,
            font=("Segoe UI", 9),
        ).pack(anchor="w")
        self.status_label = tk.Label(
            self, textvariable=self.status_var, bg=config.PANEL_RAISED,
            fg=config.TEXT_COLOR, font=("Segoe UI", 11, "bold"),
            justify="left", anchor="w", wraplength=185, padx=12, pady=12,
        )
        self.status_label.pack(fill="x", pady=(6, 20))

        tk.Label(
            self, text="对局模式", bg=config.PANEL_BG, fg=config.MUTED_TEXT,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(0, 7))
        for label, value in (("双人对弈", "pvp"), ("人机对弈 · 智能棋手", "pvc")):
            tk.Radiobutton(
                self, text=label, value=value, variable=self.mode_var,
                bg=config.PANEL_BG, fg=config.TEXT_COLOR,
                activebackground=config.PANEL_BG, activeforeground=config.ACCENT,
                selectcolor=config.PANEL_RAISED, font=("Segoe UI", 10),
                anchor="w", padx=0, pady=4,
            ).pack(fill="x")

        self.start_button = tk.Button(
            self, text="开始对局", command=self.on_start,
            bg=config.ACCENT, fg=config.BUTTON_FG,
            activebackground=config.ACCENT_HOVER, activeforeground=config.BUTTON_FG,
            relief="flat", bd=0, font=("Segoe UI", 11, "bold"),
            cursor="hand2", pady=11,
        )
        self.start_button.pack(fill="x", pady=(22, 8))
        tk.Button(
            self, text="退出", command=self.on_quit,
            bg=config.PANEL_RAISED, fg=config.MUTED_TEXT,
            activebackground="#34445A", activeforeground=config.TEXT_COLOR,
            relief="flat", bd=0, font=("Segoe UI", 10),
            cursor="hand2", pady=9,
        ).pack(fill="x")
        tk.Label(
            self, text="点击棋盘交叉点落子\n先连成五子的一方获胜",
            bg=config.PANEL_BG, fg=config.MUTED_TEXT,
            font=("Segoe UI", 9), justify="left",
        ).pack(anchor="w", side="bottom", pady=(20, 0))

    def update_status(self, status: str) -> None:
        self.status_var.set(status)

    def get_game_mode(self) -> str:
        return self.mode_var.get()