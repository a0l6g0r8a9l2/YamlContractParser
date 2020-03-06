import os
import sys
from logging import getLogger

from settings import API_TOKEN, proxies

logger = getLogger(__name__)


def load_config():
    try:
        conf_name = os.environ.get('BOT_ENV')
        logger.debug("Loaded config \"{}\" - OK".format(conf_name))
        if conf_name != 'prod':
            return API_TOKEN, proxies
        else:
            return os.environ.get('API_TOKEN'), os.environ.get('proxies')
    except (TypeError, ValueError, ImportError):
        logger.error("Invalid config \"{}\"")
        sys.exit(1)
