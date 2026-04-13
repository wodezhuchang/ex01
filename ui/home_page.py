import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # ===============================
        # 顶部欢迎区域
        # ===============================
        self.header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        
        self.lbl_welcome = tk.Label(
            self.header_frame, 
            text="欢迎使用图书管理系统", 
            font=("Helvetica", 20, "bold"),
            fg="white", 
            bg="#2c3e50"
        )
        self.lbl_welcome.pack(pady=20)
        
        # ===============================
        # 中间功能按钮区域
        # ===============================
        self.content_frame = tk.Frame(self, bg="#f0f0f0")
        self.content_frame.pack(expand=True)
        
        # 按钮样式配置
        self.btn_style = {
            "width": 20,
            "height": 2,
            "font": ("Helvetica", 12),
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "cursor": "hand2"
        }
        
        # 功能按钮容器
        self.buttons_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.buttons_frame.pack(pady=30)
        
        # ===============================
        # 底部状态栏
        # ===============================
        self.status_frame = tk.Frame(self, bg="#ecf0f1", height=30)
        self.status_frame.pack(fill="x", side="bottom")
        self.status_frame.pack_propagate(False)
        
        self.lbl_status = tk.Label(
            self.status_frame, 
            text="", 
            font=("Helvetica", 10),
            bg="#ecf0f1", 
            fg="#7f8c8d"
        )
        self.lbl_status.pack(pady=5)
    
    def update_welcome(self):
        """更新欢迎信息和功能按钮（根据用户角色）"""
        user = self.controller.current_user
        if user:
            role_text = "管理员" if user.get("role") == "admin" else "普通用户"
            self.lbl_welcome.config(text=f"欢迎，{user['username']}（{role_text}）")
            self.lbl_status.config(text=f"当前用户：{user['username']} | 角色：{role_text}")
        else:
            self.lbl_welcome.config(text="欢迎使用图书管理系统")
            self.lbl_status.config(text="")
        
        # 清空旧按钮
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        # 根据角色添加功能按钮
        # 管理员：全部功能
        if user and user.get("role") == "admin":
            self._create_button("图书管理", lambda: self.controller.show_page("book"))
            self._create_button("借阅管理", lambda: self.controller.show_page("borrow"))
            self._create_button("个人中心", lambda: self.controller.show_page("user"))
            self._create_button("退出登录", self._logout)
        else:
            # 普通用户：借阅管理、个人中心、退出
            self._create_button("借阅管理", lambda: self.controller.show_page("borrow"))
            self._create_button("个人中心", lambda: self.controller.show_page("user"))
            self._create_button("退出登录", self._logout)
    
    def _create_button(self, text, command):
        """创建统一样式的按钮"""
        btn = tk.Button(
            self.buttons_frame,
            text=text,
            command=command,
            **self.btn_style
        )
        btn.pack(pady=10)
    
    def _logout(self):
        """退出登录"""
        self.controller.current_user = None
        self.controller.show_page("login")
