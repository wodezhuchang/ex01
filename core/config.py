import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'ui', 'data')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

BOOKS_FILE = os.path.join(DATA_DIR, 'books.csv')
USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
BORROWS_FILE = os.path.join(DATA_DIR, 'borrows.csv')
LOG_FILE = os.path.join(DATA_DIR, 'app.log')