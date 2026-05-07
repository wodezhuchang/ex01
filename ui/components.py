import tkinter as tk
from tkinter import ttk
from core.book_manager import get_all_books, query_books

class BookListComponent(tk.Frame):
    def __init__(self, parent, show_search=True, show_add_button=False, show_delete_button=False, on_add_callback=None, on_delete_callback=None):
        super().__init__(parent, bg="#f0f0f0")
        self.show_add_button = show_add_button
        self.show_delete_button = show_delete_button
        self.on_add_callback = on_add_callback
        self.on_delete_callback = on_delete_callback
        
        if show_search:
            search_frame = tk.Frame(self, bg="#f0f0f0")
            search_frame.pack(fill="x", padx=10, pady=5)
            tk.Label(search_frame, text="搜索：", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
            self.entry_search = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
            self.entry_search.pack(side=tk.LEFT, padx=5)
            tk.Button(
                search_frame,
                text="搜索",
                font=("Helvetica", 12),
                command=self._search_books
            ).pack(side=tk.LEFT, padx=5)
            tk.Button(
                search_frame,
                text="刷新",
                font=("Helvetica", 12),
                command=self._refresh_list
            ).pack(side=tk.LEFT, padx=5)
        
        if show_add_button and on_add_callback:
            btn_add = tk.Button(
                self,
                text="新增图书",
                font=("Helvetica", 12),
                bg="#27ae60",
                fg="white",
                command=on_add_callback
            )
            btn_add.pack(side=tk.LEFT, padx=5, pady=5)
        
        if show_delete_button and on_delete_callback:
            btn_del = tk.Button(
                self,
                text="删除选中",
                font=("Helvetica", 12),
                bg="#e74c3c",
                fg="white",
                command=self._handle_delete
            )
            btn_del.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.tree = ttk.Treeview(
            self,
            columns=("book_id", "title", "author", "isbn", "count"),
            show="headings",
            height=15
        )
        
        self.tree.heading("book_id", text="图书ID")
        self.tree.heading("title", text="书名")
        self.tree.heading("author", text="作者")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("count", text="库存")
        
        self.tree.column("book_id", width=80)
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("isbn", width=180)
        self.tree.column("count", width=80)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self._refresh_list()
    
    def _refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        books = get_all_books()
        for book in books:
            self.tree.insert("", tk.END, values=(
                book.get("book_id", ""),
                book.get("title", ""),
                book.get("author", ""),
                book.get("isbn", ""),
                book.get("count", "0")
            ))
    
    def _search_books(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            self._refresh_list()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        books = query_books(keyword)
        for book in books:
            self.tree.insert("", tk.END, values=(
                book.get("book_id", ""),
                book.get("title", ""),
                book.get("author", ""),
                book.get("isbn", ""),
                book.get("count", "0")
            ))
    
    def _handle_delete(self):
        selected = self.tree.selection()
        if selected and self.on_delete_callback:
            item = self.tree.item(selected[0])
            book_id = item["values"][0]
            self.on_delete_callback(book_id)
            self._refresh_list()
    
    def get_selected_book(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            return {
                "book_id": item["values"][0],
                "title": item["values"][1],
                "author": item["values"][2],
                "isbn": item["values"][3],
                "count": item["values"][4]
            }
        return None
    
    def refresh(self):
        self._refresh_list()