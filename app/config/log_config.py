import logging

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)-12s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create handler (e.g., console)
handler = logging.StreamHandler()

# Create formatter
formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

# Assign formatter to handler
handler.setFormatter(formatter)
