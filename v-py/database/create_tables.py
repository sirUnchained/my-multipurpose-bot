from database_handler import *


def create_tables():
    tables = [
        """
            CREATE TABLE IF NOT EXISTS users (
                    id          INTEGER                                   PRIMARY KEY AUTOINCREMENT,
                    chat_id     INTEGER                                   UNIQUE NOT NULL,
                    username    varchar(255),
                    role        TEXT CHECK( role IN ('ADMIN', 'USER') )   NOT NULL DEFAULT 'USER',
                    created_at  DATETIME                                  DEFAULT CURRENT_TIMESTAMP
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS actions (
                    id          INTEGER                                   PRIMARY KEY AUTOINCREMENT,
                    chat_id     INTEGER                                   UNIQUE NOT NULL,
                    username    varchar(255),
                    created_at  DATETIME                                  DEFAULT CURRENT_TIMESTAMP,
                    user_id     INTEGER                                   NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """,
    ]

    with get_db() as db:
        cur = db.cursor()
        for query in tables:
            cur.execute(query)


if __name__ == "__main__":
    create_tables()
