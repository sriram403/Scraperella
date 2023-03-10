import logging
from datetime import datetime
from CUKU.constant import *
import os

LOG_DIR = "logging_directory"

LOG_FILE_NAME = f"logged_{CURRENT_TIMESTAMP}.log"

os.makedirs(LOG_DIR,exist_ok=True)

CORRECT_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
                filename=CORRECT_PATH,
                filemode="w",
                format='[%(asctime)s] %(name)s-%(levelname)s:%(message)s',
                level=logging.INFO
                )

