# ui/admin_book_page.py
import csv
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from core.book_manager import get_all_books, add_book, delete_book, update_book, query_books

class BookPage1(tk.Frame):
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

        # ========== 顶部功能区 ==========
        self.func_frame = tk.Frame(self, bg="#f0f0f0")
        self.func_frame.pack(fill="x", padx=20, pady=10)
        
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
        #self._check_permission()
        
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