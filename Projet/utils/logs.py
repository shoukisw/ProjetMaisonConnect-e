import logging
from config import LOG_FILE

# Créer un logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Définir le niveau global des logs (INFO, WARNING, ERROR...)

# Handler pour le fichier
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO) 
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Handler pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)


logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)
