import logging
from logging.handlers import RotatingFileHandler
import os
import errno


class LoggerFactory(object):
    
    @staticmethod
    def create(path, module_name):
        # Create logger
        logger = logging.getLogger(module_name)
        logger.setLevel(logging.DEBUG)

        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Create file handler
        fh = RotatingFileHandler(path + os.sep + module_name + '.log', maxBytes=1000000, backupCount=5)
        fh.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s')

        # Add formatter to handler
        fh.setFormatter(formatter)

        # Add fh to logger
        logger.addHandler(fh)

        return logger
