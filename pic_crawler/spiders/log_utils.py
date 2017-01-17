#: ------------------------------------------------
#: FileName:   log_utils.py
#: Author:  DORSEy Q F TANG
#: Date:    15 Jan 2017
#: Description: a utility class which is used to log down the
#: desired info during the procedure for tracing in case of errors detected
#: ------------------------------------------------

import logging

#: the class used to log down the required info
class LogUtils():
    name = "log_utils"
    #: the logger pattern
    log_pattern = "%(asctime)s [%(name)s] [%(filename)s:%(lineno)d] [%(levelname)s] [%(message)s]"

    #: default log file name
    default_log_file_name = "pic_crawler.log"

    def get_log(self, log_name, log_file_name = None):
        logger = logging.getLogger(log_name)
        log_formatter = logging.Formatter(self.log_pattern)

        #: if no log file name specified, default is taken in usage
        if log_file_name:
            log_handler = logging.FileHandler(log_file_name)
        else:
            log_handler = logging.FileHandler(self.default_log_file_name)

        log_handler.setFormatter(log_formatter)
        logger.addHandler(log_handler)

        return logger