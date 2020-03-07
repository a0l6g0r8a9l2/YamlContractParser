import os
import sys
from logging import getLogger

logger = getLogger(__name__)


def load_config():
    try:
        conf_name = os.environ.get('BOT_ENV')
        logger.debug("Loaded config \"{}\" - OK".format(conf_name))
        if conf_name != 'prod':
            from settings import API_TOKEN, proxies
            return API_TOKEN, proxies, conf_name
        else:
            return os.environ.get('API_TOKEN'), None, conf_name
    except (TypeError, ValueError, ImportError):
        logger.error("Invalid config \"{}\"")
        sys.exit(1)
