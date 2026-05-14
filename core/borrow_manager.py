from datetime import datetime
from core.utils_csv import read_csv, write_csv, append_csv
from core.config import BORROWS_FILE, BOOKS_FILE, USERS_FILE
from core.logger import log_info, log_error, log_warning

def borrow_book(user_id, book_id):
    try:
        users = read_csv(USERS_FILE)
        if not any(u['user_id'] == str(user_id) for u in users):
            log_error(f"借阅失败：用户ID {user_id} 不存在")
            return False
        
        books = read_csv(BOOKS_FILE)
        target_book = None
        for book in books:
            if book['book_id'] == str(book_id):
                target_book = book
                break
        if not target_book:
            log_error(f"借阅失败：图书ID {book_id} 不存在")
            return False
        
        if int(target_book.get('count', 0)) <= 0:
            log_error(f"借阅失败：图书ID {book_id} 库存不足")
            return False
        
        borrows = read_csv(BORROWS_FILE)
        if any(b['user_id'] == str(user_id) and b['book_id'] == str(book_id) and b['status'] == 'borrowed' for b in borrows):
            log_error(f"借阅失败：用户 {user_id} 已借阅图书 {book_id}")
            return False
        
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
        
        target_book['count'] = str(int(target_book['count']) - 1)
        write_csv(BOOKS_FILE, books)
        
        log_info(f"借阅成功：用户 {user_id} 借阅图书 {book_id} ({target_book.get('title', '')})")
        return True
    except Exception as e:
        log_error(f"借阅异常：{str(e)}")
        return False

def return_book(borrow_id):
    try:
        borrows = read_csv(BORROWS_FILE)
        target_borrow = None
        
        for borrow in borrows:
            if borrow['borrow_id'] == str(borrow_id):
                target_borrow = borrow
                break
        
        if not target_borrow:
            log_error(f"归还失败：借阅记录ID {borrow_id} 不存在")
            return False
        if target_borrow['status'] != 'borrowed':
            log_error(f"归还失败：借阅记录ID {borrow_id} 状态不是借出")
            return False
        
        target_borrow['status'] = 'returned'
        target_borrow['return_date'] = datetime.now().strftime("%Y-%m-%d")
        write_csv(BORROWS_FILE, borrows)
        
        books = read_csv(BOOKS_FILE)
        book_title = ""
        for book in books:
            if book['book_id'] == target_borrow['book_id']:
                book['count'] = str(int(book['count']) + 1)
                book_title = book.get('title', '')
                break
        write_csv(BOOKS_FILE, books)
        
        log_info(f"归还成功：借阅记录 {borrow_id} 已归还 ({book_title})")
        return True
    except Exception as e:
        log_error(f"归还异常：{str(e)}")
        return False

def get_user_borrows(user_id):
    try:
        borrows = read_csv(BORROWS_FILE)
        books = read_csv(BOOKS_FILE)
        
        book_map = {book['book_id']: book for book in books}
        
        user_borrows = []
        for borrow in borrows:
            if borrow['user_id'] == str(user_id):
                borrow_info = dict(borrow)
                book_info = book_map.get(borrow['book_id'], {})
                borrow_info['title'] = book_info.get('title', '')
                borrow_info['author'] = book_info.get('author', '')
                user_borrows.append(borrow_info)
        
        return user_borrows
    except Exception as e:
        log_error(f"查询用户借阅记录异常：{str(e)}")
        return []

def check_overdue(days_limit=30):
    try:
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
            except Exception as parse_e:
                log_warning(f"解析借阅日期失败：{borrow.get('borrow_date', '')} - {str(parse_e)}")
                continue
        
        return overdue_list
    except Exception as e:
        log_error(f"检查逾期异常：{str(e)}")
        return []

def get_all_borrows():
    try:
        return read_csv(BORROWS_FILE)
    except Exception as e:
        log_error(f"获取所有借阅记录异常：{str(e)}")
        return []

def has_unreturned_borrows(book_id):
    """检查指定图书是否有未归还的借阅记录"""
    try:
        borrows = read_csv(BORROWS_FILE)
        for borrow in borrows:
            if borrow['book_id'] == str(book_id) and borrow['status'] == 'borrowed':
                return True
        return False
    except Exception as e:
        log_error(f"检查图书借阅状态异常：{str(e)}")
        return False