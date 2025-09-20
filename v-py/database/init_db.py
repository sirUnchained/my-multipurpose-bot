import sqlite3

conn = None


def initDb() -> bool:
    try:
        global conn
        conn = sqlite3.Connection("real.db")
        print("database just started!")
        return True
    except sqlite3.OperationalError as e:
        print("something failed to initialize db:", e)
        return False
