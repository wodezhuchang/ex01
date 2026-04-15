import os
import sys

# 添加项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk, messagebox
import core.user_manager


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # ===============================
        # 登录框容器
        # ===============================
        self.login_frame = tk.Frame(self, bg="white", bd=2, relief="groove")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=280)
        
        # ===============================
        # 标题
        # ===============================
        tk.Label(
            self.login_frame,
            text="图书管理系统",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=15)
        
        # ===============================
        # 用户名
        # ===============================
        tk.Label(self.login_frame, text="用户名", font=("Helvetica", 11), bg="white").pack(pady=(10, 0))
        self.entry_username = tk.Entry(self.login_frame, font=("Helvetica", 11), width=25)
        self.entry_username.pack(pady=5)
        
        # ===============================
        # 密码
        # ===============================
        tk.Label(self.login_frame, text="密码", font=("Helvetica", 11), bg="white").pack(pady=(10, 0))
        self.entry_password = tk.Entry(self.login_frame, font=("Helvetica", 11), width=25, show="*")
        self.entry_password.pack(pady=5)
        
        # ===============================
        # 按钮区域
        # ===============================
        btn_frame = tk.Frame(self.login_frame, bg="white")
        btn_frame.pack(pady=15)
        
        # 登录按钮
        self.btn_login = tk.Button(
            btn_frame,
            text="登录",
            width=10,
            font=("Helvetica", 10),
            bg="#27ae60",
            fg="white",
            command=self._login
        )
        self.btn_login.grid(row=0, column=0, padx=5)
        
        # 注册按钮
        self.btn_register = tk.Button(
            btn_frame,
            text="注册",
            width=10,
            font=("Helvetica", 10),
            bg="#3498db",
            fg="white",
            command=self._show_register
        )
        self.btn_register.grid(row=0, column=1, padx=5)
        
        # ===============================
        # 绑定回车键
        # ===============================
        self.entry_password.bind("<Return>", lambda event: self._login())
        
        # 初始化默认管理员账号（可跳过，首次运行创建）
        self._init_default_admin()
    
    def _init_default_admin(self):
        """初始化默认管理员账号（仅首次运行）"""
        if not core.user_manager.user_exists("admin"):
            core.user_manager.user_register("admin", "admin123", "admin")
            print("已创建默认管理员账号: admin / admin123")
    
    # ===============================
    # 登录逻辑
    # ===============================
    def _login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return
        
        # 调用后端登录函数
        result = core.user_manager.user_login(username, password)
        
        if result:
            # 登录成功
            self.controller.current_user = result
            self.controller.show_page("home")
            # 清空输入框
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("登录失败", "用户名或密码错误")
    
    # ===============================
    # 注册逻辑（简易弹窗版）
    # ===============================
    def _show_register(self):
        """弹出注册对话框"""
        self.register_win = tk.Toplevel(self)
        self.register_win.title("用户注册")
        self.register_win.geometry("300x250")
        self.register_win.resizable(False, False)
        self.register_win.transient(self)  # 锁定主窗口
        
        # 注册表单
        tk.Label(self.register_win, text="用户名").pack(pady=(20, 5))
        entry_new_user = tk.Entry(self.register_win, width=20)
        entry_new_user.pack()
        
        tk.Label(self.register_win, text="密码").pack(pady=5)
        entry_new_pass = tk.Entry(self.register_win, width=20, show="*")
        entry_new_pass.pack()
        
        tk.Label(self.register_win, text="确认密码").pack(pady=5)
        entry_confirm = tk.Entry(self.register_win, width=20, show="*")
        entry_confirm.pack()
        
        tk.Label(self.register_win, text="角色").pack(pady=5)
        role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(self.register_win)
        role_frame.pack()
        tk.Radiobutton(role_frame, text="普通用户", variable=role_var, value="user").pack(side="left", padx=5)
        tk.Radiobutton(role_frame, text="管理员", variable=role_var, value="admin").pack(side="left", padx=5)
        
        # 注册按钮
        def do_register():
            username = entry_new_user.get().strip()
            password = entry_new_pass.get().strip()
            confirm = entry_confirm.get().strip()
            role = role_var.get()
            
            # 校验
            if not username or not password:
                messagebox.showwarning("提示", "用户名和密码不能为空")
                return
            if password != confirm:
                messagebox.showwarning("提示", "两次密码输入不一致")
                return
            if len(password) < 6:
                messagebox.showwarning("提示", "密码长度至少6位")
                return
            
            # 调用后端注册函数
            if core.user_manager.user_exists(username):
                messagebox.showerror("注册失败", "用户名已存在")
                return
            
            if core.user_manager.user_register(username, password, role):
                messagebox.showinfo("注册成功", f"用户 {username} 注册成功！")
                self.register_win.destroy()
            else:
                messagebox.showerror("注册失败", "注册失败，请重试")
        
        tk.Button(self.register_win, text="注册", command=do_register, bg="#27ae60", fg="white", width=10).pack(pady=15)
        
        # 居中显示
        self.register_win.grab_set()
