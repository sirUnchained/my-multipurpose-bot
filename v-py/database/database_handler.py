import sqlite3
from contextlib import contextmanager
from typing import Generator, Optional


class DatabaseManager:
    _conn: Optional[sqlite3.Connection] = None

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._conn is None:
            cls._conn = sqlite3.connect("./database/datas/real.db")
            cls._conn.row_factory = sqlite3.Row
            cls._conn.execute("PRAGMA foreign_keys = ON")
        return cls._conn

    @classmethod
    def close_connection(cls):
        if cls._conn:
            cls._conn.close()
            cls._conn = None


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database operations"""
    conn = DatabaseManager.get_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        # todo : create a logger later
        pass


if __name__ == "__main__":
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(result)

    db = DatabaseManager.get_connection()
