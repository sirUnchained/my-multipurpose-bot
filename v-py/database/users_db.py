import sqlite3
import datetime
from database_handler import *


class User_controller:

    @classmethod
    def create(
        cls,
        chatid: int,
        username: str,
    ):
        """say hello to new user"""
        try:
            with get_db() as db:
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
                user_data = cursor.fetchone()

                db.commit()

                if user_data:
                    return dict(user_data)
        except sqlite3.IntegrityError:
            print("user already exist")
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None


if __name__ == "__main__":
    print(User_controller.create(76767, "bob"))
