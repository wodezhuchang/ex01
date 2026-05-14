from core.borrow_manager import has_unreturned_borrows

# 测试图书ID 102，它有未归还的借阅记录（borrowed状态）
result = has_unreturned_borrows(102)
print(f"图书ID 102 是否有未归还借阅: {result}")

# 测试图书ID 5，它的借阅记录都已归还
result = has_unreturned_borrows(5)
print(f"图书ID 5 是否有未归还借阅: {result}")

# 测试图书ID 99，它的借阅记录都已归还
result = has_unreturned_borrows(99)
print(f"图书ID 99 是否有未归还借阅: {result}")