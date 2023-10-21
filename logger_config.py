from loguru import logger

# Remove the default sink
logger.remove(0)

# Add a new sink that logs to a file
logger.add("my_log_file.log")
