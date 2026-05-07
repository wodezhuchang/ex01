# Tkinter 语法指南

本指南基于图书管理系统项目，介绍 Tkinter 中常用的弹窗、提示框、布局等语法。

## 目录

1. [消息弹窗](#1-消息弹窗)
2. [自定义输入弹窗](#2-自定义输入弹窗)
3. [常用组件](#3-常用组件)
4. [布局管理器](#4-布局管理器)
5. [数据绑定与动态更新](#5-数据绑定与动态更新)

---

## 1. 消息弹窗

Tkinter 提供 `messagebox` 模块用于显示各种消息提示框。

### 1.1 成功提示 - showinfo

显示蓝色信息图标和确定按钮。

```python
from tkinter import messagebox

messagebox.showinfo("成功", "密码修改成功！请重新登录")
```

**项目示例**（ui/user_page.py 第 205 行）：
```python
if change_password(user["username"], old_pwd, new_pwd):
    messagebox.showinfo("成功", "密码修改成功！请重新登录")
```

### 1.2 错误提示 - showerror

显示红色错误图标和确定按钮。

```python
messagebox.showerror("错误", "原密码错误！")
```

**项目示例**（ui/user_page.py 第 212 行）：
```python
else:
    messagebox.showerror("错误", "原密码错误！")
```

### 1.3 警告提示 - showwarning

显示黄色警告图标和确定按钮。

```python
messagebox.showwarning("提示", "请先登录！")
```

**项目示例**（ui/user_page.py 第 185 行）：
```python
if not user:
    messagebox.showwarning("提示", "请先登录！")
    return
```

### 1.4 确认对话框 - askyesno

显示是/否按钮，返回布尔值 `True`/`False`。

```python
if messagebox.askyesno("确认", "是否归还图书？"):
    # 执行确认操作
    pass
```

**项目示例**（ui/borrow_page.py 第 313 行）：
```python
if messagebox.askyesno("确认", f"是否归还图书《{book_title}》？\n借阅ID：{borrow_id}"):
    if return_book(borrow_id):
        messagebox.showinfo("成功", "图书归还成功！")
```

### 1.5 其他确认对话框

```python
# askokcancel - 确定/取消
result = messagebox.askokcancel("标题", "内容")

# askretrycancel - 重试/取消
result = messagebox.askretrycancel("标题", "内容")

# askquestion - 是/否，返回 'yes'/'no'
result = messagebox.askquestion("标题", "内容")
```

---

## 2. 自定义输入弹窗

使用 `Toplevel` 创建自定义的输入对话框。

### 2.1 创建 Toplevel 窗口

```python
import tkinter as tk

dialog = tk.Toplevel(parent)  # parent 是父窗口
dialog.title("窗口标题")
dialog.geometry("450x300")  # 宽度x高度
dialog.resizable(False, False)  # 禁止调整大小
dialog.transient(parent)  # 保持在父窗口前面
```

**项目示例**（ui/borrow_page.py 第 211-215 行）：
```python
dialog = tk.Toplevel(self)
dialog.title("借阅图书")
dialog.geometry("450x300")
dialog.resizable(False, False)
dialog.transient(self)
```

### 2.2 在弹窗中添加组件

```python
# 添加标签和输入框
tk.Label(dialog, text="图书ID：", font=("Helvetica", 12)).grid(row=0, column=0)
entry = tk.Entry(dialog, font=("Helvetica", 12), width=20)
entry.grid(row=0, column=1)
entry.insert(0, "默认值")  # 插入默认值

# 添加按钮
def confirm_action():
    value = entry.get().strip()
    # 处理逻辑...
    dialog.destroy()  # 关闭弹窗

tk.Button(dialog, text="确认", command=confirm_action).pack()
```

**项目完整示例**（ui/borrow_page.py 第 211-288 行）：
```python
dialog = tk.Toplevel(self)
dialog.title("借阅图书")
dialog.geometry("450x300")

# 添加表单元素
row = 0
tk.Label(dialog, text="用户ID：", font=("Helvetica", 12)).grid(row=row, column=0, sticky=tk.W, padx=20, pady=10)
tk.Label(dialog, text=user["user_id"], font=("Helvetica", 12)).grid(row=row, column=1, padx=20, pady=10)
row += 1

# 添加按钮
def confirm_borrow():
    book_id_input = entry_book_id.get().strip()
    if borrow_book(user["user_id"], book_id_input):
        messagebox.showinfo("成功", "图书借阅成功！")
        dialog.destroy()

tk.Button(btn_frame, text="确认借阅", command=confirm_borrow).pack()
```

---

## 3. 常用组件

### 3.1 按钮 - Button

```python
button = tk.Button(
    parent,
    text="按钮文字",
    font=("Helvetica", 12),  # 字体和大小
    bg="#3498db",           # 背景色
    fg="white",             # 前景色（文字颜色）
    activebackground="#2980b9",  # 点击时的背景色
    width=10,               # 宽度
    command=callback_function  # 点击事件
)
button.pack()
```

**项目示例**（ui/user_page.py 第 68-76 行）：
```python
tk.Button(
    pwd_grid,
    text="确认修改",
    font=("Helvetica", 10),
    bg="#3498db",
    fg="white",
    width=10,
    command=self._change_pwd
).grid(row=1, column=0, columnspan=6, pady=8)
```

### 3.2 标签 - Label

```python
label = tk.Label(
    parent,
    text="标签文字",
    font=("Helvetica", 12, "bold"),  # 字体、大小、加粗
    bg="white",                      # 背景色
    fg="#27ae60",                    # 前景色
    textvariable=string_var          # 绑定 StringVar 动态更新
)
label.pack()
```

**项目示例**（ui/user_page.py 第 35-36 行）：
```python
tk.Label(info_grid, text="用户ID：", font=("Helvetica", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=3)
self.label_user_id = tk.Label(info_grid, textvariable=self.user_id_var, font=("Helvetica", 10), bg="white", fg="#27ae60")
```

### 3.3 输入框 - Entry

```python
entry = tk.Entry(
    parent,
    font=("Helvetica", 12),
    width=15,           # 宽度
    show="*"            # 输入掩码（用于密码）
)
entry.pack()

# 获取输入内容
text = entry.get().strip()

# 清空输入框
entry.delete(0, tk.END)

# 插入内容
entry.insert(0, "默认值")
```

**项目示例**（ui/user_page.py 第 55-65 行）：
```python
self.entry_old_pwd = tk.Entry(pwd_grid, font=("Helvetica", 10), width=15, show="*")
self.entry_old_pwd.grid(row=0, column=1, padx=5)
```

### 3.4 框架 - Frame / LabelFrame

```python
# 普通框架
frame = tk.Frame(
    parent,
    bg="#f0f0f0"  # 背景色
)
frame.pack(fill="x", padx=20, pady=10)

# 带标题的框架
label_frame = tk.LabelFrame(
    parent,
    text="框架标题",
    bg="white",
    padx=20,  # 内部水平边距
    pady=10,  # 内部垂直边距
    font=("Helvetica", 12, "bold")
)
label_frame.pack(fill="x")
```

**项目示例**（ui/user_page.py 第 25、48 行）：
```python
self.info_frame = tk.LabelFrame(self, text="个人信息", bg="white", padx=20, pady=10, font=("Helvetica", 12, "bold"))
self.info_frame.pack(pady=5, padx=15, fill="x")
```

### 3.5 树形表格 - Treeview (ttk)

```python
from tkinter import ttk

tree = ttk.Treeview(
    parent,
    columns=("col1", "col2", "col3"),  # 列名
    show="headings",  # 只显示列标题，不显示树结构
    height=8          # 显示行数
)

# 设置列标题
tree.heading("col1", text="列1标题")
tree.heading("col2", text="列2标题")

# 设置列宽
tree.column("col1", width=80)
tree.column("col2", width=150)

tree.pack(fill="both", expand=True)

# 插入数据
tree.insert("", tk.END, values=("值1", "值2", "值3"))

# 删除所有数据
for item in tree.get_children():
    tree.delete(item)

# 获取选中项
selected_items = tree.selection()
if selected_items:
    item = tree.item(selected_items[0])
    values = item["values"]
```

**项目示例**（ui/user_page.py 第 105-125 行）：
```python
self.tree = ttk.Treeview(
    self.borrow_list_frame,
    columns=("borrow_id", "book_title", "author", "borrow_date", "return_date", "status"),
    show="headings",
    height=8
)
self.tree.heading("borrow_id", text="借阅ID")
self.tree.heading("book_title", text="书名")
self.tree.column("borrow_id", width=60)
self.tree.column("book_title", width=150)
self.tree.pack(fill="both", expand=True)
```

---

## 4. 布局管理器

### 4.1 Pack 布局

最简单的布局，按添加顺序排列。

```python
widget.pack(
    side=tk.TOP,    # 位置：TOP/BOTTOM/LEFT/RIGHT
    anchor=tk.NW,   # 锚点：N/NE/E/SE/S/SW/W/NW/CENTER
    padx=20,        # 水平外边距
    pady=10,        # 垂直外边距
    fill="x",       # 填充：x/y/both
    expand=True     # 是否扩展
)
```

**项目示例**：
```python
self.back_btn.pack(side=tk.TOP, anchor=tk.NW, padx=15, pady=8)
self.info_frame.pack(pady=5, padx=15, fill="x")
self.tree.pack(fill="both", expand=True)
```

### 4.2 Grid 布局

网格布局，按行列排列。

```python
widget.grid(
    row=0,              # 行号
    column=0,           # 列号
    rowspan=2,          # 跨行数
    columnspan=3,       # 跨列数
    sticky=tk.W,        # 对齐方式：N/S/E/W/NE/SE/SW/NW
    padx=5,             # 水平外边距
    pady=5              # 垂直外边距
)
```

**项目示例**（ui/user_page.py 第 55-76 行）：
```python
tk.Label(pwd_grid, text="原密码：", font=("Helvetica", 10), bg="white").grid(row=0, column=0, sticky=tk.W, padx=5)
self.entry_old_pwd = tk.Entry(pwd_grid, font=("Helvetica", 10), width=15, show="*")
self.entry_old_pwd.grid(row=0, column=1, padx=5)

tk.Button(pwd_grid, text="确认修改", ...).grid(row=1, column=0, columnspan=6, pady=8)
```

### 4.3 Place 布局

绝对定位布局（较少使用）。

```python
widget.place(
    x=100,      # x坐标
    y=50,       # y坐标
    width=200,  # 宽度
    height=30   # 高度
)
```

---

## 5. 数据绑定与动态更新

### 5.1 StringVar - 字符串变量

用于绑定文本，自动更新显示。

```python
import tkinter as tk

var = tk.StringVar(value="初始值")

# 创建时绑定
label = tk.Label(parent, textvariable=var)

# 设置值
var.set("新值")

# 获取值
value = var.get()
```

**项目示例**（ui/user_page.py 第 28-30 行）：
```python
self.user_id_var = tk.StringVar(value="")
self.username_var = tk.StringVar(value="")
self.role_var = tk.StringVar(value="")

# 绑定到 Label
self.label_user_id = tk.Label(info_grid, textvariable=self.user_id_var, ...)

# 更新值
self.user_id_var.set(user.get("user_id", ""))
```

### 5.2 动态修改组件属性

使用 `config()` 方法修改组件属性。

```python
# 修改文字颜色
label.config(fg="#e74c3c")

# 修改文字内容（如果没有绑定 StringVar）
label.config(text="新文字")

# 修改背景色
frame.config(bg="#ecf0f1")
```

**项目示例**（ui/user_page.py 第 139 行）：
```python
self.label_role.config(fg="#e74c3c" if user.get("role") == "admin" else "#3498db")
```

**项目示例**（ui/borrow_page.py 第 256 行）：
```python
label_title.config(text=target_book.get('title', ''), fg="#27ae60")
label_author.config(text=target_book.get('author', ''), fg="#27ae60")
```

---

## 附录：常用颜色

| 颜色 | 值 | 用途 |
|------|-----|------|
| 成功绿 | `#27ae60` | 成功状态 |
| 错误红 | `#e74c3c` | 错误状态 |
| 警告黄 | `#ffeaa7` | 警告提示 |
| 主蓝 | `#3498db` | 主要按钮 |
| 次灰 | `#95a5a6` | 次要按钮 |
| 背景灰 | `#f0f0f0` | 页面背景 |
| 白色 | `white` | 内容背景 |

---

## 总结

- **消息提示**：使用 `messagebox` 模块的 `showinfo`/`showerror`/`showwarning`/`askyesno`
- **自定义弹窗**：使用 `Toplevel` 创建，内部可自由添加组件
- **组件绑定**：使用 `StringVar` 实现数据动态更新
- **布局管理**：`pack` 适合简单排列，`grid` 适合表格布局
- **动态修改**：使用 `config()` 修改组件属性
