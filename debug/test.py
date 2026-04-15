# test_final.py - 完整测试文件
###################
# #移至根目录下使用#
###################

import os
import sys
import tempfile
import shutil

# 先切换到临时目录
TEST_DIR = tempfile.mkdtemp()
ORIGINAL_DIR = os.getcwd()
os.chdir(TEST_DIR)
print(f"测试目录: {TEST_DIR}")

os.makedirs('data', exist_ok=True)

# 导入并初始化
import core.utils_csv as csv_utils
import core.init_csv as init_csv
init_csv.init_csv_files()

import core.user_manager as user_manager
import core.book_manager as book_manager
import core.borrow_manager as borrow_manager
import core.import_export as import_export


def test_user():
    """用户管理测试"""
    print("\n" + "=" * 50)
    print("【用户管理】")
    print("=" * 50)
    
    # 注册
    assert user_manager.user_register("testuser", "pass123", "user") == True
    print("  ✓ 注册用户")
    
    assert user_manager.user_register("testuser", "pass123", "user") == False
    print("  ✓ 重复注册被拒绝")
    
    assert user_manager.user_register("admin1", "admin123", "admin") == True
    print("  ✓ 注册管理员")
    
    # 登录
    user = user_manager.user_login("testuser", "pass123")
    assert user is not None and user['role'] == 'user'
    print("  ✓ 用户登录")
    
    assert user_manager.user_login("testuser", "wrong") is None
    print("  ✓ 错误密码被拒绝")
    
    user = user_manager.user_login("admin1", "admin123")
    assert user is not None and user['role'] == 'admin'
    print("  ✓ 管理员登录")
    
    # 修改密码
    assert user_manager.change_password("testuser", "pass123", "newpass") == True
    print("  ✓ 修改密码")
    
    assert user_manager.user_login("testuser", "newpass") is not None
    print("  ✓ 新密码可登录")
    
    return user_manager.user_login("testuser", "newpass")


def test_book():
    """图书管理测试"""
    print("\n" + "=" * 50)
    print("【图书管理】")
    print("=" * 50)
    
    # 添加图书
    book1 = {"title": "Python编程", "author": "张三", "isbn": "978-7-111-12345-6", "count": "5"}
    assert book_manager.add_book(book1) == True
    print("  ✓ 添加图书")
    
    assert book_manager.add_book(book1) == False
    print("  ✓ ISBN重复被拒绝")
    
    book2 = {"title": "Java编程", "author": "李四", "isbn": "978-7-111-67890-1", "count": "3"}
    assert book_manager.add_book(book2) == True
    print("  ✓ 添加第二本书")
    
    # 获取所有图书
    books = book_manager.get_all_books()
    assert len(books) == 2
    print(f"  ✓ 获取图书列表 ({len(books)} 本)")
    
    # 更新图书
    book_id = books[0]['book_id']
    assert book_manager.update_book(book_id, {"title": "Python编程(第2版)"}) == True
    print("  ✓ 更新图书")
    
    # 搜索图书
    results = book_manager.query_books("Python")
    assert len(results) >= 1
    print(f"  ✓ 搜索图书 (找到 {len(results)} 本)")
    
    # 删除图书
    assert book_manager.delete_book(book_id) == True
    print("  ✓ 删除图书")
    
    books = book_manager.get_all_books()
    assert len(books) == 1
    print(f"  ✓ 删除后剩余 {len(books)} 本")
    
    return books[0]['book_id'] if books else None


def test_borrow(user_id, book_id):
    """借阅管理测试"""
    print("\n" + "=" * 50)
    print("【借阅管理】")
    print("=" * 50)
    
    if not book_id:
        print("  ⚠ 无图书，跳过借阅测试")
        return
    
    # 借书
    assert borrow_manager.borrow_book(user_id, book_id) == True
    print("  ✓ 借书成功")
    
    assert borrow_manager.borrow_book(user_id, book_id) == False
    print("  ✓ 重复借书被拒绝")
    
    # 检查库存
    books = book_manager.get_all_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    assert int(book['count']) == 2  # 原来3本
    print("  ✓ 库存已更新")
    
    # 获取借阅记录
    records = borrow_manager.get_user_borrows(user_id)
    assert len(records) >= 1
    print(f"  ✓ 获取借阅记录 ({len(records)} 条)")
    
    # 归还
    borrows = borrow_manager.get_all_borrows()
    borrowed = next((b for b in borrows if b['status'] == 'borrowed'), None)
    if borrowed:
        assert borrow_manager.return_book(borrowed['borrow_id']) == True
        print("  ✓ 还书成功")
        
        assert borrow_manager.return_book(borrowed['borrow_id']) == False
        print("  ✓ 重复还书被拒绝")
    
    # 逾期检查
    overdue = borrow_manager.check_overdue()
    print(f"  ✓ 逾期检查 (发现 {len(overdue)} 条)")


def test_import():
    """导入导出测试"""
    print("\n" + "=" * 50)
    print("【批量导入】")
    print("=" * 50)
    
    csv_path = os.path.join(TEST_DIR, 'import_test.csv')
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        f.write("title,author,isbn,count\n")
        f.write("导入书1,作者A,978-7-111-77777-1,10\n")
        f.write("导入书2,作者B,978-7-111-88888-2,20\n")
    
    result = import_export.import_books_from_csv(csv_path)
    assert result['success'] == 2
    print(f"  ✓ 批量导入 ({result['success']} 本)")
    
    os.remove(csv_path)


def run_all_tests():
    print("\n" + "=" * 60)
    print("开始运行图书管理系统测试")
    print("=" * 60)
    
    try:
        user = test_user()
        book_id = test_book()
        test_borrow(user['user_id'], book_id)
        test_import()
        
        print("\n" + "=" * 60)
        print("所有测试通过！✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        os.chdir(ORIGINAL_DIR)
        shutil.rmtree(TEST_DIR, ignore_errors=True)


if __name__ == "__main__":
    run_all_tests()
