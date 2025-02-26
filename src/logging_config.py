import logging

LOG_FORMAT = "%(asctime)s:%(name)s:%(levelname)s:%(pathname)s:%(lineno)d:%(message)s"


def setup_logger(name, log_file="swissmade365.log", log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # prevent duplicate
    if logger.hasHandlers():
        return logger

    # console handler

    # file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
