import os
from datetime import datetime
from global_var import logs_file_name, maximum_logs_lines, DEBUG


class Logger:
    @classmethod
    def _maintain_limit(cls):
        """
        ok i need to check my logs stay in 1000 line limit
        """
        if not os.path.exists(logs_file_name):
            return

        try:
            # Count lines in current file
            with open(logs_file_name, "r") as f:
                lines = f.readlines()

            # if file exceeds max lines, remove oldest lines
            if len(lines) >= maximum_logs_lines:
                # Keep only the most recent lines
                lines_to_keep = lines[-(maximum_logs_lines - 1) :]

                # write new lines
                with open(logs_file_name, "w") as f:
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
            with open(logs_file_name, "a") as f:
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
        if not os.path.exists(logs_file_name):
            return 0
        try:
            with open(logs_file_name, "r") as f:
                return sum(1 for _ in f)
        except:
            return 0


if __name__ == "__main__":
    Logger.info_log("Application started")
    Logger.debug_log("This is a debug message")
    Logger.warning_log("Low disk space")
    Logger.error_log("Failed to connect to database")
    Logger.info_log("User logged in")

    Logger.info_log("This message should create a new file")

    print(f"Current log count: {Logger.get_log_count()}")
