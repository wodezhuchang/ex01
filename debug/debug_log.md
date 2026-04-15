## 问题总结

在调试过程中发现了以下 **Bug**：

### 1. 模块导入名称不一致
| 文件 | 错误导入 | 正确导入 |
|------|---------|---------|
| `book_manager.py` | `from core.csv_utils` | `from core.utils_csv` |
| `borrow_manager.py` | `from core.csv_utils` | `from core.utils_csv` |
| `import_export.py` | `from core.csv_utils` | `from core.utils_csv` |
| `user_manager.py` | `from core.csv_utils` | `from core.utils_csv` |

### 2. CSV 文件编码问题（BOM）
Windows 下 CSV 文件可能有 UTF-8 BOM，导致 `DictReader` 解析错位。

**修复**：所有文件操作使用 `encoding='utf-8-sig'` 替代 `'utf-8'`

### 3. `append_csv` 字段顺序错误
原代码按字典 keys 顺序写入，但与 CSV 表头顺序不一致，导致数据错位。

**修复**：先读取现有文件的表头，按照表头顺序提取并写入数据。

---

**测试文件 `test.py`** 已完成，可用于验证系统功能。
