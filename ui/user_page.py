# ui/user_page.py
import tkinter as tk
from tkinter import messagebox
from core.user_manager import change_password
from core.borrow_manager import get_user_borrows

class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # ========== 用户信息区 ==========
        self.info_frame = tk.Frame(self, bg="white", padx=50, pady=30)
        self.info_frame.pack(pady=30)
        
        # 显示用户基本信息
        self._show_user_info()
        
        # ========== 修改密码区 ==========
        self.pwd_frame = tk.Frame(self, bg="white", padx=50, pady=30)
        self.pwd_frame.pack(pady=10)
        
        tk.Label(self.pwd_frame, text="修改密码", font=("Helvetica", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(self.pwd_frame, text="原密码：", font=("Helvetica", 12), bg="white").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.entry_old_pwd = tk.Entry(self.pwd_frame, font=("Helvetica", 12), width=20, show="*")
        self.entry_old_pwd.grid(row=1, column=1, pady=10)
        
        tk.Label(self.pwd_frame, text="新密码：", font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.entry_new_pwd = tk.Entry(self.pwd_frame, font=("Helvetica", 12), width=20, show="*")
        self.entry_new_pwd.grid(row=2, column=1, pady=10)
        
        tk.Button(
            self.pwd_frame,
            text="确认修改",
            font=("Helvetica", 12),
            command=self._change_pwd
        ).grid(row=3, column=0, columnspan=2, pady=20)
        
        # ========== 我的借阅统计 ==========
        self.borrow_frame = tk.Frame(self, bg="white", padx=50, pady=20)
        self.borrow_frame.pack(pady=10)
        
        self._show_borrow_stats()

    def _show_user_info(self):
        """显示用户基本信息"""
        user = self.controller.current_user
        if not user:
            tk.Label(self.info_frame, text="未登录", font=("Helvetica", 16), bg="white").pack()
            return
        
        tk.Label(self.info_frame, text="个人信息", font=("Helvetica", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.info_frame, text="用户ID：", font=("Helvetica", 12), bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Label(self.info_frame, text=user["user_id"], font=("Helvetica", 12), bg="white").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        tk.Label(self.info_frame, text="用户名：", font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        tk.Label(self.info_frame, text=user["username"], font=("Helvetica", 12), bg="white").grid(row=2, column=1, sticky=tk.W, pady=5)
        
        tk.Label(self.info_frame, text="角色：", font=("Helvetica", 12), bg="white").grid(row=3, column=0, sticky=tk.W, pady=5)
        role_text = "管理员" if user.get("role") == "admin" else "普通用户"
        tk.Label(self.info_frame, text=role_text, font=("Helvetica", 12), bg="white").grid(row=3, column=1, sticky=tk.W, pady=5)

    def _show_borrow_stats(self):
        """显示借阅统计"""
        user = self.controller.current_user
        if not user:
            tk.Label(self.borrow_frame, text="未登录", font=("Helvetica", 12), bg="white").pack()
            return
        
        borrows = get_user_borrows(user["user_id"])
        total = len(borrows)
        borrowed = len([b for b in borrows if b["status"] == "borrowed"])
        returned = len([b for b in borrows if b["status"] == "returned"])
        
        tk.Label(self.borrow_frame, text="我的借阅统计", font=("Helvetica", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.borrow_frame, text="总借阅数：", font=("Helvetica", 12), bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Label(self.borrow_frame, text=total, font=("Helvetica", 12), bg="white").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        tk.Label(self.borrow_frame, text="未归还数：", font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        tk.Label(self.borrow_frame, text=borrowed, font=("Helvetica", 12), bg="white").grid(row=2, column=1, sticky=tk.W, pady=5)
        
        tk.Label(self.borrow_frame, text="已归还数：", font=("Helvetica", 12), bg="white").grid(row=3, column=0, sticky=tk.W, pady=5)
        tk.Label(self.borrow_frame, text=returned, font=("Helvetica", 12), bg="white").grid(row=3, column=1, sticky=tk.W, pady=5)

    def _change_pwd(self):
        """修改密码"""
        user = self.controller.current_user
        if not user:
            messagebox.showwarning("提示", "请先登录！")
            return
        
        old_pwd = self.entry_old_pwd.get().strip()
        new_pwd = self.entry_new_pwd.get().strip()
        
        if not old_pwd or not new_pwd:
            messagebox.showwarning("提示", "原密码/新密码不能为空！")
            return
        
        if change_password(user["username"], old_pwd, new_pwd):
            messagebox.showinfo("成功", "密码修改成功！请重新登录")
            # 退出登录
            self.controller.current_user = None
            self.controller.show_page("login")
            # 清空输入框
            self.entry_old_pwd.delete(0, tk.END)
            self.entry_new_pwd.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "原密码错误！")