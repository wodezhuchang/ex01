from core.utils_csv import read_csv, write_csv, append_csv
from core.config import BOOKS_FILE, BORROWS_FILE
from core.logger import log_info, log_error

def get_all_books():
    try:
        return read_csv(BOOKS_FILE)
    except Exception as e:
        log_error(f"获取所有图书异常：{str(e)}")
        return []

def add_book(book_info):
    try:
        books = get_all_books()
        for book in books:
            if book['isbn'] == book_info['isbn']:
                log_error(f"添加图书失败：ISBN {book_info['isbn']} 已存在")
                return False
        max_id = max([int(book['book_id']) for book in books], default=0)
        book_info = book_info.copy()
        book_info['book_id'] = str(max_id + 1)
        append_csv(BOOKS_FILE, book_info)
        log_info(f"添加图书成功：{book_info.get('title', '')} (ISBN: {book_info.get('isbn', '')})")
        return True
    except Exception as e:
        log_error(f"添加图书异常：{str(e)}")
        return False

def delete_book(book_id):
    try:
        # 检查是否有未归还的借阅记录
        borrows = read_csv(BORROWS_FILE)
        for borrow in borrows:
            if borrow['book_id'] == str(book_id) and borrow['status'] == 'borrowed':
                log_error(f"删除图书失败：图书ID {book_id} 存在未归还的借阅记录")
                return False
        
        books = get_all_books()
        book_title = ""
        for book in books:
            if book['book_id'] == str(book_id):
                book_title = book.get('title', '')
                break
        
        new_books = [b for b in books if b['book_id'] != str(book_id)]
        if len(new_books) == len(books):
            log_error(f"删除图书失败：图书ID {book_id} 不存在")
            return False
        write_csv(BOOKS_FILE, new_books)
        log_info(f"删除图书成功：{book_title} (ID: {book_id})")
        return True
    except Exception as e:
        log_error(f"删除图书异常：{str(e)}")
        return False

def update_book(book_id, new_info):
    try:
        books = get_all_books()
        found = False
        for book in books:
            if book['book_id'] == str(book_id):
                book.update(new_info)
                found = True
                break
        if not found:
            log_error(f"更新图书失败：图书ID {book_id} 不存在")
            return False
        write_csv(BOOKS_FILE, books)
        log_info(f"更新图书成功：图书ID {book_id}")
        return True
    except Exception as e:
        log_error(f"更新图书异常：{str(e)}")
        return False

def query_books(keyword):
    try:
        keyword = str(keyword).strip().lower()
        books = get_all_books()
        results = []
        for book in books:
            if (keyword in book['title'].lower() or
                keyword in book['author'].lower() or
                keyword in book['isbn'].lower()):
                results.append(book)
        return results
    except Exception as e:
        log_error(f"查询图书异常：{str(e)}")
        return []