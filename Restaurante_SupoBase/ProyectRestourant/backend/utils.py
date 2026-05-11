import logging

# Simple logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def log(msg, level="info"):
    if level == "error":
        logging.error(msg)
    else:
        logging.info(msg)
