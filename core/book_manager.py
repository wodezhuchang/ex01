import os
from core.utils_csv import read_csv, write_csv, append_csv

BOOKS_FILE = os.path.join('data', 'books.csv')

def get_all_books():
    """返回所有图书列表，每本书为dict。"""
    return read_csv(BOOKS_FILE)

def add_book(book_info):
    """
    添加图书，book_info为dict。自动生成book_id。
    返回True成功，False表示ISBN重复。
    """
    books = get_all_books()
    # ISBN查重
    for book in books:
        if book['isbn'] == book_info['isbn']:
            return False
    # 生成新book_id
    max_id = max([int(book['book_id']) for book in books], default=0)
    book_info = book_info.copy()
    book_info['book_id'] = str(max_id + 1)
    append_csv(BOOKS_FILE, book_info)
    return True

def delete_book(book_id):
    """
    删除指定book_id的图书，返回True/False
    """
    books = get_all_books()
    new_books = [b for b in books if b['book_id'] != str(book_id)]
    if len(new_books) == len(books):  # 没找到
        return False
    write_csv(BOOKS_FILE, new_books)
    return True

def update_book(book_id, new_info):
    """
    修改book_id的图书信息，new_info为dict, 只更新提供的字段
    返回True/False
    """
    books = get_all_books()
    found = False
    for book in books:
        if book['book_id'] == str(book_id):
            book.update(new_info)
            found = True
            break
    if not found:
        return False
    write_csv(BOOKS_FILE, books)
    return True

def query_books(keyword):
    """
    按关键词（书名/作者/ISBN）模糊搜索，返回匹配图书列表
    """
    keyword = str(keyword).strip().lower()
    books = get_all_books()
    results = []
    for book in books:
        if (keyword in book['title'].lower() or
            keyword in book['author'].lower() or
            keyword in book['isbn'].lower()):
            results.append(book)
    return results
