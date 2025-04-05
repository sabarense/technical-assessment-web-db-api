import sqlite3

def create_connection():
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn
