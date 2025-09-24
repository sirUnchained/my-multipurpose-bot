DEBUG = True
LOGS_PATH = "./src/log.log"
LOGS_MAX_LINE = 1000
BOT_TOKEN = ""

tables = [
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
