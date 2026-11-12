"""限时 α-β 搜索五子棋 AI。"""

import math
import time
from typing import List, Optional, Tuple

from configure.settings import config
from core.game import GobangGame

Move = Tuple[int, int]


class BaseAI:
    """电脑对手的基础接口。"""

    def __init__(self, game: GobangGame):
        self.game = game

    def get_move(self) -> Optional[Move]:
        raise NotImplementedError


class MinimaxAI(BaseAI):
    """使用限深 α-β 搜索，并优先处理直接获胜和防守。"""

    DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    WIN_SCORE = 1_000_000

    def __init__(self, game: GobangGame, depth: int = 2):
        super().__init__(game)
        self.depth = max(1, depth)
        self.ai_piece = config.State.WHITE_TURN
        self.human_piece = config.State.BLACK_TURN
        self.deadline = 0.0
        self.nodes = 0
        self.evaluation_cache = {}
        self.cache_hits = 0

    def get_move(self) -> Optional[Move]:
        started = time.perf_counter()
        board = self.game.board
        candidates = self._candidates(board)
        if not candidates:
            return None
        if all(cell is None for row in board for cell in row):
            center = config.BOARD_SIZE // 2
            return center, center

        # 优先落下必胜棋，也要及时堵住对手的直接胜势。
        for piece in (self.ai_piece, self.human_piece):
            for move in candidates:
                row, col = move
                board[row][col] = piece
                try:
                    if self._wins_at(board, move, piece):
                        return move
                finally:
                    board[row][col] = None

        self.deadline = time.monotonic() + config.AI_SEARCH_SECONDS
        self.nodes = 0
        self.evaluation_cache = {}
        self.cache_hits = 0
        best_move = candidates[0]
        best_score = -math.inf
        alpha, beta = -math.inf, math.inf
        for move in candidates:
            if time.monotonic() >= self.deadline:
                break
            row, col = move
            board[row][col] = self.ai_piece
            try:
                if self._wins_at(board, move, self.ai_piece):
                    score = self.WIN_SCORE
                else:
                    score = self._search(board, self.depth - 1, alpha, beta, False, move)
            finally:
                board[row][col] = None
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, best_score)
        elapsed = time.perf_counter() - started
        print(f"AI思考时间: {elapsed:.2f}s, 缓存命中: {self.cache_hits}")
        return best_move

    def _candidates(self, board: List[List[Optional[int]]]) -> List[Move]:
        occupied = [
            (row, col)
            for row in range(config.BOARD_SIZE)
            for col in range(config.BOARD_SIZE)
            if board[row][col] is not None
        ]
        if not occupied:
            center = config.BOARD_SIZE // 2
            return [(center, center)]
        nearby = set()
        for row, col in occupied:
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    r, c = row + dr, col + dc
                    if 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE and board[r][c] is None:
                        nearby.add((r, c))
        return sorted(nearby, key=lambda move: self._move_order(board, move), reverse=True)[:12]

    def _move_order(self, board: List[List[Optional[int]]], move: Move) -> int:
        row, col = move
        score = 0
        for dr, dc in self.DIRECTIONS:
            for piece in (self.ai_piece, self.human_piece):
                count = 0
                for step in range(-4, 5):
                    r, c = row + dr * step, col + dc * step
                    if 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE and board[r][c] == piece:
                        count += 1
                score += count * count * (2 if piece == self.ai_piece else 3)
        center = config.BOARD_SIZE // 2
        score -= abs(row - center) + abs(col - center)
        return score

    def _wins_at(self, board: List[List[Optional[int]]], move: Move, piece: int) -> bool:
        row, col = move
        if board[row][col] != piece:
            return False
        for dr, dc in self.DIRECTIONS:
            count = 1
            for sign in (-1, 1):
                r, c = row + sign * dr, col + sign * dc
                while 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE and board[r][c] == piece:
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= 5:
                return True
        return False

    def _search(self, board, depth: int, alpha: float, beta: float, maximizing: bool, last_move: Move) -> float:
        self.nodes += 1
        if self._wins_at(board, last_move, self.ai_piece):
            return self.WIN_SCORE + depth
        if self._wins_at(board, last_move, self.human_piece):
            return -self.WIN_SCORE - depth
        if depth <= 0 or time.monotonic() >= self.deadline:
            return self._evaluate(board)
        moves = self._candidates(board)
        if not moves:
            return 0

        if maximizing:
            value = -math.inf
            piece = self.ai_piece
            for move in moves:
                row, col = move
                board[row][col] = piece
                try:
                    score = self._search(board, depth - 1, alpha, beta, False, move)
                finally:
                    board[row][col] = None
                value = max(value, score)
                alpha = max(alpha, value)
                if beta <= alpha or time.monotonic() >= self.deadline:
                    break
            return value
        value = math.inf
        piece = self.human_piece
        for move in moves:
            row, col = move
            board[row][col] = piece
            try:
                score = self._search(board, depth - 1, alpha, beta, True, move)
            finally:
                board[row][col] = None
            value = min(value, score)
            beta = min(beta, value)
            if beta <= alpha or time.monotonic() >= self.deadline:
                break
        return value

    def _evaluate(self, board) -> float:
        key = tuple(tuple(row) for row in board)
        cached = self.evaluation_cache.get(key)
        if cached is not None:
            self.cache_hits += 1
            return cached
        score = 0
        size = config.BOARD_SIZE
        for row in range(size):
            for col in range(size):
                for dr, dc in self.DIRECTIONS:
                    end_row, end_col = row + 4 * dr, col + 4 * dc
                    if not (0 <= end_row < size and 0 <= end_col < size):
                        continue
                    cells = [board[row + i * dr][col + i * dc] for i in range(5)]
                    ai_count = cells.count(self.ai_piece)
                    human_count = cells.count(self.human_piece)
                    if ai_count and human_count:
                        continue
                    if ai_count:
                        score += (1, 8, 60, 700, 20_000)[ai_count - 1]
                    elif human_count:
                        score -= (1, 10, 80, 1_000, 25_000)[human_count - 1]
        self.evaluation_cache[key] = score
        return score