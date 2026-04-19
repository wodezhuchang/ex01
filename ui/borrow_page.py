# ui/borrow_page.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.borrow_manager import borrow_book, return_book, get_user_borrows, get_all_borrows
from core.book_manager import get_all_books

class BorrowPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # ========== 顶部功能区 ==========
        self.func_frame = tk.Frame(self, bg="#f0f0f0")
        self.func_frame.pack(fill="x", padx=20, pady=10)
        
        # 借阅按钮
        self.btn_borrow = tk.Button(
            self.func_frame,
            text="借阅图书",
            font=("Helvetica", 12),
            command=self._borrow_book_dialog
        )
        self.btn_borrow.pack(side=tk.LEFT, padx=5)
        
        # 归还按钮
        self.btn_return = tk.Button(
            self.func_frame,
            text="归还选中图书",
            font=("Helvetica", 12),
            command=self._return_book
        )
        self.btn_return.pack(side=tk.LEFT, padx=5)
        
        # 查看权限（管理员看全部，普通用户看个人）
        self.btn_view = tk.Button(
            self.func_frame,
            text="查看全部借阅" if self._is_admin() else "查看我的借阅",
            font=("Helvetica", 12),
            command=self._refresh_borrow_list
        )
        self.btn_view.pack(side=tk.LEFT, padx=5)
        
        # ========== 借阅列表区 ==========
        self.tree = ttk.Treeview(
            self,
            columns=("borrow_id", "user_id", "book_id", "title", "borrow_date", "return_date", "status"),
            show="headings",
            height=15
        )
        # 设置列标题
        self.tree.heading("borrow_id", text="借阅ID")
        self.tree.heading("user_id", text="用户ID")
        self.tree.heading("book_id", text="图书ID")
        self.tree.heading("title", text="书名")
        self.tree.heading("borrow_date", text="借阅日期")
        self.tree.heading("return_date", text="归还日期")
        self.tree.heading("status", text="状态")
        # 设置列宽
        self.tree.column("borrow_id", width=80)
        self.tree.column("user_id", width=80)
        self.tree.column("book_id", width=80)
        self.tree.column("title", width=200)
        self.tree.column("borrow_date", width=120)
        self.tree.column("return_date", width=120)
        self.tree.column("status", width=80)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 初始化列表
        self._refresh_borrow_list()

    def _is_admin(self):
        """判断是否为管理员"""
        user = self.controller.current_user
        return user and user.get("role") == "admin"

    def _refresh_borrow_list(self):
        """刷新借阅列表"""
        # 清空原有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        user = self.controller.current_user
        if not user:
            return
        
        # 管理员看全部，普通用户看个人
        if self._is_admin():
            borrows = get_all_borrows()
        else:
            borrows = get_user_borrows(user["user_id"])
        
        # 构建图书ID->书名映射
        book_map = {b["book_id"]: b["title"] for b in get_all_books()}
        
        # 插入数据
        for borrow in borrows:
            self.tree.insert("", tk.END, values=(
                borrow.get("borrow_id", ""),
                borrow.get("user_id", ""),
                borrow.get("book_id", ""),
                book_map.get(borrow.get("book_id", ""), ""),
                borrow.get("borrow_date", ""),
                borrow.get("return_date", ""),
                borrow.get("status", "")
            ))

    def _borrow_book_dialog(self):
        """借阅图书弹窗"""
        user = self.controller.current_user
        if not user:
            messagebox.showwarning("提示", "请先登录！")
            return
        
        dialog = tk.Toplevel(self)
        dialog.title("借阅图书")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        
        # 图书ID输入
        tk.Label(dialog, text="图书ID：", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, padx=20, pady=20)
        entry_book_id = tk.Entry(dialog, font=("Helvetica", 12), width=15)
        entry_book_id.grid(row=0, column=1, padx=20, pady=20)
        
        # 确认借阅
        def confirm_borrow():
            book_id = entry_book_id.get().strip()
            if not book_id:
                messagebox.showwarning("提示", "图书ID不能为空！")
                return
            # 执行借阅
            if borrow_book(user["user_id"], book_id):
                messagebox.showinfo("成功", "图书借阅成功！")
                dialog.destroy()
                self._refresh_borrow_list()
            else:
                messagebox.showerror("错误", "借阅失败（图书不存在/库存不足/已借阅）！")
        
        tk.Button(
            dialog,
            text="确认借阅",
            font=("Helvetica", 12),
            command=confirm_borrow
        ).grid(row=1, column=0, columnspan=2, pady=20)

    def _return_book(self):
        """归还选中图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选中要归还的借阅记录！")
            return
        # 获取选中行的borrow_id
        item = self.tree.item(selected[0])
        borrow_id = item["values"][0]
        # 确认归还
        if messagebox.askyesno("确认", f"是否归还借阅ID：{borrow_id}？"):
            if return_book(borrow_id):
                messagebox.showinfo("成功", "图书归还成功！")
                self._refresh_borrow_list()
            else:
                messagebox.showerror("错误", "归还失败（记录不存在/已归还）！")