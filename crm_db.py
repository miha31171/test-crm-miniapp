import sqlite3
from datetime import datetime
from contextlib import closing

DB_PATH = "crm.db"

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        # Мастера
        cur.execute("CREATE TABLE IF NOT EXISTS masters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, telegram_id INTEGER)")
        # Свободные слоты (мастер создаёт)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_id INTEGER,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                status TEXT DEFAULT 'free',
                FOREIGN KEY(master_id) REFERENCES masters(id)
            )
        """)
        # Записи клиентов
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_id INTEGER NOT NULL,
                client_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                place TEXT NOT NULL,
                created_at TEXT,
                FOREIGN KEY(slot_id) REFERENCES slots(id)
            )
        """)
        conn.commit()


def add_master(name, telegram_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO masters (name, telegram_id) VALUES (?, ?)", (name, telegram_id))
        conn.commit()
        return cur.lastrowid

def get_masters():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM masters")
        return [{"id":r[0], "name":r[1]} for r in cur.fetchall()]

def add_slot(master_id, date, time):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO slots (master_id, date, time) VALUES (?, ?, ?)", (master_id, date, time))
        conn.commit()
        return cur.lastrowid

def get_free_slots():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, m.name, s.date, s.time 
            FROM slots s JOIN masters m ON s.master_id = m.id 
            WHERE s.status = 'free'
            ORDER BY s.date, s.time
        """)
        return [{"id":r[0],"master":r[1],"date":r[2],"time":r[3]} for r in cur.fetchall()]

def book_slot(slot_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE slots SET status = 'booked' WHERE id = ? AND status = 'free'", (slot_id,))
        return cur.rowcount > 0

def create_booking(slot_id, name, phone, place):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO bookings (slot_id, client_name, phone, place, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (slot_id, name, phone, place, datetime.now().isoformat()))
        conn.commit()
        return cur.lastrowid

def get_bookings():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT b.id, b.client_name, b.phone, b.place, s.date, s.time, m.name
            FROM bookings b JOIN slots s ON b.slot_id = s.id 
            JOIN masters m ON s.master_id = m.id
            ORDER BY b.created_at DESC LIMIT 50
        """)
        return [{"id":r[0],"name":r[1],"phone":r[2],"place":r[3],"date":r[4],"time":r[5],"master":r[6]} for r in cur.fetchall()]


# # ТЕСТОВЫЕ СЛОТЫ (удали потом)
# def add_test_slots():
#     masters = get_masters()
#     if masters:
#         master_id = masters[0]['id']  # Первый мастер
#         test_slots = [
#             ('2026-01-15', '14:00'), ('2026-01-15', '15:00'),
#             ('2026-01-16', '12:00'), ('2026-01-16', '17:00')
#         ]
#         for date, time in test_slots:
#             add_slot(master_id, date, time)
#         print("✅ Тестовые слоты добавлены!")

# add_test_slots()  # Выполнится при запуске


# Роли по TG ID (замени на свои)
ADMIN_TG_IDS = [60973352]  # ТВОИ TG ID здесь!
def is_admin(telegram_id):
    #return True  # Временно для всех!
    return telegram_id in ADMIN_TG_IDS
