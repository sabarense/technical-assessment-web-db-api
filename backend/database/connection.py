import sqlite3
from backend.database.schema import criar_tabelas

def create_connection():
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON;')
    criar_tabelas(conn)
    return conn
