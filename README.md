# 所有路径建议用 os.path.join("data", "xxx.csv")

项目根目录
- main.py        # 程序入口
- core/          # 核心后端逻辑文件夹，所有后端函数都放这里
  - "__init__".py  # 空文件，告诉Python这是个可导入的包
  - init_csv.py  # CSV初始化函数
  - utils_csv.py # CSV读写工具
  - book_manager.py # 图书管理逻辑
  - user_manager.py # 用户管理逻辑
  - import_export.py # 图书批量导入逻辑
- ui/            # Tkinter前端界面代码
- data/          # 存放CSV数据文件


# 【后端模块】Core Issues（纯 Python 函数）

CORE-001：创建 CSV 文件与表头初始化
- 创建 data 目录
- 创建 books.csv、users.csv、borrows.csv
- 写入固定表头
- 确保文件不存在时自动创建

CORE-002：封装 CSV 通用读写工具函数
- read_csv(file_path) → 返回列表数据
- write_csv(file_path, data) → 覆盖写入
- append_csv(file_path, row) → 追加一行
- 异常处理（文件不存在、格式错误）

CORE-003：用户账户逻辑函数
- user_login(username, password) → 登录校验
- user_register(username, password, role) → 注册
- user_exists(username) → 判断用户是否重复
- get_all_users() → 获取所有用户

CORE-004：图书信息逻辑函数
- add_book(图书信息) → 添加图书
- delete_book(book_id) → 删除图书
- update_book(book_id, 新信息) → 修改图书
- query_books(关键词) → 搜索图书
- get_all_books() → 获取全部图书

CORE-005：借阅归还逻辑函数
- borrow_book(user_id, book_id) → 借阅（校验状态）
- return_book(borrow_id) → 归还
- get_user_borrows(user_id) → 查询个人借阅
- check_overdue() → 逾期判断（可选）

CORE-006：数据导入导出函数（CSV 导入图书）
- import_books_from_csv(file_path) → 批量导入图书
- 校验重复 ISBN、格式正确性

---

# 【前端模块】UI Issues（Tkinter 界面）

UI-001：搭建主窗口框架
- 创建主窗口
- 设置标题、大小、样式
- 页面切换框架（登录、首页、图书管理、用户中心）

UI-002：登录页面
- 用户名、密码输入框
- 登录按钮 → 调用 CORE-003
- 注册按钮（简易版）
- 错误提示弹窗

UI-003：系统首页 / 菜单页面
- 功能按钮：图书管理、借阅管理、个人中心、退出
- 根据用户身份显示菜单（管理员 / 普通用户）

UI-004：图书管理页面
- 图书列表展示（Treeview）
- 查询输入框 + 查询按钮
- 添加、修改、删除图书按钮
- 调用 CORE-004 所有函数

UI-005：图书批量导入页面
- 选择文件按钮
- 导入按钮 → 调用 CORE-006
- 导入成功 / 失败提示

UI-006：借阅管理页面
- 借阅图书功能
- 归还图书功能
- 当前借阅列表展示
- 调用 CORE-005

UI-007：个人中心页面
- 显示个人信息
- 显示我的借阅记录
- 密码修改（简易）

UI-008：弹窗与工具
- 提示框 success/error/info
- 确认删除弹窗
- 输入表单弹窗（添加 / 修改图书）

---

# 【整合联调】Integration Issues

INTEG-001：前后端函数对接
- UI 按钮点击 → 调用 core 函数
- 数据展示 → core 读取 CSV → 显示到界面

INTEG-002：数据一致性测试
- 测试添加图书 → CSV 是否写入
- 测试登录 → 账号是否正确读取
- 测试借阅 → 状态是否同步更新

INTEG-003：程序入口 main.py 整合
- 导入所有模块
- 启动界面
- 初始化 CSV 文件

INTEG-004：打包成可运行软件（可选）
- 使用 pyinstaller 打包 exe
- 提供双击运行版本

---

# 三、汇总步骤（超清晰）

1. 后端开发完成
- 完成所有 core 函数
- 所有 CSV 读写测试通过
- 提供可直接调用的函数列表

2. 前端开发完成
- 完成所有 Tkinter 页面、按钮、表单
- 页面内部 “预留函数调用位置”
- 不依赖后端也能先做界面

3. 合并联调（最关键）
在 main.py 中做一件事：
把前端的按钮事件 → 绑定后端的函数

示例：
```python

# 前端登录按钮点击
def login_click():
    username = entry_username.get()
    password = entry_password.get()
    # 调用后端函数
    result = core.user_login(username, password)
    if result:
        show_menu()
    else:
        show_error()
```
      
4. 数据文件统一存放
- 所有 CSV 放在 /data 目录
- 前后端都读写这个目录，数据天然互通

5. 最终交付
- 只需要交付：
main.py
/core
/ui
/data
- 双击运行 main.py 即可使用

# 四、开发顺序（最顺畅）
- CORE-001、002（CSV 基础）
- CORE-003（用户）
- UI-001、002（登录界面）
- 联调登录
- CORE-004（图书）
- UI-004、005（图书界面）
- CORE-005（借阅）
- UI-006（借阅界面）
- 全部联调
- 打包交付
