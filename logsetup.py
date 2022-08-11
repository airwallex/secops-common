import logging
import sys
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    def __init__(self,
                 fmt="%(levelname) %(message)",
                 style='%',
                 *args,
                 **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record['severity'] = log_record['levelname']
        del log_record['levelname']
        return super(StackdriverJsonFormatter,
                     self).process_log_record(log_record)


class _MaxLevelFilter(object):
    def __init__(self, highest_log_level):
        self._highest_log_level = highest_log_level

    def filter(self, log_record):
        return log_record.levelno <= self._highest_log_level


# A handler for low level logs that should be sent to STDOUT
info_handler = logging.StreamHandler(sys.stdout)
formatter = StackdriverJsonFormatter()
info_handler.setFormatter(formatter)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(_MaxLevelFilter(logging.ERROR))

# A handler for high level logs that should be sent to STDERR
error_handler = logging.StreamHandler(sys.stderr)
formatter = StackdriverJsonFormatter()
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(info_handler)
logger.addHandler(error_handler)

# See https://github.com/googleapis/google-api-python-client/issues/299
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def enable_logfile(f):
    rotatingFile = RotatingFileHandler(f,
                                       maxBytes=(1048576 * 5),
                                       backupCount=7)
    logger.addHandler(rotatingFile)
