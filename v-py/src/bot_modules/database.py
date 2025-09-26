import datetime
from typing import Optional, Any, Dict
import sqlite3
from .logger import Logger

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
            CREATE TABLE IF NOT EXISTS ais (
                    id          INTEGER                                                     PRIMARY KEY AUTOINCREMENT,
                    model       TEXT CHECK( model IN ('gpt-4') )                            NOT NULL DEFAULT 'gpt-4',
                    use_count   INTEGER                                                     DEFAULT 0
            );
    """,
    """
            CREATE TABLE IF NOT EXISTS actions (
                    id              INTEGER                                                                           PRIMARY KEY AUTOINCREMENT,
                    current_action  TEXT CHECK( current_action IN ('translate', 'ais', 'pc_control', 'text_voice') )  NOT NULL DEFAULT 'translate',
                    voice_lang      TEXT CHECK( voice_lang IN ('fa', 'en', 'de', 'tr', 'ru') )                        NOT NULL DEFAULT 'en',
                    translations_id INTEGER                                                                           NOT NULL,
                    ais_id          INTEGER                                                                           NOT NULL,
                    FOREIGN KEY (translations_id) REFERENCES translations (id) ON DELETE CASCADE
                    FOREIGN KEY (ais_id) REFERENCES ais (id) ON DELETE CASCADE
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
            Logger.debug_log("migrate started.")
            for query in _tables:
                cur.execute(query)
            Logger.debug_log("migrate finished.")

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._conn is None:
            Logger.warning_log("database _conn is null, so we try to init dataase.")
            cls._conn = sqlite3.connect(
                "./src/db_file/main.db", check_same_thread=False
            )
            cls._conn.row_factory = sqlite3.Row
            cls._conn.execute("PRAGMA foreign_keys = ON")
            cls._migrate_tables()
        Logger.info_log("one call for getting database _conn.")
        return cls._conn

    @classmethod
    def close_connection(cls):
        if cls._conn:
            cls._conn.close()
            cls._conn = None
            Logger.info_log("database __conn closed.")


class Translation_db_controller:
    def __init__(self, translation_data: Dict[str, Any]) -> None:
        if translation_data:
            self.source = translation_data.get("source")
            self.target = translation_data.get("target")
            self.engine = translation_data.get("engine")
        else:
            self.source = None
            self.target = None
            self.engine = None

    @classmethod
    def update_translation(cls, action_id: int, translations: dict[str, str]):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                query = "UPDATE translations SET source = ?, target = ?, engine = ? WHERE id = ?"

                cursor.execute(
                    query,
                    (
                        translations.get("source"),
                        translations.get("target"),
                        translations.get("engine"),
                        action_id,
                    ),
                )

                db.commit()
        except Exception as e:
            Logger.error_log(f"error in updating translations: {e}")
            return None

    @classmethod
    def find_single_translation(cls, id: int):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()

                cursor.execute("SELECT * FROM translations WHERE id = ?", (id,))
                translation = cursor.fetchone()

                if translation:
                    return cls(dict(translation))
        except Exception as e:
            Logger.error_log(f"error in finding translations: {e}")
            return None


class Actions_db_controller:
    def __init__(self, action_data: Dict[str, Any]) -> None:
        if action_data:
            self.id = action_data.get("id")
            self.chatbot = action_data.get("chatbot")
            self.voice_lang = action_data.get("voice_lang")
            self.translations_id = action_data.get("translations_id")
            self.ais_id = action_data.get("ais_id")
            self.current_action = action_data.get("current_action")
        else:
            self.id = None
            self.chatbot = None
            self.voice_lang = None
            self.translations_id = None
            self.ais_id = None
            self.current_action = None

    @classmethod
    def create_action(cls):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()

                cursor.execute("INSERT INTO translations (source) VALUES ('fa')")
                translations_id = cursor.lastrowid
                db.commit()

                cursor.execute("INSERT INTO ais (model) VALUES (?)", ("gpt-4",))
                ais_id = cursor.lastrowid
                db.commit()

                cursor.execute(
                    "INSERT INTO actions (translations_id, ais_id) VALUES (?, ?)",
                    (translations_id, ais_id),
                )
                db.commit()

                # getting created action
                cursor.execute(
                    "SELECT * FROM actions WHERE id = ?", (cursor.lastrowid,)
                )
                actions = cursor.fetchone()

                if actions:
                    return cls(dict(actions))
        except Exception as e:
            Logger.error_log(f"error in creating action: {e}")
            return None

    @classmethod
    def find_single_action(cls, action_id: int):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()

                cursor.execute("SELECT * FROM actions WHERE id = ?", (action_id,))
                action = cursor.fetchone()

                if action:
                    return cls(dict(action))
        except Exception as e:
            Logger.error_log(f"error in finding action: {e}")
            return None

    @classmethod
    def update_action(cls, action_id: int, key: str, value: Any):
        try:
            if key == "translations":
                Translation_db_controller.update_translation(action_id, value)
                return

            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                query = f"UPDATE actions SET {key} = ? WHERE id = ?"

                cursor.execute(query, (value, action_id))

                db.commit()
        except Exception as e:
            Logger.error_log(f"error in updating action: {e}")
            return None

    @classmethod
    def increase_gpt_use(cls, ai_id: int):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                query = "UPDATE translations SET source = ?, target = ?, engine = ? WHERE id = ?"

                cursor.execute("SELECT * FROM ais WHERE id = ?", (ai_id,))
                ai = cursor.fetchone()
                if ai is None:
                    Logger.error_log(
                        f"couldn't find AI model in database with id {ai_id}"
                    )
                    return None

                cursor.execute(
                    "UPDATE ais SET use_count = ? WHERE id = ?",
                    (ai.use_count + 1, ai.id),
                )
                db.commit()
        except Exception as e:
            Logger.error_log(f"error in updating translation: {e}")
            return None


class Users_db_controller:
    def __init__(self, user_data: Dict[str, Any]) -> None:
        if user_data:
            self.id = user_data.get("id")
            self.chat_id = user_data.get("chat_id")
            self.username = user_data.get("username")
            self.role = user_data.get("role")
            self.is_banned = user_data.get("is_banned")
            self.created_at = user_data.get("created_at")
            self.actions_id = user_data.get("actions_id")
        else:
            self.id = None
            self.chat_id = None
            self.username = None
            self.role = None
            self.is_banned = None
            self.created_at = None
            self.actions_id = None

    @classmethod
    def update_user(cls, chat_id: str, username: str):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                cursor.execute(
                    "UPDATE users SET username = ? WHERE chat_id = ?",
                    (
                        username,
                        chat_id,
                    ),
                )

                db.commit()

        except Exception as e:
            Logger.error_log(f"error in updating username: {e}")

    @classmethod
    def find_single_user(cls, chat_id: str) -> Optional["Users_db_controller"]:
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM users WHERE chat_id == ?", (chat_id,))
                user = cursor.fetchone()

                return cls(dict(user))

        except Exception as e:
            Logger.error_log(f"user not found: {e}")
            return None

    @classmethod
    def change_user_ban_status(cls, chat_id: str):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                cursor.execute(
                    "UPDATE users SET is_banned = ? WHERE chat_id = ?",
                    (
                        True,
                        chat_id,
                    ),
                )
                db.commit()
        except Exception as e:
            Logger.error_log(f"Error changing user ban status: {e}")
            return None

    @classmethod
    def create_user(cls, chatid: str, username) -> Optional["Users_db_controller"]:
        """say hello to new user"""
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                users_count = cursor.lastrowid
                role = "ADMIN" if (users_count == None) else "USER"
                ceratedAt = datetime.datetime.now()

                actions = Actions_db_controller.create_action()
                actions_id = actions.id if actions is not None else -1

                if actions_id == -1:
                    Logger.error_log(f"error, action not exists for user {username}")
                    return None

                cursor.execute(
                    """
                    INSERT INTO users (username, chat_id, username, role, created_at, actions_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (username, chatid, username, role, ceratedAt, actions_id),
                )

                # getting created user
                cursor.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,))
                user = cursor.fetchone()
                db.commit()

                if user:
                    return cls(dict(user))
        except sqlite3.IntegrityError:
            Logger.warning_log(f"user with username '{username}' already exist")
            return None
        except Exception as e:
            Logger.error_log(f"Error creating user: {e}")
            return None


if __name__ == "__main__":
    with DatabaseManager.get_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(result)
