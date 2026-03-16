import logging.config
from src.env import get_env
env = get_env()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            # Added %(funcName)s for the function name
            "format": "%(asctime)s.%(msecs)03d | %(levelname)s | [%(name)s][%(funcName)s] : %(message)s",
            # datefmt defines how the 'asctime' part looks before the ms are added
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": env.LOG_LEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
        "handlers": ["default"],
        "level": env.LOG_LEVEL
        
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)