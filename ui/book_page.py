# ui/book_page.py - 管理员图书管理页面
import tkinter as tk
from tkinter import messagebox
from core.book_manager import add_book, delete_book
from ui.components import BookListComponent

class BookPage(tk.Frame):
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
            show_add_button=True,
            show_delete_button=True,
            on_add_callback=self._add_book_dialog,
            on_delete_callback=self._delete_book
        )
        self.book_list.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._check_permission()
    
    def _check_permission(self):
        user = self.controller.current_user
        if not user or user.get("role") != "admin":
            messagebox.showwarning("提示", "您没有权限访问此页面！")
            self.controller.show_page("home")
    
    def _add_book_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("新增图书")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self)
        
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
        entry_count.insert(0, "1")
        
        def confirm_add():
            book_info = {
                "title": entry_title.get().strip(),
                "author": entry_author.get().strip(),
                "isbn": entry_isbn.get().strip(),
                "count": entry_count.get().strip()
            }
            if not book_info["title"] or not book_info["isbn"]:
                messagebox.showwarning("提示", "书名/ISBN不能为空！")
                return
            if add_book(book_info):
                messagebox.showinfo("成功", "图书新增成功！")
                dialog.destroy()
                self.book_list.refresh()
            else:
                messagebox.showerror("错误", "ISBN已存在！")
        
        tk.Button(
            dialog,
            text="确认新增",
            font=("Helvetica", 12),
            command=confirm_add
        ).grid(row=4, column=0, columnspan=2, pady=20)
    
    def _delete_book(self, book_id):
        if messagebox.askyesno("确认", f"是否删除图书ID：{book_id}？"):
            if delete_book(book_id):
                messagebox.showinfo("成功", "图书删除成功！")
                self.book_list.refresh()
            else:
                messagebox.showerror("错误", "删除失败（图书不存在）！")