import os
from datetime import datetime
from core.csv_utils import read_csv, write_csv, append_csv, get_all_data

BORROWS_FILE = os.path.join('data', 'borrows.csv')
BOOKS_FILE = os.path.join('data', 'books.csv')
USERS_FILE = os.path.join('data', 'users.csv')

# ============================================
# 借阅功能
# ============================================

def borrow_book(user_id, book_id):
    """
    用户借阅图书。
    校验：用户存在、图书存在、图书库存 > 0
    返回: True成功, False失败
    """
    # 1. 校验用户
    users = read_csv(USERS_FILE)
    if not any(u['user_id'] == str(user_id) for u in users):
        return False
    
    # 2. 校验图书
    books = read_csv(BOOKS_FILE)
    target_book = None
    for book in books:
        if book['book_id'] == str(book_id):
            target_book = book
            break
    if not target_book:
        return False
    
    # 3. 校验库存
    if int(target_book.get('count', 0)) <= 0:
        return False
    
    # 4. 校验用户是否已借该书（未归还）
    borrows = read_csv(BORROWS_FILE)
    if any(b['user_id'] == str(user_id) and b['book_id'] == str(book_id) and b['status'] == 'borrowed' for b in borrows):
        return False
    
    # 5. 创建借阅记录
    max_id = max([int(b['borrow_id']) for b in borrows], default=0)
    borrow_record = {
        "borrow_id": str(max_id + 1),
        "user_id": str(user_id),
        "book_id": str(book_id),
        "borrow_date": datetime.now().strftime("%Y-%m-%d"),
        "return_date": "",
        "status": "borrowed"
    }
    append_csv(BORROWS_FILE, borrow_record)
    
    # 6. 减少图书数量
    target_book['count'] = str(int(target_book['count']) - 1)
    write_csv(BOOKS_FILE, books)
    
    return True


# ============================================
# 归还功能
# ============================================

def return_book(borrow_id):
    """
    归还图书。
    校验借阅记录存在且状态为借出中。
    返回: True成功, False失败
    """
    borrows = read_csv(BORROWS_FILE)
    target_borrow = None
    
    for borrow in borrows:
        if borrow['borrow_id'] == str(borrow_id):
            target_borrow = borrow
            break
    
    if not target_borrow:
        return False
    if target_borrow['status'] != 'borrowed':
        return False
    
    # 更新借阅记录
    target_borrow['status'] = 'returned'
    target_borrow['return_date'] = datetime.now().strftime("%Y-%m-%d")
    write_csv(BORROWS_FILE, borrows)
    
    # 增加图书数量
    books = read_csv(BOOKS_FILE)
    for book in books:
        if book['book_id'] == target_borrow['book_id']:
            book['count'] = str(int(book['count']) + 1)
            break
    write_csv(BOOKS_FILE, books)
    
    return True


# ============================================
# 查询个人借阅
# ============================================

def get_user_borrows(user_id):
    """
    查询指定用户的所有借阅记录。
    返回: 借阅记录列表（包含图书信息）
    """
    borrows = read_csv(BORROWS_FILE)
    books = read_csv(BOOKS_FILE)
    
    # 构建 book_id -> book_info 映射
    book_map = {book['book_id']: book for book in books}
    
    user_borrows = []
    for borrow in borrows:
        if borrow['user_id'] == str(user_id):
            # 关联图书信息
            borrow_info = dict(borrow)
            book_info = book_map.get(borrow['book_id'], {})
            borrow_info['title'] = book_info.get('title', '')
            borrow_info['author'] = book_info.get('author', '')
            user_borrows.append(borrow_info)
    
    return user_borrows


# ============================================
# 逾期判断（可选）
# ============================================

def check_overdue(days_limit=30):
    """
    检查逾期未还的记录（默认30天算逾期）。
    返回: 逾期记录列表
    """
    borrows = read_csv(BORROWS_FILE)
    today = datetime.now()
    overdue_list = []
    
    for borrow in borrows:
        if borrow['status'] != 'borrowed':
            continue
        
        try:
            borrow_date = datetime.strptime(borrow['borrow_date'], "%Y-%m-%d")
            days = (today - borrow_date).days
            if days > days_limit:
                overdue_list.append(borrow)
        except:
            continue
    
    return overdue_list


# ============================================
# 辅助：获取所有借阅记录
# ============================================

def get_all_borrows():
    """获取全部借阅记录"""
    return read_csv(BORROWS_FILE)
