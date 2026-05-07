from core.utils_csv import read_csv, append_csv, write_csv
from core.config import USERS_FILE
from core.logger import log_info, log_error, log_warning

def get_all_users():
    try:
        return read_csv(USERS_FILE)
    except Exception as e:
        log_error(f"获取所有用户异常：{str(e)}")
        return []

def user_exists(username):
    users = get_all_users()
    return any(u['username'] == username for u in users)

def user_register(username, password, role='user'):
    try:
        if user_exists(username):
            log_error(f"注册失败：用户名 {username} 已存在")
            return False
        if role not in ['admin', 'user']:
            role = 'user'
        
        users = get_all_users()
        max_id = max([int(u['user_id']) for u in users if u['user_id'].strip().isdigit()], default=0)
        new_id = max_id + 1
        
        new_user = {
            "user_id": str(new_id),
            "username": username,
            "password": password,
            "role": role
        }
        append_csv(USERS_FILE, new_user)
        
        if user_exists(username):
            log_info(f"注册成功：{username} ({role})")
            return True
        else:
            log_error(f"注册失败：用户 {username} 写入失败")
            return False
    except Exception as e:
        log_error(f"注册异常：{str(e)}")
        return False

def user_login(username, password):
    try:
        users = get_all_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                log_info(f"登录成功：{username}")
                return {
                    "user_id": user['user_id'],
                    "username": user['username'],
                    "role": user['role']
                }
        log_warning(f"登录失败：用户名或密码错误 ({username})")
        return None
    except Exception as e:
        log_error(f"登录异常：{str(e)}")
        return None

def change_password(username, old_password, new_password):
    try:
        users = get_all_users()
        for user in users:
            if user['username'] == username and user['password'] == old_password:
                user['password'] = new_password
                write_csv(USERS_FILE, users)
                log_info(f"密码修改成功：{username}")
                return True
        log_error(f"密码修改失败：用户名或旧密码错误 ({username})")
        return False
    except Exception as e:
        log_error(f"密码修改异常：{str(e)}")
        return False