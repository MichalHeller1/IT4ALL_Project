import logging

logging_format = "%(asctime)s LEVEL: %(levelname)s MSG: %(message)s"
logging.basicConfig(format=logging_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)
