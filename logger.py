
import logging
from datetime import datetime
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name="chatbot_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    now = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"chatbot_{now}.log")

    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Contoh penggunaan:
# logger = get_logger()
# logger.info("User input: Wie lange dauert der Bau?")
