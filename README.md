# Qiqi 五子棋

一个使用 Python 和 Tkinter 开发的桌面五子棋游戏，支持双人对弈和人机对弈。程序不依赖第三方运行库。

## 功能

- 15 × 15 棋盘，暖木色棋盘搭配深色控制面板
- 双人对弈和人机对弈
- AI 使用限时 α-β 搜索，并优先处理直接获胜和防守堵截
- 显示当前对局状态、最后一步和获胜连线
- 点击棋盘交叉点落子；鼠标移动到待落位置时不会显示棋子
- `Ctrl+N` 开始新对局，`Esc` 退出程序

## 运行环境

- Python 3.8 或更高版本
- 支持 Tkinter 的 Python 安装

项目清理前发现的历史缓存文件名包含 `cpython-38`，说明此前曾使用 CPython 3.8。缓存文件不属于项目，也无法反映当前电脑正在使用的 Python 版本。

## 启动

在包含 `run.py` 的项目根目录打开终端：

```bash
python run.py
```

Windows 也可以使用（需要安装 Python Launcher）：

```powershell
py -3 run.py
```

启动后选择对局模式，点击“开始对局”。人机模式中黑棋先行，AI 执白棋。

## 项目结构

```text
GobangApp/
├── configure/
│   └── settings.py       # 棋盘、配色和游戏设置
├── core/
│   ├── AI.py             # 电脑对手
│   └── game.py           # 游戏规则与状态
├── gui/
│   ├── app.py            # 主窗口和对局流程
│   ├── gobang.ico        # 窗口图标
│   └── components/
│       ├── board.py      # 棋盘绘制和鼠标输入
│       └── control.py    # 模式、状态和操作面板
├── run.py                # 程序入口
├── README.md
├── .gitignore
└── pyproject.toml        # Ruff 代码风格配置
```

`configure`、`core`、`gui` 和 `gui/components` 目录不含 `__init__.py`。Python 3.8 支持命名空间包；请从项目根目录运行程序。

## AI 说明

AI 会优先寻找直接获胜的位置，其次尝试阻止对手立即获胜；其他情况下会在已有棋子附近进行限时搜索。搜索强度和响应时间会随棋局与电脑性能变化。AI 思考时会在启动程序的终端打印思考耗时和评估缓存命中次数。