# ui/book_page.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.book_manager import get_all_books, add_book, delete_book, update_book, query_books

class BookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # ========== 顶部功能区 ==========
        self.func_frame = tk.Frame(self, bg="#f0f0f0")
        self.func_frame.pack(fill="x", padx=20, pady=10)
        
        # 新增按钮（仅管理员可见）
        self.btn_add = tk.Button(
            self.func_frame,
            text="新增图书",
            font=("Helvetica", 12),
            command=self._add_book_dialog
        )
        self.btn_add.pack(side=tk.LEFT, padx=5)
        
        # 删除按钮（仅管理员可见）
        self.btn_del = tk.Button(
            self.func_frame,
            text="删除选中图书",
            font=("Helvetica", 12),
            command=self._delete_book
        )
        self.btn_del.pack(side=tk.LEFT, padx=5)
        
        # 搜索框
        tk.Label(self.func_frame, text="搜索：", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.entry_search = tk.Entry(self.func_frame, font=("Helvetica", 12), width=20)
        self.entry_search.pack(side=tk.LEFT, padx=5)
        tk.Button(
            self.func_frame,
            text="搜索",
            font=("Helvetica", 12),
            command=self._search_book
        ).pack(side=tk.LEFT, padx=5)
        
        # 刷新按钮
        tk.Button(
            self.func_frame,
            text="刷新列表",
            font=("Helvetica", 12),
            command=self._refresh_book_list
        ).pack(side=tk.LEFT, padx=5)
        
        # ========== 图书列表区 ==========
        self.tree = ttk.Treeview(
            self,
            columns=("book_id", "title", "author", "isbn", "count"),
            show="headings",
            height=15
        )
        # 设置列标题
        self.tree.heading("book_id", text="图书ID")
        self.tree.heading("title", text="书名")
        self.tree.heading("author", text="作者")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("count", text="库存")
        # 设置列宽
        self.tree.column("book_id", width=80)
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("isbn", width=180)
        self.tree.column("count", width=80)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 初始化列表
        self._refresh_book_list()
        # 根据用户角色控制按钮权限
        self._check_permission()

    def _check_permission(self):
        """检查用户权限（管理员显示增删按钮）"""
        user = self.controller.current_user
        if not user or user.get("role") != "admin":
            self.btn_add.config(state=tk.DISABLED)
            self.btn_del.config(state=tk.DISABLED)
        else:
            self.btn_add.config(state=tk.NORMAL)
            self.btn_del.config(state=tk.NORMAL)

    def _refresh_book_list(self):
        """刷新图书列表"""
        # 清空原有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 获取所有图书并插入
        books = get_all_books()
        for book in books:
            self.tree.insert("", tk.END, values=(
                book.get("book_id", ""),
                book.get("title", ""),
                book.get("author", ""),
                book.get("isbn", ""),
                book.get("count", "0")
            ))

    def _search_book(self):
        """搜索图书"""
        keyword = self.entry_search.get().strip()
        if not keyword:
            self._refresh_book_list()
            return
        # 清空原有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 插入搜索结果
        books = query_books(keyword)
        for book in books:
            self.tree.insert("", tk.END, values=(
                book.get("book_id", ""),
                book.get("title", ""),
                book.get("author", ""),
                book.get("isbn", ""),
                book.get("count", "0")
            ))

    def _add_book_dialog(self):
        """新增图书弹窗"""
        dialog = tk.Toplevel(self)
        dialog.title("新增图书")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self)  # 置顶
        
        # 表单布局
        tk.Label(dialog, text="书名：", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, padx=20, pady=10)
        entry_title = tk.Entry(dialog, font=("Helvetica", 12), width=25)
        entry_title.grid(row=0, column=1, padx=20, pady=10)
        
        tk.Label(dialog, text="作者：", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, padx=20, pady=10)
        entry_author = tk.Entry(dialog, font=("Helvetica", 12), width=25)
        entry_author.grid(row=1, column=1, padx=20, pady=10)
        
        tk.Label(dialog, text="ISBN：", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, padx=20, pady=10)
        entry_isbn = tk.Entry(dialog, font=("Helvetica", 12), width=25)
        entry_isbn.grid(row=2, column=1, padx=20, pady=10)
        
        tk.Label(dialog, text="库存：", font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W, padx=20, pady=10)
        entry_count = tk.Entry(dialog, font=("Helvetica", 12), width=25)
        entry_count.grid(row=3, column=1, padx=20, pady=10)
        entry_count.insert(0, "1")  # 默认库存1
        
        # 确认按钮
        def confirm_add():
            book_info = {
                "title": entry_title.get().strip(),
                "author": entry_author.get().strip(),
                "isbn": entry_isbn.get().strip(),
                "count": entry_count.get().strip()
            }
            # 校验必填项
            if not book_info["title"] or not book_info["isbn"]:
                messagebox.showwarning("提示", "书名/ISBN不能为空！")
                return
            # 新增图书
            if add_book(book_info):
                messagebox.showinfo("成功", "图书新增成功！")
                dialog.destroy()
                self._refresh_book_list()
            else:
                messagebox.showerror("错误", "ISBN已存在！")
        
        tk.Button(
            dialog,
            text="确认新增",
            font=("Helvetica", 12),
            command=confirm_add
        ).grid(row=4, column=0, columnspan=2, pady=20)

    def _delete_book(self):
        """删除选中图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选中要删除的图书！")
            return
        # 获取选中行的book_id
        item = self.tree.item(selected[0])
        book_id = item["values"][0]
        # 确认删除
        if messagebox.askyesno("确认", f"是否删除图书ID：{book_id}？"):
            if delete_book(book_id):
                messagebox.showinfo("成功", "图书删除成功！")
                self._refresh_book_list()
            else:
                messagebox.showerror("错误", "删除失败（图书不存在）！")