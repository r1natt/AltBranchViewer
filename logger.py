import logging


STREAM_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

LOGFORMAT = "[%(levelname)s] %(asctime)s %(filename)s:%(funcName)s() (line:%(lineno)s) - %(message)s"
logger_formatter = logging.Formatter(LOGFORMAT)

streamh = logging.StreamHandler()
streamh.setLevel(STREAM_LOG_LEVEL)
streamh.setFormatter(logger_formatter)

fileh = logging.FileHandler("./logs/general.log")
fileh.setLevel(FILE_LOG_LEVEL)
fileh.setFormatter(logger_formatter)

logger = logging.getLogger("general")
logger.setLevel(logging.DEBUG)
logger.addHandler(fileh)
logger.addHandler(streamh)