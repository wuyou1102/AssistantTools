# -*- encoding:UTF-8 -*-
import logging.config
from Config.Path import LOG
from os.path import join

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'delay': True,
            'filename': join(LOG, 'a.log'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    }
})
