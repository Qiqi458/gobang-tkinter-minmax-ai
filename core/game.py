from typing import Optional, List, Tuple
from dataclasses import dataclass
from configure.settings import config

@dataclass
class MoveResult:
    """落子结果"""
    valid: bool  # 落子是否有效
    game_over: bool  # 游戏是否结束
    game_state: int  # 游戏状态


class GobangGame:
    """五子棋游戏类"""

    def __init__(self):
        """初始化游戏"""
        self.reset_game()

    def reset_game(self):
        """重置游戏"""
        self.board = [[None for _ in range(config.BOARD_SIZE)] for _ in range(config.BOARD_SIZE)]
        self.current_state = config.State.READY
        self.winning_line = []  # 获胜棋子连线

    def make_move(self, row: int, col: int) -> MoveResult:
        """在指定位置落子"""
        # 检查游戏状态是否允许落子
        if self.current_state not in (config.State.BLACK_TURN, config.State.WHITE_TURN):
            return MoveResult(False, False, self.current_state)
        # 检查落子的位置是否有效
        if not (0 <= row < config.BOARD_SIZE and 0 <= col < config.BOARD_SIZE):
            return MoveResult(False, False, self.current_state)
        if self.board[row][col] is not None:
            return MoveResult(False, False, self.current_state)
        # 放置棋子
        self.board[row][col] = self.current_state
        # 检查是否获胜
        if self._check_win(row, col):
            self.current_state = config.State.BLACK_WIN if self.current_state == config.State.BLACK_TURN else config.State.WHITE_WIN
            return MoveResult(True, True, self.current_state)
        # 检查是否平局
        if self._check_draw():
            self.current_state = config.State.DRAW
            return MoveResult(True, True, self.current_state)
        # 切换轮次
        self._switch_state()
        return MoveResult(True, False, self.current_state)
    
    def _switch_state(self):
        """切换轮次"""
        self.current_state = config.State.WHITE_TURN if self.current_state == config.State.BLACK_TURN else config.State.BLACK_TURN
    
    def _check_win(self, row: int, col: int) -> bool:
        """检查是否获胜"""
        directions = [
            [(0, 1), (0, -1)],   # 水平方向
            [(1, 0), (-1, 0)],   # 垂直方向
            [(1, 1), (-1, -1)],  # 主对角线
            [(1, -1), (-1, 1)],  # 副对角线
        ]
        player = self.current_state
        for direction in directions:
            count = 1  # 当前落子的位置已有一个棋子
            # 检查两个相反的方向
            for dx, dy in direction:
                r, c = row+dx, col+dy
                while 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE and self.board[r][c] == player:
                    count += 1
                    r += dx
                    c += dy
            # 如果任意方向有 5 个或更多的连续棋子
            if count >= 5:
                self._record_winning_line(row, col, direction)
                return True
        return False

    def _check_draw(self) -> bool:
        """检查是否平局"""
        return all(cell is not None for row in self.board for cell in row)
    
    def _record_winning_line(self, row: int, col: int, direction: List[Tuple[int, int]]):
        """记录获胜线"""
        player = self.current_state
        winning_line = [(row, col)]
        for dx, dy in direction:
            r, c = row + dx, col + dy
            while 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE and self.board[r][c] == player:
                winning_line.append((r, c))
                r += dx
                c += dy
        self.winning_line = winning_line
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """获取所有合法的落子位置"""
        return [(row, col) for row in range(config.BOARD_SIZE) for col in range(config.BOARD_SIZE) if self.board[row][col] is None]

    def get_current_state(self) -> int:
        """获取当前状态"""
        return self.current_state
    
    def set_current_state(self, state: int):
        """设置当前状态"""
        self.current_state = state
    
    def get_board(self)-> List[List[Optional[int]]]:
        """获取当前棋盘"""
        return self.board
    
    def get_winning_line(self) -> List[Tuple[int, int]]:
        """获取胜利的棋子位置"""
        return self.winning_line