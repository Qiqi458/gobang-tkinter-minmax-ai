import tkinter as tk
from gui.app import GobangApp


def main():
    """主程序入口"""
    root = tk.Tk()
    app = GobangApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()