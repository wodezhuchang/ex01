# ui/borrow_page.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.borrow_manager import borrow_book, return_book, get_user_borrows, get_all_borrows
from core.book_manager import get_all_books, query_books

class BorrowPage(tk.Frame):
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

        # ========== 功能区 ==========
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

        # ========== 图书列表区（新增）==========
        self.book_frame = tk.LabelFrame(self, text="可借阅图书", bg="#f0f0f0", font=("Helvetica", 12, "bold"))
        self.book_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 图书搜索框
        search_frame = tk.Frame(self.book_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(search_frame, text="搜索图书：", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.entry_book_search = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
        self.entry_book_search.pack(side=tk.LEFT, padx=5)
        tk.Button(
            search_frame,
            text="搜索",
            font=("Helvetica", 12),
            command=self._search_books
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            search_frame,
            text="刷新图书列表",
            font=("Helvetica", 12),
            command=self._refresh_book_list
        ).pack(side=tk.LEFT, padx=5)
        
        # 图书列表树
        self.book_tree = ttk.Treeview(
            self.book_frame,
            columns=("book_id", "title", "author", "isbn", "count"),
            show="headings",
            height=8
        )
        # 设置列标题
        self.book_tree.heading("book_id", text="图书ID")
        self.book_tree.heading("title", text="书名")
        self.book_tree.heading("author", text="作者")
        self.book_tree.heading("isbn", text="ISBN")
        self.book_tree.heading("count", text="库存")
        # 设置列宽
        self.book_tree.column("book_id", width=80)
        self.book_tree.column("title", width=200)
        self.book_tree.column("author", width=150)
        self.book_tree.column("isbn", width=180)
        self.book_tree.column("count", width=80)
        
        self.book_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # ========== 借阅列表区 ==========
        self.borrow_frame = tk.LabelFrame(self, text="借阅记录", bg="#f0f0f0", font=("Helvetica", 12, "bold"))
        self.borrow_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.tree = ttk.Treeview(
            self.borrow_frame,
            columns=("borrow_id", "user_id", "book_id", "title", "author", "borrow_date", "return_date", "status"),
            show="headings",
            height=10
        )
        # 设置列标题
        self.tree.heading("borrow_id", text="借阅ID")
        self.tree.heading("user_id", text="用户ID")
        self.tree.heading("book_id", text="图书ID")
        self.tree.heading("title", text="书名")
        self.tree.heading("author", text="作者")
        self.tree.heading("borrow_date", text="借阅日期")
        self.tree.heading("return_date", text="归还日期")
        self.tree.heading("status", text="状态")
        # 设置列宽
        self.tree.column("borrow_id", width=80)
        self.tree.column("user_id", width=80)
        self.tree.column("book_id", width=80)
        self.tree.column("title", width=150)
        self.tree.column("author", width=120)
        self.tree.column("borrow_date", width=120)
        self.tree.column("return_date", width=120)
        self.tree.column("status", width=80)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 初始化列表
        self._refresh_book_list()
        self._refresh_borrow_list()

    def _is_admin(self):
        """判断是否为管理员"""
        user = self.controller.current_user
        return user and user.get("role") == "admin"

    def _refresh_borrow_list(self):
        """刷新借阅列表"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        user = self.controller.current_user
        if not user:
            return
        
        if self._is_admin():
            borrows = get_all_borrows()
        else:
            borrows = get_user_borrows(user["user_id"])
        
        book_map = {b["book_id"]: b for b in get_all_books()}
        
        for borrow in borrows:
            book_info = book_map.get(borrow.get("book_id", ""), {})
            self.tree.insert("", tk.END, values=(
                borrow.get("borrow_id", ""),
                borrow.get("user_id", ""),
                borrow.get("book_id", ""),
                book_info.get("title", ""),
                book_info.get("author", ""),
                borrow.get("borrow_date", ""),
                borrow.get("return_date", ""),
                borrow.get("status", "")
            ))

    def _refresh_book_list(self):
        """刷新可借阅图书列表"""
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        books = get_all_books()
        for book in books:
            count = int(book.get("count", "0"))
            if count > 0:
                self.book_tree.insert("", tk.END, values=(
                    book.get("book_id", ""),
                    book.get("title", ""),
                    book.get("author", ""),
                    book.get("isbn", ""),
                    count
                ))

    def _search_books(self):
        """搜索图书"""
        keyword = self.entry_book_search.get().strip()
        if not keyword:
            self._refresh_book_list()
            return
        
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        books = query_books(keyword)
        for book in books:
            count = int(book.get("count", "0"))
            if count > 0:
                self.book_tree.insert("", tk.END, values=(
                    book.get("book_id", ""),
                    book.get("title", ""),
                    book.get("author", ""),
                    book.get("isbn", ""),
                    count
                ))

    def _borrow_book_dialog(self):
        """借阅图书弹窗"""
        user = self.controller.current_user
        if not user:
            messagebox.showwarning("提示", "请先登录！")
            return
        
        selected_items = self.book_tree.selection()
        if selected_items:
            item = self.book_tree.item(selected_items[0])
            book_id = item["values"][0]
            title = item["values"][1]
            author = item["values"][2]
        else:
            book_id = ""
            title = ""
            author = ""
        
        dialog = tk.Toplevel(self)
        dialog.title("借阅图书")
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        dialog.transient(self)
        
        row = 0
        tk.Label(dialog, text="用户ID：", font=("Helvetica", 12)).grid(row=row, column=0, sticky=tk.W, padx=20, pady=10)
        tk.Label(dialog, text=user["user_id"], font=("Helvetica", 12)).grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        tk.Label(dialog, text="用户名：", font=("Helvetica", 12)).grid(row=row, column=0, sticky=tk.W, padx=20, pady=10)
        tk.Label(dialog, text=user["username"], font=("Helvetica", 12)).grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        tk.Label(dialog, text="图书ID：", font=("Helvetica", 12)).grid(row=row, column=0, sticky=tk.W, padx=20, pady=10)
        entry_book_id = tk.Entry(dialog, font=("Helvetica", 12), width=20)
        entry_book_id.grid(row=row, column=1, padx=20, pady=10)
        entry_book_id.insert(0, book_id)
        row += 1
        
        tk.Label(dialog, text="书名：", font=("Helvetica", 12)).grid(row=row, column=0, sticky=tk.W, padx=20, pady=10)
        label_title = tk.Label(dialog, text=title, font=("Helvetica", 12), fg="#27ae60")
        label_title.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        tk.Label(dialog, text="作者：", font=("Helvetica", 12)).grid(row=row, column=0, sticky=tk.W, padx=20, pady=10)
        label_author = tk.Label(dialog, text=author, font=("Helvetica", 12), fg="#27ae60")
        label_author.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        def confirm_borrow():
            book_id_input = entry_book_id.get().strip()
            if not book_id_input:
                messagebox.showwarning("提示", "图书ID不能为空！")
                return
            
            books = get_all_books()
            target_book = None
            for book in books:
                if book['book_id'] == book_id_input:
                    target_book = book
                    break
            
            if target_book:
                label_title.config(text=target_book.get('title', ''), fg="#27ae60")
                label_author.config(text=target_book.get('author', ''), fg="#27ae60")
            
            if borrow_book(user["user_id"], book_id_input):
                messagebox.showinfo("成功", "图书借阅成功！")
                dialog.destroy()
                self._refresh_borrow_list()
                self._refresh_book_list()
            else:
                label_title.config(text="图书不存在或库存不足", fg="#e74c3c")
                label_author.config(text="", fg="#e74c3c")
                messagebox.showerror("错误", "借阅失败（图书不存在/库存不足/已借阅）！")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        tk.Button(
            btn_frame,
            text="确认借阅",
            font=("Helvetica", 12),
            bg="#3498db",
            fg="white",
            command=confirm_borrow
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame,
            text="从列表选择",
            font=("Helvetica", 12),
            bg="#95a5a6",
            fg="white",
            command=lambda: self._select_from_book_list(entry_book_id, label_title, label_author)
        ).pack(side=tk.LEFT, padx=10)

    def _select_from_book_list(self, entry_book_id, label_title, label_author):
        """从图书列表中选择"""
        selected_items = self.book_tree.selection()
        if selected_items:
            item = self.book_tree.item(selected_items[0])
            entry_book_id.delete(0, tk.END)
            entry_book_id.insert(0, item["values"][0])
            label_title.config(text=item["values"][1], fg="#27ae60")
            label_author.config(text=item["values"][2], fg="#27ae60")
        else:
            messagebox.showwarning("提示", "请先在图书列表中选择一本书！")

    def _return_book(self):
        """归还选中图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选中要归还的借阅记录！")
            return
        
        item = self.tree.item(selected[0])
        borrow_id = item["values"][0]
        book_title = item["values"][3]
        
        if messagebox.askyesno("确认", f"是否归还图书《{book_title}》？\n借阅ID：{borrow_id}"):
            if return_book(borrow_id):
                messagebox.showinfo("成功", "图书归还成功！")
                self._refresh_borrow_list()
                self._refresh_book_list()
            else:
                messagebox.showerror("错误", "归还失败（记录不存在/已归还）！")