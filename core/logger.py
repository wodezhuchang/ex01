import datetime
from core.config import LOG_FILE

def log(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"日志写入失败: {e}")
    
    if level in ["ERROR", "CRITICAL"]:
        print(log_entry.strip())

def log_info(message):
    log(message, "INFO")

def log_error(message):
    log(message, "ERROR")

def log_warning(message):
    log(message, "WARNING")

def log_debug(message):
    log(message, "DEBUG")