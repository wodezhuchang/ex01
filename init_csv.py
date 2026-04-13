import os
import csv

def init_csv_files():
    """
    初始化 data 目录与三大 CSV 文件（users, books, borrows），
    不会覆盖已存在文件，只在文件不存在时创建并写入表头。
    """
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    files = {
        'users.csv':   ["user_id", "username", "password", "role"],
        'books.csv':   ["book_id", "title", "author", "isbn", "count"],
        'borrows.csv': ["borrow_id", "user_id", "book_id", "borrow_date", "return_date", "status"]
    }

    for filename, headers in files.items():
        file_path = os.path.join(data_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
