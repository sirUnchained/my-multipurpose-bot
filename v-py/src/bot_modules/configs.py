from dotenv import load_dotenv
from os import getenv

load_dotenv()


def get_env_var(name, default=None, cast_func=None):
    value = getenv(name)
    if value is None:
        return default
    return cast_func(value) if cast_func else value


PROXY = str(get_env_var("PROXY"))
BOT_TOKEN = str(get_env_var("BOT_TOKEN"))
API_TOKEN = str(get_env_var("API_TOKEN"))
DEBUG = get_env_var(
    "DEBUG", default=True, cast_func=lambda v: v.lower() in ("1", "true", "yes")
)
LOGS_PATH = get_env_var("LOGS_PATH", default="./src/log.log")
LOGS_MAX_LINE = int(get_env_var("LOGS_MAX_LINE", default=1000, cast_func=int))
