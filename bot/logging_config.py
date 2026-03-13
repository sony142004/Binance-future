import logging
import os

def setup_logger():
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.DEBUG)

    # File handler
    fh = logging.FileHandler('logs/trading_bot.log')
    fh.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(fh)

    return logger

logger = setup_logger()
