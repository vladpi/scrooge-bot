import logging.config
import sys

from .settings import settings

MAIN_LOGGER = 'console'
LOGGER_CONF_DICT = {
    'class': 'logging.StreamHandler',
    'formatter': 'verbose',
    'stream': sys.stdout,
    'level': settings.LOG_LEVEL.upper(),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(log_color)s%(asctime)s [%(levelname)s] [%(name)s] %(message)s (%(filename)s:%(lineno)d)',  # noqa
            '()': 'colorlog.ColoredFormatter',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        }
    },
    'handlers': {
        MAIN_LOGGER: {**LOGGER_CONF_DICT},
        'blackhole': {'level': 'DEBUG', 'class': 'logging.NullHandler'},
    },
    'loggers': {
        'fastapi': {'level': 'INFO', 'handlers': [MAIN_LOGGER]},
        'uvicorn.error': {'level': 'INFO', 'handlers': [MAIN_LOGGER], 'propagate': False},
        'uvicorn.access': {'level': 'INFO', 'handlers': [MAIN_LOGGER], 'propagate': False},
        'uvicorn': {'level': 'INFO', 'handlers': [MAIN_LOGGER], 'propagate': False},
        '': {
            'level': settings.LOG_LEVEL.upper(),
            'handlers': [MAIN_LOGGER],
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)
