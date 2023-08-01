import logging


# Custom filter to exclude log messages containing specific substrings
class ExcludeSpecificMessagesFilter(logging.Filter):
    def __init__(self, excluded_substrings):
        self.excluded_substrings = excluded_substrings

    def filter(self, record):
        message = record.getMessage()
        return not any(substr in message for substr in self.excluded_substrings)


# Set the excluded substrings
excluded_substrings = ["STREAM", "b'sBIT'", "(unknown)"]

# Set up the logger
logging_format = "%(asctime)s LEVEL: %(levelname)s MSG: %(message)s"
logging.basicConfig(format=logging_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the custom filter to the logger
logger.addFilter(ExcludeSpecificMessagesFilter(excluded_substrings))
