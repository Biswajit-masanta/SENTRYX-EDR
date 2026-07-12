from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "database.db"

print("Using database:", DB_PATH)

def get_connection():
    return sqlite3.connect(DB_PATH)