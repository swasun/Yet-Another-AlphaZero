 ###############################################################################
 # Copyright (C) 2019 Charly Lamothe                                           #
 #                                                                             #
 # This file is part of YetAnotherAlphaZero.                                   #
 #                                                                             #
 #   Licensed under the Apache License, Version 2.0 (the "License");           #
 #   you may not use this file except in compliance with the License.          #
 #   You may obtain a copy of the License at                                   #
 #                                                                             #
 #   http://www.apache.org/licenses/LICENSE-2.0                                #
 #                                                                             #
 #   Unless required by applicable law or agreed to in writing, software       #
 #   distributed under the License is distributed on an "AS IS" BASIS,         #
 #   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
 #   See the License for the specific language governing permissions and       #
 #   limitations under the License.                                            #
 ###############################################################################

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
