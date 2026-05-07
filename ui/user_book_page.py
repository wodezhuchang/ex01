# ui/user_book_page.py - 普通用户图书查看页面
import tkinter as tk
from ui.components import BookListComponent

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
        
        self.book_list = BookListComponent(
            self,
            show_search=True,
            show_add_button=False,
            show_delete_button=False
        )
        self.book_list.pack(fill="both", expand=True, padx=20, pady=10)