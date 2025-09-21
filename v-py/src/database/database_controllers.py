import sqlite3
import datetime
from typing import Optional, Any, Dict

from database_initializer import DatabaseManager


class Users_db_controller:
    def __init__(self, user_data: Dict[str, Any]) -> None:
        if user_data:
            self.id = user_data.get("id")
            self.chat_id = user_data.get("chat_id")
            self.username = user_data.get("username")
            self.role = user_data.get("role")
            self.is_banned = user_data.get("is_banned")
            self.created_at = user_data.get("created_at")
        else:
            self.id = None
            self.chat_id = None
            self.username = None
            self.role = None
            self.is_banned = None
            self.created_at = None

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
    def create_user(
        cls,
        chatid: str,
        username: str,
    ) -> Optional["Users_db_controller"]:
        """say hello to new user"""
        try:
            with DatabaseManager.get_connection() as db:
                cursor = db.cursor()

                users_count = cursor.lastrowid
                role = "ADMIN" if (users_count == None) else "USER"
                ceratedAt = datetime.datetime.now()

                cursor.execute(
                    """
                    INSERT INTO users (username, chat_id, username, role, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (username, chatid, username, role, ceratedAt),
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


# class

if __name__ == "__main__":
    print(Users_db_controller.find_single_user("76767"))
