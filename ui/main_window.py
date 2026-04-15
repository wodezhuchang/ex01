import os
import sys

# 【关键】添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        
        # ===============================
        # 主窗口基本设置
        # ===============================
        self.root.title("图书管理系统")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # 字体样式
        self.font_title = ("Helvetica", 18, "bold")
        self.font_normal = ("Helvetica", 12)
        
        # 当前登录用户信息
        self.current_user = None
        
        # ===============================
        # 页面容器（切换用）
        # ===============================
        self.pages = {}
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # ===============================
        # 初始化各页面
        # ===============================
        self._init_pages()
        
        # 默认显示登录页
        self.show_page("login")
    
    def _init_pages(self):
        """初始化所有页面"""
        # 先导入各页面（后面会创建）
        from ui.login_page import LoginPage
        from ui.home_page import HomePage
        from ui.book_page import BookPage
        from ui.borrow_page import BorrowPage
        from ui.user_page import UserPage
        
        # 创建页面实例
        self.pages["login"] = LoginPage(self.container, self)
        self.pages["home"] = HomePage(self.container, self)
        self.pages["book"] = BookPage(self.container, self)
        self.pages["borrow"] = BorrowPage(self.container, self)
        self.pages["user"] = UserPage(self.container, self)
        
        # 初始隐藏所有页面
        for page in self.pages.values():
            page.pack_forget()
    
    def show_page(self, page_name):
        # 隐藏所有页面
        for page in self.pages.values():
            page.pack_forget()
        # 显示目标页面
        self.pages[page_name].pack(fill="both", expand=True)
        # 如果进入首页，更新欢迎信息
        if page_name == "home":
            self.pages["home"].update_welcome()

    
    def run(self):
        """启动主循环"""
        self.root.mainloop()
