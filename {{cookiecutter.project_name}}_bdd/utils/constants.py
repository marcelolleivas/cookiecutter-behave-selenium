from os import getcwd
from os.path import join

PATH = getcwd()
LOG_FILE_DIR = join(PATH, "log")
LOGGER_CONFIG = join(PATH, "utils", "logging.json")