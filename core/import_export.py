import os
from core.utils_csv import read_csv, append_csv

BOOKS_FILE = os.path.join('data', 'books.csv')

def import_books_from_csv(file_path):
    """
    从外部CSV文件批量导入图书。
    file_path: 外部CSV文件路径（需包含 title, author, isbn, count 字段）
    返回: {"success": 成功数, "failed": 失败数, "errors": [错误信息列表]}
    """
    result = {"success": 0, "failed": 0, "errors": []}
    
    # 1. 检查文件是否存在
    if not os.path.exists(file_path):
        result["errors"].append(f"文件不存在: {file_path}")
        return result
    
    # 2. 读取现有图书（用于ISBN查重）
    existing_books = read_csv(BOOKS_FILE)
    existing_isbns = {book['isbn'] for book in existing_books}
    
    # 3. 读取外部导入文件
    import csv
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        result["errors"].append(f"文件读取失败: {str(e)}")
        return result
    
    if not rows:
        result["errors"].append("导入文件为空")
        return result
    
    # 4. 生成新book_id（基于现有最大ID）
    max_id = max([int(book['book_id']) for book in existing_books], default=0)
    next_id = max_id + 1
    
    # 5. 逐行校验并导入
    for idx, row in enumerate(rows, start=1):
        # 校验必要字段
        required_fields = ['title', 'author', 'isbn', 'count']
        missing = [f for f in required_fields if not row.get(f, '').strip()]
        if missing:
            result["failed"] += 1
            result["errors"].append(f"第{idx}行缺少字段: {', '.join(missing)}")
            continue
        
        # 校验ISBN重复
        isbn = row['isbn'].strip()
        if isbn in existing_isbns:
            result["failed"] += 1
            result["errors"].append(f"第{idx}行 ISBN重复: {isbn}")
            continue
        
        # 写入新图书
        new_book = {
            "book_id": str(next_id),
            "title": row['title'].strip(),
            "author": row['author'].strip(),
            "isbn": isbn,
            "count": row['count'].strip()
        }
        append_csv(BOOKS_FILE, new_book)
        
        # 更新状态
        existing_isbns.add(isbn)
        next_id += 1
        result["success"] += 1
    
    return result
