import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

import logging
from logging.handlers import RotatingFileHandler

# Setup basic parameters for logging
logging_str = (
    "[%(asctime)s: %(levelname)s: %(module)s: %(funcName)s: %(lineno)d] %(message)s"
)
log_dir = "logs"
log_filename = "running_logs.log"
log_filepath = os.path.join(log_dir, log_filename)
max_log_size = 10 * 1024 * 1024  # 10 MB
backup_count = 3  # Number of backup logs to keep

# Ensure the log directory exists
os.makedirs(log_dir, exist_ok=True)

# Create a logger with a specified name
logger = logging.getLogger("<itcanbeanyname>")
logger.setLevel(logging.DEBUG)  # Set the logger to capture all levels of messages

# Create handlers for both file and console with different log levels
file_handler = RotatingFileHandler(
    log_filepath, maxBytes=max_log_size, backupCount=backup_count
)
file_handler.setLevel(logging.DEBUG)  # More verbose level for file
file_handler.setFormatter(logging.Formatter(logging_str))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(
    logging.INFO
)  # Less verbose level for console, but will show warnings and errors
console_handler.setFormatter(logging.Formatter(logging_str))

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Demonstrate logging at different levels
# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")