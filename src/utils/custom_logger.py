import logging

class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: "\033[90m%(message)s\033[0m",  # Grey
        logging.INFO: "\033[32mINFO: %(message)s\033[0m",  # Green
        logging.WARNING: "\033[33m%(asctime)s - %(levelname)s : %(message)s\033[0m",  # Yellow
        logging.ERROR: "\033[31m%(asctime)s - %(levelname)s : %(message)s\033[0m",  # Red
        logging.CRITICAL: "\033[41m%(asctime)s - %(levelname)s : %(message)s\033[0m",  # Red background
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def get_custom_logger(name): # public: used in all services
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    return logger
