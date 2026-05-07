import os
from core.utils_csv import read_csv, append_csv, write_csv

USERS_FILE = os.path.join('data', 'users.csv')


# ============================================
# 获取所有用户
# ============================================

def get_all_users():
    """返回所有用户列表，每条为dict。"""
    return read_csv(USERS_FILE)


# ============================================
# 判断用户是否存在
# ============================================

def user_exists(username):
    """
    判断用户名是否已存在。
    返回: True存在, False不存在
    """
    users = get_all_users()
    return any(u['username'] == username for u in users)


# ============================================
# 用户注册
# ============================================

def user_register(username, password, role='user'):
    """
    注册新用户。
    参数:
        username: 用户名
        password: 密码（建议后续加密存储，这里明文存储示例）
        role: 角色，'admin' 或 'user'，默认 'user'
    返回: True成功, False失败（用户名重复或角色非法）
    """
    # 1. 检查用户名是否重复
    if user_exists(username):
        return False

    # 2. 校验角色
    if role not in ['admin', 'user']:
        role = 'user'

    # 3. 生成 user_id（新增异常捕获）
    try:
        users = get_all_users()
        max_id = max([int(u['user_id']) for u in users if u['user_id'].strip().isdigit()], default=0)
        new_id = max_id + 1
    except Exception as e:
        print(f"生成user_id失败: {e}")
        return False

    # 4. 写入新用户
    new_user = {
        "user_id": str(new_id),
        "username": username,
        "password": password,
        "role": role
    }
    # 临时：手动校验append_csv写入前的字段
    print(f"准备写入新用户: {new_user}")  # 打印日志，验证字段
    append_csv(USERS_FILE, new_user)

    # 新增：校验是否写入成功
    if user_exists(username):
        return True
    else:
        return False


# ============================================
# 用户登录
# ============================================

def user_login(username, password):
    """
    用户登录校验。
    返回: 登录成功返回用户dict（包含user_id, username, role），
          登录失败返回 None
    """
    users = get_all_users()
    # 临时：打印所有用户数据，定位字段问题
    print(f"当前用户列表: {users}")

    for user in users:
        # 临时：打印比对过程
        print(f"比对用户: {user['username']}, 输入密码: {password}, 存储密码: {user['password']}")
        if user['username'] == username and user['password'] == password:
            # 返回用户信息（不返回密码）
            return {
                "user_id": user['user_id'],
                "username": user['username'],
                "role": user['role']
            }

    return None


# ============================================
# 修改密码（可选）
# ============================================

def change_password(username, old_password, new_password):
    """
    修改用户密码。
    返回: True成功, False失败（用户不存在或旧密码错误）
    """
    users = get_all_users()
    
    for user in users:
        if user['username'] == username and user['password'] == old_password:
            user['password'] = new_password
            write_csv(USERS_FILE, users)
            return True
    
    return False
