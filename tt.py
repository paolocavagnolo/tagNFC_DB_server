import os
import json
import logging.config

def setup_logging(
    default_path='logging.json',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging()
logger = logging.getLogger()

logger.debug('often makes a very good meal of %r', 'visiting tourists')
logger.info('ciao')
logger.error('ciaone')
logger.debug('often makes a very good meal of %r', 'visiting tourists')
