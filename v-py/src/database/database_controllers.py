import sqlite3
import datetime
from typing import Optional, Any, Dict

from database_initializer import DatabaseManager


class Actions_db_controller:
    def __init__(self, action_data: Dict[str, Any]) -> None:
        if action_data:
            self.id = action_data.get("id")
            self.chatbot = action_data.get("chatbot")
            self.voice_lang = action_data.get("voice_lang")
            self.translations_id = action_data.get("translations_id")
        else:
            self.id = None
            self.chatbot = None
            self.voice_lang = None
            self.translations_id = None

    @classmethod
    def create_action(cls):
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()

                cursor.execute("INSERT INTO translations (source) VALUES ('fa')")
                translations_id = cursor.lastrowid
                db.commit()

                cursor.execute(
                    "INSERT INTO actions (translations_id) VALUES (?)",
                    (translations_id,),
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
            print(f"error in creating action: {e}")
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
            print(f"error in finding action: {e}")
            return None

    @classmethod
    def update_action(cls, action_id: int, key: str, value: Any):
        try:
            if key == "translations":
                cls._update_translation(action_id, value)
                return

            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                query = f"UPDATE translations SET {key} = ? WHERE id = ?"

                cursor.execute(query, (value, action_id))

                db.commit()
        except Exception as e:
            print(f"error in updating action: {e}")
            return None

    @classmethod
    def _update_translation(cls, action_id: int, translations: dict[str, str]):
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
            print(f"error in updating translation: {e}")
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
            print(f"error in updating username: {e}")

    @classmethod
    def find_single_user(cls, chat_id: str) -> Optional["Users_db_controller"]:
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM users WHERE chat_id == ?", (chat_id,))
                user = cursor.fetchone()

                return cls(dict(user))

        except Exception as e:
            print(f"user not found: {e}")
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
            print(f"Error changing user ban status: {e}")

    @classmethod
    def create_user(cls, chatid: str, username: str) -> Optional["Users_db_controller"]:
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
                    print(f"error, action not exists for user {username}")
                    return

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
            print("user already exist")
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None


if __name__ == "__main__":
    # print(Users_db_controller.create_user("6565", "jon"))
    # print(
    #     Actions_db_controller.update_action(
    #         1, "translations", {"source": "de", "target": "tr", "engine": "yandex"}
    #     )
    # )
    # print(Actions_db_controller.find_single_action(1))
    print("hiii")
