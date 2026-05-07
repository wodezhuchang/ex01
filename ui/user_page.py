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
            font=("Helvetica", 10),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            command=lambda: self.controller.show_page("home")
        )
        self.back_btn.pack(side=tk.TOP, anchor=tk.NW, padx=15, pady=8)

        # ========== 用户信息区 ==========
        self.info_frame = tk.LabelFrame(self, text="个人信息", bg="white", padx=20, pady=10, font=("Helvetica", 12, "bold"))
        self.info_frame.pack(pady=5, padx=15, fill="x")
        
        self.user_id_var = tk.StringVar(value="")
        self.username_var = tk.StringVar(value="")
        self.role_var = tk.StringVar(value="")
        
        info_grid = tk.Frame(self.info_frame, bg="white")
        info_grid.pack()
        
        tk.Label(info_grid, text="用户ID：", font=("Helvetica", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.label_user_id = tk.Label(info_grid, textvariable=self.user_id_var, font=("Helvetica", 10), bg="white", fg="#27ae60")
        self.label_user_id.grid(row=0, column=1, sticky=tk.W, pady=3)
        
        tk.Label(info_grid, text="用户名：", font=("Helvetica", 10), bg="white").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.label_username = tk.Label(info_grid, textvariable=self.username_var, font=("Helvetica", 10), bg="white", fg="#27ae60")
        self.label_username.grid(row=1, column=1, sticky=tk.W, pady=3)
        
        tk.Label(info_grid, text="角色：", font=("Helvetica", 10), bg="white").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.label_role = tk.Label(info_grid, textvariable=self.role_var, font=("Helvetica", 10), bg="white")
        self.label_role.grid(row=2, column=1, sticky=tk.W, pady=3)
        
        # ========== 修改密码区（三项放同一行）==========
        self.pwd_frame = tk.LabelFrame(self, text="修改密码", bg="white", padx=15, pady=10, font=("Helvetica", 12, "bold"))
        self.pwd_frame.pack(pady=5, padx=15, fill="x")
        
        pwd_grid = tk.Frame(self.pwd_frame, bg="white")
        pwd_grid.pack()
        
        # 三个输入框放在同一行
        tk.Label(pwd_grid, text="原密码：", font=("Helvetica", 10), bg="white").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.entry_old_pwd = tk.Entry(pwd_grid, font=("Helvetica", 10), width=15, show="*")
        self.entry_old_pwd.grid(row=0, column=1, padx=5)
        
        tk.Label(pwd_grid, text="新密码：", font=("Helvetica", 10), bg="white").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.entry_new_pwd = tk.Entry(pwd_grid, font=("Helvetica", 10), width=15, show="*")
        self.entry_new_pwd.grid(row=0, column=3, padx=5)
        
        tk.Label(pwd_grid, text="确认密码：", font=("Helvetica", 10), bg="white").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.entry_confirm_pwd = tk.Entry(pwd_grid, font=("Helvetica", 10), width=15, show="*")
        self.entry_confirm_pwd.grid(row=0, column=5, padx=5)
        
        # 按钮放在第二行
        tk.Button(
            pwd_grid,
            text="确认修改",
            font=("Helvetica", 10),
            bg="#3498db",
            fg="white",
            width=10,
            command=self._change_pwd
        ).grid(row=1, column=0, columnspan=6, pady=8)
        
        # ========== 我的借阅统计 ==========
        self.stats_frame = tk.LabelFrame(self, text="借阅统计", bg="white", padx=15, pady=8, font=("Helvetica", 12, "bold"))
        self.stats_frame.pack(pady=5, padx=15, fill="x")
        
        self.stats_total_var = tk.StringVar(value="0")
        self.stats_borrowed_var = tk.StringVar(value="0")
        self.stats_returned_var = tk.StringVar(value="0")
        
        stats_grid = tk.Frame(self.stats_frame, bg="white")
        stats_grid.pack()
        
        total_frame = tk.LabelFrame(stats_grid, text="总借阅", bg="#ecf0f1", padx=25, pady=6)
        total_frame.grid(row=0, column=0, padx=8)
        tk.Label(total_frame, textvariable=self.stats_total_var, font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack()
        
        borrowed_frame = tk.LabelFrame(stats_grid, text="未归还", bg="#ffeaa7", padx=25, pady=6)
        borrowed_frame.grid(row=0, column=1, padx=8)
        tk.Label(borrowed_frame, textvariable=self.stats_borrowed_var, font=("Helvetica", 16, "bold"), bg="#ffeaa7", fg="#d63031").pack()
        
        returned_frame = tk.LabelFrame(stats_grid, text="已归还", bg="#dfe6e9", padx=25, pady=6)
        returned_frame.grid(row=0, column=2, padx=8)
        tk.Label(returned_frame, textvariable=self.stats_returned_var, font=("Helvetica", 16, "bold"), bg="#dfe6e9", fg="#00b894").pack()
        
        # ========== 我的借阅记录列表 ==========
        self.borrow_list_frame = tk.LabelFrame(self, text="我的借阅记录", bg="white", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        self.borrow_list_frame.pack(pady=5, padx=15, fill="both", expand=True)
        
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
        
        self.tree.column("borrow_id", width=60)
        self.tree.column("book_title", width=150)
        self.tree.column("author", width=90)
        self.tree.column("borrow_date", width=90)
        self.tree.column("return_date", width=90)
        self.tree.column("status", width=60)
        
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        self._update_user_info()
        self._update_stats()
        self._refresh_borrow_list()

    def _update_user_info(self):
        user = self.controller.current_user
        if user:
            self.user_id_var.set(user.get("user_id", ""))
            self.username_var.set(user.get("username", ""))
            role_text = "管理员" if user.get("role") == "admin" else "普通用户"
            self.role_var.set(role_text)
            self.label_role.config(fg="#e74c3c" if user.get("role") == "admin" else "#3498db")
        else:
            self.user_id_var.set("")
            self.username_var.set("")
            self.role_var.set("")

    def _update_stats(self):
        user = self.controller.current_user
        if user:
            borrows = get_user_borrows(user["user_id"])
            total = len(borrows)
            borrowed = len([b for b in borrows if b["status"] == "borrowed"])
            returned = len([b for b in borrows if b["status"] == "returned"])
            self.stats_total_var.set(str(total))
            self.stats_borrowed_var.set(str(borrowed))
            self.stats_returned_var.set(str(returned))
        else:
            self.stats_total_var.set("0")
            self.stats_borrowed_var.set("0")
            self.stats_returned_var.set("0")

    def _refresh_borrow_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        user = self.controller.current_user
        if not user:
            return
        
        borrows = get_user_borrows(user["user_id"])
        book_map = {b["book_id"]: b for b in get_all_books()}
        
        for borrow in borrows:
            book_info = book_map.get(borrow.get("book_id", ""), {})
            self.tree.insert("", tk.END, values=(
                borrow.get("borrow_id", ""),
                book_info.get("title", ""),
                book_info.get("author", ""),
                borrow.get("borrow_date", ""),
                borrow.get("return_date", "未归还"),
                borrow.get("status", "")
            ))

    def _change_pwd(self):
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