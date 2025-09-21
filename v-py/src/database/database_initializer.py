import sqlite3
from typing import Optional


tables = [
    """
            CREATE TABLE IF NOT EXISTS users (
                    id          INTEGER                                   PRIMARY KEY AUTOINCREMENT,
                    chat_id     varchar(128)                              UNIQUE NOT NULL,
                    username    varchar(255),
                    role        TEXT CHECK( role IN ('ADMIN', 'USER') )   NOT NULL DEFAULT 'USER',
                    is_banned   BOOL                                      DEFAULT FALSE,
                    created_at  DATETIME                                  DEFAULT CURRENT_TIMESTAMP
            );
        """,
    """
            CREATE TABLE IF NOT EXISTS actions (
                    id          INTEGER                                   PRIMARY KEY AUTOINCREMENT,
                    created_at  DATETIME                                  DEFAULT CURRENT_TIMESTAMP,
                    user_id     INTEGER                                   NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """,
]


class DatabaseManager:
    _conn: Optional[sqlite3.Connection] = None

    @classmethod
    def _migrate_tables(cls):
        if cls._conn == None:
            print("database is not connnected yet.")
        else:
            cur = cls._conn.cursor()
            for query in tables:
                cur.execute(query)

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._conn is None:
            cls._conn = sqlite3.connect("./src/database/datas/real.db")
            cls._conn.row_factory = sqlite3.Row
            cls._conn.execute("PRAGMA foreign_keys = ON")
            cls._migrate_tables()
        return cls._conn

    @classmethod
    def close_connection(cls):
        if cls._conn:
            cls._conn.close()
            cls._conn = None


if __name__ == "__main__":
    with DatabaseManager.get_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(result)
