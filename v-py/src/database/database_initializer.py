import sqlite3
from typing import Optional

# from utils.logger import Logger
from ..utils.logger import Logger

_tables = [
    """
            CREATE TABLE IF NOT EXISTS translations (
                    id          INTEGER                                                     PRIMARY KEY AUTOINCREMENT,
                    source      TEXT CHECK( source IN ('fa', 'en', 'de', 'tr', 'ru') )      NOT NULL DEFAULT 'fa',
                    target      TEXT CHECK( target IN ('fa', 'en', 'de', 'tr', 'ru') )      NOT NULL DEFAULT 'en',
                    engine      TEXT CHECK( engine IN ('google', 'microsoft', 'yandex') )   NOT NULL DEFAULT 'google'
            );
    """,
    """
            CREATE TABLE IF NOT EXISTS actions (
                    id              INTEGER                                                     PRIMARY KEY AUTOINCREMENT,
                    chatbot         varchar(128)                                                NOT NULL DEFAULT 'gpt-4',
                    voice_lang      TEXT CHECK( voice_lang IN ('fa', 'en', 'de', 'tr', 'ru') )      NOT NULL DEFAULT 'en',
                    translations_id INTEGER                                                     NOT NULL,
                    FOREIGN KEY     (translations_id) REFERENCES translations (id) ON DELETE CASCADE
            );
    """,
    """
            CREATE TABLE IF NOT EXISTS users (
                    id          INTEGER                                   PRIMARY KEY AUTOINCREMENT,
                    chat_id     varchar(128)                              UNIQUE NOT NULL,
                    username    varchar(255),
                    role        TEXT CHECK( role IN ('ADMIN', 'USER') )   NOT NULL DEFAULT 'USER',
                    is_banned   BOOL                                      DEFAULT FALSE,
                    created_at  DATETIME                                  DEFAULT CURRENT_TIMESTAMP,
                    actions_id  INTEGER                                   NOT NULL,
                    FOREIGN KEY (actions_id) REFERENCES actions (id) ON DELETE CASCADE
            );
    """,
]


class DatabaseManager:
    _conn: Optional[sqlite3.Connection] = None

    @classmethod
    def _migrate_tables(cls):
        if cls._conn == None:
            Logger.error_log("database is not connnected yet, so we cannot migrate.")
        else:
            cur = cls._conn.cursor()
            for query in _tables:
                cur.execute(query)
            Logger.info_log("migrate finished.")

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._conn is None:
            cls._conn = sqlite3.connect("./datas/real.db")
            cls._conn.row_factory = sqlite3.Row
            cls._conn.execute("PRAGMA foreign_keys = ON")
            cls._migrate_tables()
        Logger.debug_log("one call for getting database _conn.")
        return cls._conn

    @classmethod
    def close_connection(cls):
        if cls._conn:
            cls._conn.close()
            cls._conn = None
            Logger.info_log("database __conn closed.")


if __name__ == "__main__":
    with DatabaseManager.get_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(result)
