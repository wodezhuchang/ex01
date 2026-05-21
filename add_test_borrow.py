from datetime import datetime
from core.utils_csv import read_csv, write_csv, append_csv
from core.config import BORROWS_FILE

# 添加一条未归还的借阅记录（book_id=102）
borrows = read_csv(BORROWS_FILE)
max_id = max([int(b['borrow_id']) for b in borrows], default=0)

new_borrow = {
    "borrow_id": str(max_id + 1),
    "user_id": "1",
    "book_id": "102",
    "borrow_date": datetime.now().strftime("%Y-%m-%d"),
    "return_date": "",
    "status": "borrowed"
}

append_csv(BORROWS_FILE, new_borrow)
print(f"已添加未归还借阅记录：{new_borrow}")