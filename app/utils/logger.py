import logging
import sys


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            # logging.FileHandler('app.log', mode='a', encoding='utf-8')
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging is configured")
    return logger
