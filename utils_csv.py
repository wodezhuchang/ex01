import csv
import os

def read_csv(file_path):
    """
    读取CSV文件，返回列表[dict, ...]（首行为表头）。
    文件不存在返回空列表。
    """
    if not os.path.exists(file_path):
        return []
    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        # 你可选择记录log，这里返回空
        return []
    return data

def write_csv(file_path, data):
    """
    覆盖写入CSV文件，data为[dict, ...]，自动写入表头。
    """
    if not data:
        return  # 没有数据不写入
    fieldnames = data[0].keys()
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        pass  # 可加日志

def append_csv(file_path, row):
    """
    追加一行到CSV文件，row为dict，自动适配表头。
    如果文件不存在或无表头，则自动写表头再写入。
    """
    file_exists = os.path.exists(file_path)
    write_header = not file_exists or os.path.getsize(file_path) == 0
    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        pass  # 可加日志

