"""SQLite persistence layer; no Telegram or AI imports."""
import sqlite3
from pathlib import Path


def init_db(db_path: str | Path = "bot.sqlite3") -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, username TEXT NOT NULL)")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS items ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER NOT NULL, "
            "name TEXT NOT NULL, price REAL NOT NULL)"
        )


def save_user(telegram_id: int, username: str, db_path: str | Path = "bot.sqlite3") -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("INSERT INTO users(telegram_id, username) VALUES (?, ?) ON CONFLICT(telegram_id) DO UPDATE SET username=excluded.username", (telegram_id, username))


def get_user(telegram_id: int, db_path: str | Path = "bot.sqlite3") -> str | None:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("SELECT username FROM users WHERE telegram_id = ?", (telegram_id,)).fetchone()
    return row[0] if row else None


def add_item(telegram_id: int, name: str, price: float, db_path: str | Path = "bot.sqlite3") -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("INSERT INTO items(telegram_id, name, price) VALUES (?, ?, ?)", (telegram_id, name, price))


def list_items(telegram_id: int, db_path: str | Path = "bot.sqlite3") -> list[dict]:
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT name, price FROM items WHERE telegram_id = ? ORDER BY id", (telegram_id,)).fetchall()
    return [{"name": name, "price": price} for name, price in rows]


def total_price(telegram_id: int, db_path: str | Path = "bot.sqlite3") -> float:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("SELECT COALESCE(SUM(price), 0) FROM items WHERE telegram_id = ?", (telegram_id,)).fetchone()
    return row[0]


def clear_items(telegram_id: int, db_path: str | Path = "bot.sqlite3") -> int:
    """Delete the user's items and return how many were removed."""
    with sqlite3.connect(db_path) as conn:
        return conn.execute("DELETE FROM items WHERE telegram_id = ?", (telegram_id,)).rowcount
