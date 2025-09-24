from dotenv import load_dotenv
from os import getenv

load_dotenv()


BOT_TOKEN = getenv("BOT_TOKEN")
DEBUG = True if getenv("DEBUG") is None else bool(getenv("DEBUG"))
LOGS_PATH = "/" if getenv("LOGS_PATH") is None else getenv("LOGS_PATH")
LOGS_MAX_LINE = (
    1000 if getenv("LOGS_MAX_LINE") is None else int(getenv("LOGS_MAX_LINE"))
)
