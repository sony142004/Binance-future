import logging
import os
import sys

def setup_logger():
    log_dir = '/tmp/logs' if os.environ.get('VERCEL') == '1' else 'logs'
    log_file = os.path.join(log_dir, 'trading_bot.log')
    
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if not logger.handlers:
        # Stream handler (for Vercel Function logs)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        
        # File handler (Optional/Fallback)
        try:
            os.makedirs(log_dir, exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception:
            pass # Vercel read-only system fallback

    return logger

logger = setup_logger()
