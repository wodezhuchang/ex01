# ui/user_page.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.user_manager import change_password
from core.borrow_manager import get_user_borrows
from core.book_manager import get_all_books

class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        self.back_btn = tk.Button(
            self,
            text="返回首页",
            font=("Helvetica", 12),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            command=lambda: self.controller.show_page("home")
        )
        self.back_btn.pack(side=tk.TOP, anchor=tk.NW, padx=20, pady=10)

        # ========== 用户信息区 ==========
        self.info_frame = tk.LabelFrame(self, text="个人信息", bg="white", padx=50, pady=30, font=("Helvetica", 14, "bold"))
        self.info_frame.pack(pady=10, padx=20, fill="x")
        
        self._show_user_info()
        
        # ========== 修改密码区 ==========
        self.pwd_frame = tk.LabelFrame(self, text="修改密码", bg="white", padx=50, pady=30, font=("Helvetica", 14, "bold"))
        self.pwd_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(self.pwd_frame, text="原密码：", font=("Helvetica", 12), bg="white").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_old_pwd = tk.Entry(self.pwd_frame, font=("Helvetica", 12), width=25, show="*")
        self.entry_old_pwd.grid(row=0, column=1, pady=10)
        
        tk.Label(self.pwd_frame, text="新密码：", font=("Helvetica", 12), bg="white").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.entry_new_pwd = tk.Entry(self.pwd_frame, font=("Helvetica", 12), width=25, show="*")
        self.entry_new_pwd.grid(row=1, column=1, pady=10)
        
        tk.Label(self.pwd_frame, text="确认密码：", font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.entry_confirm_pwd = tk.Entry(self.pwd_frame, font=("Helvetica", 12), width=25, show="*")
        self.entry_confirm_pwd.grid(row=2, column=1, pady=10)
        
        tk.Button(
            self.pwd_frame,
            text="确认修改",
            font=("Helvetica", 12),
            bg="#3498db",
            fg="white",
            command=self._change_pwd
        ).grid(row=3, column=0, columnspan=2, pady=20)
        
        # ========== 我的借阅统计 ==========
        self.stats_frame = tk.LabelFrame(self, text="借阅统计", bg="white", padx=50, pady=20, font=("Helvetica", 14, "bold"))
        self.stats_frame.pack(pady=10, padx=20, fill="x")
        
        self._show_borrow_stats()
        
        # ========== 我的借阅记录列表 ==========
        self.borrow_list_frame = tk.LabelFrame(self, text="我的借阅记录", bg="white", padx=20, pady=20, font=("Helvetica", 14, "bold"))
        self.borrow_list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # 借阅记录表格
        self.tree = ttk.Treeview(
            self.borrow_list_frame,
            columns=("borrow_id", "book_title", "author", "borrow_date", "return_date", "status"),
            show="headings",
            height=8
        )
        self.tree.heading("borrow_id", text="借阅ID")
        self.tree.heading("book_title", text="书名")
        self.tree.heading("author", text="作者")
        self.tree.heading("borrow_date", text="借阅日期")
        self.tree.heading("return_date", text="归还日期")
        self.tree.heading("status", text="状态")
        
        self.tree.column("borrow_id", width=80)
        self.tree.column("book_title", width=200)
        self.tree.column("author", width=120)
        self.tree.column("borrow_date", width=120)
        self.tree.column("return_date", width=120)
        self.tree.column("status", width=80)
        
        self.tree.pack(fill="both", expand=True)
        
        self._refresh_borrow_list()

    def refresh(self):
        """刷新页面数据"""
        self._refresh_borrow_list()
        self._update_stats()

    def _show_user_info(self):
        """显示用户基本信息"""
        user = self.controller.current_user
        if not user:
            tk.Label(self.info_frame, text="未登录", font=("Helvetica", 16), bg="white").pack()
            return
        
        row = 0
        tk.Label(self.info_frame, text="用户ID：", font=("Helvetica", 12), bg="white").grid(row=row, column=0, sticky=tk.W, pady=8)
        tk.Label(self.info_frame, text=user["user_id"], font=("Helvetica", 12), bg="white", fg="#27ae60").grid(row=row, column=1, sticky=tk.W, pady=8)
        row += 1
        
        tk.Label(self.info_frame, text="用户名：", font=("Helvetica", 12), bg="white").grid(row=row, column=0, sticky=tk.W, pady=8)
        tk.Label(self.info_frame, text=user["username"], font=("Helvetica", 12), bg="white", fg="#27ae60").grid(row=row, column=1, sticky=tk.W, pady=8)
        row += 1
        
        tk.Label(self.info_frame, text="角色：", font=("Helvetica", 12), bg="white").grid(row=row, column=0, sticky=tk.W, pady=8)
        role_text = "管理员" if user.get("role") == "admin" else "普通用户"
        role_color = "#e74c3c" if user.get("role") == "admin" else "#3498db"
        tk.Label(self.info_frame, text=role_text, font=("Helvetica", 12), bg="white", fg=role_color).grid(row=row, column=1, sticky=tk.W, pady=8)

    def _show_borrow_stats(self):
        """显示借阅统计"""
        user = self.controller.current_user
        if not user:
            tk.Label(self.stats_frame, text="未登录", font=("Helvetica", 12), bg="white").pack()
            return
        
        borrows = get_user_borrows(user["user_id"])
        total = len(borrows)
        borrowed = len([b for b in borrows if b["status"] == "borrowed"])
        returned = len([b for b in borrows if b["status"] == "returned"])
        
        # 使用Frame来布局统计数据
        stats_grid = tk.Frame(self.stats_frame, bg="white")
        stats_grid.pack()
        
        # 总借阅数
        total_frame = tk.LabelFrame(stats_grid, text="总借阅", bg="#ecf0f1", padx=20, pady=15)
        total_frame.grid(row=0, column=0, padx=20)
        tk.Label(total_frame, text=str(total), font=("Helvetica", 24, "bold"), bg="#ecf0f1", fg="#2c3e50").pack()
        
        # 未归还数
        borrowed_frame = tk.LabelFrame(stats_grid, text="未归还", bg="#ffeaa7", padx=20, pady=15)
        borrowed_frame.grid(row=0, column=1, padx=20)
        tk.Label(borrowed_frame, text=str(borrowed), font=("Helvetica", 24, "bold"), bg="#ffeaa7", fg="#d63031").pack()
        
        # 已归还数
        returned_frame = tk.LabelFrame(stats_grid, text="已归还", bg="#dfe6e9", padx=20, pady=15)
        returned_frame.grid(row=0, column=2, padx=20)
        tk.Label(returned_frame, text=str(returned), font=("Helvetica", 24, "bold"), bg="#dfe6e9", fg="#00b894").pack()

    def _update_stats(self):
        """更新统计信息"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        self._show_borrow_stats()

    def _refresh_borrow_list(self):
        """刷新借阅记录列表"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        user = self.controller.current_user
        if not user:
            return
        
        borrows = get_user_borrows(user["user_id"])
        book_map = {b["book_id"]: b for b in get_all_books()}
        
        for borrow in borrows:
            book_info = book_map.get(borrow.get("book_id", ""), {})
            status_text = borrow.get("status", "")
            status_color = "#e74c3c" if status_text == "borrowed" else "#27ae60"
            
            self.tree.insert("", tk.END, values=(
                borrow.get("borrow_id", ""),
                book_info.get("title", ""),
                book_info.get("author", ""),
                borrow.get("borrow_date", ""),
                borrow.get("return_date", "未归还"),
                status_text
            ))

    def _change_pwd(self):
        """修改密码"""
        user = self.controller.current_user
        if not user:
            messagebox.showwarning("提示", "请先登录！")
            return
        
        old_pwd = self.entry_old_pwd.get().strip()
        new_pwd = self.entry_new_pwd.get().strip()
        confirm_pwd = self.entry_confirm_pwd.get().strip()
        
        if not old_pwd or not new_pwd or not confirm_pwd:
            messagebox.showwarning("提示", "所有密码字段不能为空！")
            return
        
        if new_pwd != confirm_pwd:
            messagebox.showwarning("提示", "两次输入的新密码不一致！")
            return
        
        if len(new_pwd) < 6:
            messagebox.showwarning("提示", "新密码长度不能少于6位！")
            return
        
        if change_password(user["username"], old_pwd, new_pwd):
            messagebox.showinfo("成功", "密码修改成功！请重新登录")
            self.controller.current_user = None
            self.controller.show_page("login")
            self.entry_old_pwd.delete(0, tk.END)
            self.entry_new_pwd.delete(0, tk.END)
            self.entry_confirm_pwd.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "原密码错误！")