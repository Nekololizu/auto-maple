import logging
import os
import sys
from datetime import datetime
import traceback

# Ensure the logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Log file cap (Single log file with max size)
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB max size for the log file

# Generate log file name (using environment variable or default timestamp)
log_filename = os.getenv("LOG_FILE_NAME", f"auto_maple_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
log_file = os.path.join(LOG_DIR, log_filename)

# Set up the logger
logger = logging.getLogger("auto_maple")
log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
logger.setLevel(logging.DEBUG)  # We're only logging print() output, so DEBUG is fine for all output

# File handler for logging print() output
file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Stream handler for errors (to capture any error messages in stderr)
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

# Custom print redirection
class PrintLogger:
    def __init__(self, logger):
        self.logger = logger
        self.terminal = sys.stdout

    def write(self, message):
        if message.strip():  # Avoid logging empty lines
            self.logger.debug(message.strip())  # Log all print() output
            self.terminal.write(message)  # Still print to terminal

    def flush(self):
        self.terminal.flush()

# Redirect print() to the logger
sys.stdout = PrintLogger(logger)

# Custom error logger for stderr
class ErrorLogger:
    def __init__(self, logger):
        self.logger = logger
        self.terminal = sys.stderr

    def write(self, message):
        if message.strip():  # Avoid logging empty lines
            self.logger.error(message.strip())  # Log all error messages
            self.terminal.write(message)  # Still print to terminal

    def flush(self):
        self.terminal.flush()

# Redirect stderr to capture error messages
sys.stderr = ErrorLogger(logger)

# Function to catch unhandled exceptions and log them
def log_exception(exc_type, exc_value, exc_tb):
    # Only log uncaught exceptions, and don't log KeyboardInterrupt
    if exc_type is not KeyboardInterrupt:
        error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        logger.error(f"Unhandled exception: {error_message}")

# Set sys.excepthook to catch all uncaught exceptions
sys.excepthook = log_exception
