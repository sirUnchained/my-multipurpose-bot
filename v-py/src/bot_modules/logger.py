import os
from datetime import datetime
from .configs import LOGS_PATH, LOGS_MAX_LINE, DEBUG


class Logger:
    @classmethod
    def _maintain_limit(cls):
        """
        ok i need to check my logs stay in 1000 line limit
        """
        if not os.path.exists(LOGS_PATH):
            return LOGS_PATH

        try:
            # Count lines in current file
            with open(LOGS_PATH, "r") as f:
                lines = f.readlines()

            # if file exceeds max lines, remove oldest lines
            if len(lines) >= LOGS_MAX_LINE:
                # Keep only the most recent lines
                lines_to_keep = lines[-(LOGS_MAX_LINE - 1) :]

                # write new lines
                with open(LOGS_PATH, "w") as f:
                    f.writelines(lines_to_keep)

        except Exception as e:
            print(f"Error maintaining log limit: {e}")

    @classmethod
    def _write_log(cls, level, message):
        """Write log entry to file"""
        if not DEBUG:
            return

        cls._maintain_limit()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        try:
            with open(LOGS_PATH, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to log file: {e}")

    @classmethod
    def info_log(cls, message):
        cls._write_log("INFO", message)

    @classmethod
    def warning_log(cls, message):
        cls._write_log("WARNING", message)

    @classmethod
    def error_log(cls, message):
        cls._write_log("ERROR", message)

    @classmethod
    def debug_log(cls, message):
        cls._write_log("DEBUG", message)

    @classmethod
    def get_log_count(cls):
        if not os.path.exists(LOGS_PATH):
            return 0
        try:
            with open(LOGS_PATH, "r") as f:
                return sum(1 for _ in f)
        except:
            return 0


if __name__ == "__main__":
    Logger.info_log("Application started")
    Logger.debug_log("This is a debug message")
    Logger.warning_log("Low disk space")
    Logger.error_log("Failed to connect to database")
    Logger.info_log("User logged in")
