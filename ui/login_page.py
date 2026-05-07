# ui/login_page.py
import tkinter as tk
from tkinter import messagebox
from core.user_manager import user_login, user_register


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        # 登录容器
        self.login_frame = tk.Frame(self, bg="white", padx=50, pady=30)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 标题
        tk.Label(
            self.login_frame,
            text="图书管理系统登录",
            font=("Helvetica", 18, "bold"),
            bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # 用户名
        tk.Label(self.login_frame, text="用户名：", font=("Helvetica", 12), bg="white").grid(row=1, column=0,
                                                                                            sticky=tk.W, pady=10)
        self.entry_username = tk.Entry(self.login_frame, font=("Helvetica", 12), width=20)
        self.entry_username.grid(row=1, column=1, pady=10)
        # 默认聚焦用户名输入框
        self.entry_username.focus_set()

        # 密码
        tk.Label(self.login_frame, text="密码：", font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky=tk.W,
                                                                                          pady=10)
        self.entry_pwd = tk.Entry(self.login_frame, font=("Helvetica", 12), width=20, show="*")
        self.entry_pwd.grid(row=2, column=1, pady=10)

        # 绑定回车键 = 登录（非常重要的体验优化）
        self.entry_pwd.bind('<Return>', lambda event: self._login())

        # 按钮
        tk.Button(
            self.login_frame,
            text="登录",
            font=("Helvetica", 12),
            width=10,
            command=self._login
        ).grid(row=3, column=0, pady=20)

        tk.Button(
            self.login_frame,
            text="注册",
            font=("Helvetica", 12),
            width=10,
            command=self._register
        ).grid(row=3, column=1, pady=20)

    def _login(self):
        """登录逻辑"""
        username = self.entry_username.get().strip()
        password = self.entry_pwd.get().strip()

        # 修正：更严谨的空值判断
        if username == "" or password == "":
            messagebox.showwarning("提示", "用户名和密码不能为空！")
            return

        # 增加异常捕获：防止 user_manager 报错导致程序崩溃
        try:
            user = user_login(username, password)
        except Exception as e:
            messagebox.showerror("系统错误", f"登录失败：{str(e)}")
            return

        if user:
            self.controller.current_user = user
            self.controller.show_page("Home")  # 修正：页面名大小写统一
            # 登录成功清空输入框
            self.entry_username.delete(0, tk.END)
            self.entry_pwd.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "用户名或密码错误！")

    def _register(self):
        """注册逻辑"""
        username = self.entry_username.get().strip()
        password = self.entry_pwd.get().strip()

        if username == "" or password == "":
            messagebox.showwarning("提示", "用户名和密码不能为空！")
            return

        # 注册也增加异常捕获
        try:
            result = user_register(username, password)
        except Exception as e:
            messagebox.showerror("系统错误", f"注册失败：{str(e)}")
            return

        if result:
            messagebox.showinfo("成功", "注册成功！请登录")
            # 注册成功后清空密码框
            self.entry_pwd.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "用户名已存在！")