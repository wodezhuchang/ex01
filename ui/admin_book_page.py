# ui/admin_book_page.py
import csv
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from core.book_manager import get_all_books, add_book, delete_book, update_book, query_books

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

        # 批量导入按钮（仅管理员可见）【新增】
        self.btn_batch_import = tk.Button(
            self.func_frame,
            text="批量导入图书",
            font=("Helvetica", 12),
            command=self._batch_import_books
        )
        self.btn_batch_import.pack(side=tk.LEFT, padx=5)
        
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

    def _check_permission(self):
        """检查用户权限（管理员显示增删按钮）"""
        user = self.controller.current_user
        if not user or user.get("role") != "admin":
            self.btn_add.config(state=tk.DISABLED)
            self.btn_del.config(state=tk.DISABLED)
            self.btn_batch_import.config(state=tk.DISABLED)  # 新增
        else:
            self.btn_add.config(state=tk.NORMAL)
            self.btn_del.config(state=tk.NORMAL)
            self.btn_batch_import.config(state=tk.NORMAL)

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
                messagebox.showerror("错误", "删除失败（图书不存在或存在未归还的借阅记录）！")

    def _batch_import_books(self):
        """批量导入图书（CSV文件）- 支持库存累加"""
        # 1. 选择CSV文件
        file_path = filedialog.askopenfilename(
            title="选择批量导入的CSV文件",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        if not file_path:  # 用户取消选择
            return

        # 预加载数据库中已有的图书信息（构建ISBN映射）
        existing_books = get_all_books()
        isbn_map = {}  # key: isbn, value: {title, author, count, book_id}
        for book in existing_books:
            isbn = book.get("isbn")
            if isbn:
                isbn_map[isbn] = {
                    "title": book.get("title", "").strip(),
                    "author": book.get("author", "").strip(),
                    "count": int(book.get("count", 0)),
                    "book_id": book.get("book_id")
                }

        # 2. 校验文件格式和内容
        try:
            # 读取CSV文件并验证格式
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                # 校验列名（必须包含：title, author, isbn, count）
                required_columns = {"title", "author", "isbn", "count"}
                if not required_columns.issubset(reader.fieldnames):
                    messagebox.showerror("格式错误",
                                         f"CSV文件列名缺失！必须包含：{', '.join(required_columns)}\n当前列名：{reader.fieldnames}")
                    return

                # 3. 验证每一行数据
                valid_books = []
                error_lines = []
                for line_num, row in enumerate(reader, start=2):  # 行号从2开始（跳过表头）
                    # 清空首尾空格
                    row = {k: v.strip() for k, v in row.items()}

                    # 校验必填项
                    if not row.get("title") or not row.get("isbn"):
                        error_lines.append(f"第{line_num}行：书名/ISBN不能为空")
                        continue

                    # 校验库存为数字
                    try:
                        count = int(row.get("count", 1))
                        if count < 0:
                            error_lines.append(f"第{line_num}行：库存不能为负数")
                            continue
                    except ValueError:
                        error_lines.append(f"第{line_num}行：库存必须是数字")
                        continue

                    # 数据合法，加入列表
                    valid_books.append({
                        "title": row["title"],
                        "author": row.get("author", ""),
                        "isbn": row["isbn"],
                        "count": count,
                        "line_num": line_num  # 记录行号，用于后续报错
                    })

            # 4. 处理校验结果
            if error_lines:
                # 显示错误信息
                error_msg = "以下行数据校验失败，未导入：\n" + "\n".join(error_lines[:10])  # 只显示前10条
                if len(error_lines) > 10:
                    error_msg += f"\n... 共{len(error_lines)}行错误"
                messagebox.showwarning("数据校验失败", error_msg)
                if not valid_books:  # 无合法数据，终止导入
                    return

            # 5. 批量处理数据（新增/更新）
            success_count = 0  # 新增成功数
            update_count = 0  # 更新库存数
            fail_count = 0  # 失败数
            fail_reasons = []  # 失败原因

            for book in valid_books:
                isbn = book["isbn"]
                title = book["title"].strip()
                author = book["author"].strip()
                add_count = book["count"]
                line_num = book["line_num"]

                # 检查ISBN是否已存在
                if isbn in isbn_map:
                    # 获取已存在的图书信息
                    exist_book = isbn_map[isbn]
                    exist_title = exist_book["title"]
                    exist_author = exist_book["author"]

                    # 对比title和author
                    if title == exist_title and author == exist_author:
                        # 信息完全匹配，累加库存并更新
                        new_count = exist_book["count"] + add_count
                        update_book(exist_book["book_id"], {"count": new_count})
                        update_count += 1
                    else:
                        # ISBN相同但信息不匹配，标记失败
                        fail_count += 1
                        fail_reasons.append(
                            f"第{line_num}行：ISBN[{isbn}]已存在（现有：《{exist_title}》/{exist_author}，导入：《{title}》/{author}）"
                        )
                else:
                    # ISBN不存在，执行新增
                    if add_book({
                        "title": title,
                        "author": author,
                        "isbn": isbn,
                        "count": add_count
                    }):
                        success_count += 1
                    else:
                        # 新增失败（理论上不会触发，因为ISBN已校验不存在）
                        fail_count += 1
                        fail_reasons.append(f"第{line_num}行：ISBN[{isbn}]新增失败")

            # 6. 显示导入结果
            result_msg = f"批量导入完成！\n新增成功：{success_count} 条\n库存更新：{update_count} 条\n失败：{fail_count} 条"

            if fail_reasons:
                result_msg += "\n\n失败原因（前10条）：\n" + "\n".join(fail_reasons[:10])
                if len(fail_reasons) > 10:
                    result_msg += f"\n... 共{len(fail_reasons)}条失败记录"

            messagebox.showinfo("导入结果", result_msg)

            # 7. 刷新图书列表
            self._refresh_book_list()

        except Exception as e:
            # 捕获所有异常（文件编码、读取错误等）
            messagebox.showerror("导入失败", f"文件处理异常：{str(e)}")
