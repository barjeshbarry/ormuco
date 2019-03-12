#!usr/bin/python

import logging
import time

g_logger = None

#
# This class returns the logger of type logging. Ideally this class should also take care of
# setting command line option related to logging but at this time I don't know how to do it.
# TODO Barjesh (March 27, 2018) Move logging level command line options to this class
#
class Logger:

    log_level_dict = {'critical': logging.CRITICAL, 'error': logging.ERROR,
                      'warning': logging.WARNING, 'info': logging.INFO,
                      'debug': logging.DEBUG}

    #
    # This function builds a logger of type logging.
    #
    # @logger_name logger name is (generally) the name of the program.
    # @log_level log_level is one of the keys in log_level_dict.
    # @log_file log_file is the log file. If log_file is empty, the output will be sent to the
    #           console.
    #
    # returns Logger
    #
    @staticmethod
    def get_logger(logger_name, log_level, log_file, enable_stdout_log):

        # We want all log timestamps in UTC
        logging.Formatter.converter = time.gmtime

        logger = logging.getLogger(logger_name)

        # log-level
        logger.setLevel(Logger.log_level_dict[log_level])

        handler = None
        formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)s: %(message)s [%(filename)s:%(lineno)d]',
                                      datefmt='%Y-%b-%d %H:%M:%S')

        if log_file:
            handler = logging.FileHandler(log_file)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        if enable_stdout_log:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        else:
            print "!!!stdout output is off. Please review the log file or use the --enable-stdout-log option."

        global g_logger
        g_logger = logger
        return logger


