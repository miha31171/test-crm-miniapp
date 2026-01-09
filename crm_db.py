# crm_db.py
import sqlite3
from contextlib import closing

DB_PATH = "crm.db"

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            contact TEXT,
            comment TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            master TEXT,
            zone TEXT,
            price REAL,
            status TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
        """)
        conn.commit()

def add_client(name, phone, contact, comment):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clients (name, phone, contact, comment) VALUES (?, ?, ?, ?)",
            (name, phone, contact, comment),
        )
        conn.commit()
        return cur.lastrowid

def add_session(client_id, date, time, master, zone, price, status):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO sessions
               (client_id, date, time, master, zone, price, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (client_id, date, time, master, zone, price, status),
        )
        conn.commit()
        return cur.lastrowid

def get_upcoming_sessions(limit=20):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id,
                   c.name,
                   s.date,
                   s.time,
                   s.master,
                   s.zone,
                   s.price,
                   s.status
            FROM sessions s
            JOIN clients c ON s.client_id = c.id
            ORDER BY s.date, s.time
            LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
        keys = ["id", "client_name", "date", "time", "master", "zone", "price", "status"]
        return [dict(zip(keys, r)) for r in rows]
