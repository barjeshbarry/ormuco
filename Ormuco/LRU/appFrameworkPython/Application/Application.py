#!/usr/bin/python

import sys
import os
import argparse
import logging
import ConfigParser
import posixpath as path
from abc import ABCMeta, abstractmethod
import signal

my_path = path.join(sys.path[0], "../../Logger")
if my_path not in sys.path:
    sys.path.append( my_path )

from Logger import Logger

#
# This class is a generic class which provides the basic functionality required by all the
# applications. The functionality includes generic command-line options, function to parse the
# command line options, logging command line options etc.
#
class Application(object):

    __metaclass__ = ABCMeta

    #
    # Constructor
    #
    # @self: this pointer
    # @sys_argv: sys_Argv from the calling program.
    # @program_help: Program help description.
    #
    # returns nothing
    #
    def __init__(self,  sys_argv, program_help):

        start_index = sys_argv[0].rfind("/") + 1
        self.m_program_name = sys_argv[0][start_index:][:-3]

        self.m_parser = argparse.ArgumentParser(prog=self.m_program_name,
                                description=program_help,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.m_sys_argv_beg_one = sys_argv[1:]

        self.m_logger = None
        self.m_app_args_dict = None
        self.m_abort = False
        self.build_app_args_0()

        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        # Ignore SIGHUP
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    #
    # This function is the signal handler
    #
    # @self: this pointer
    # @sig_number: signal number
    # @frame: It points to the execution frame that was interrupted by the signal
    #
    # returns nothing
    #
    def signal_handler(self, sig_number, frame):
        message = ''
        sig_name = tuple((v) for v, k in signal.__dict__.iteritems() if k == sig_number)[0]
        if not self.m_abort:
            message = "Caught signal %s(%d), shutting down... (Ctrl+C again to force exit)" % (sig_name, sig_number)
        else:
            message = "Caught signal %s(%d), Force closing..." % (sig_name, sig_number)
        self.m_logger.info(message)
        if self.m_abort:
            sys.exit(message)
        self.m_abort = True

    #
    # This function logs all the command line option for a given program. All program should call
    # this function so that in case of some issue, we could refer to the options being used to run
    # the program.
    #
    # returns nothing
    #
    def log_app_args(self):
        self.m_logger.info("========== Command line options ==========")
        for k,v in self.m_app_args_dict.iteritems():
            s= k + "=" + str(v)
            self.m_logger.info(s)
        self.m_logger.info("======== End Command line options ========")

    #
    # This function builds generic command line options like help, version, log-file etc.
    # All applications should define command line options specific to their functionality in
    # their own files by defining build_app_arg function. Please note that build_app_arg is defined
    # as an abstract method to force the derived class to introduce its own command-line options
    # in build_app_args function.
    #
    # returns nothing
    #
    def build_app_args_0(self):

        log_dir = path.join(os.environ['MY_TEST_APP'], 'log')
        try:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
        except Exception as e:
            print "Failed to create log directory {0}".format(log_dir)
            sys.exit()

         # Logging
        log_file = path.join(log_dir, self.m_program_name + '.log')

        self.m_parser.add_argument('--log-file',
                                    help='log-file. If you do not want log to go into a file, '
                                         'specify log-file as an empty string ("")',
                                    type=str,
                                    default= log_file)

        self.m_parser.add_argument('--enable-stdout-log',
                                    help='Print log messages to stdout.',
                                    action="store_true",
                                    default= False)

        self.m_parser.add_argument('--log-level',
                                  help='log-level',
                                  type=str,
                                  choices=[k for k in Logger.log_level_dict],
                                  default= 'info')
    #
    # This function is expected to be implemented by the derived class to introduce its own
    # command-line options. It's highly unlikely that the derived class does not need to add any
    # command-line option so that's why this fnction is made abstract.
    #
    # returns nothing
    #
    @abstractmethod
    def build_app_args(self):
        pass

    #
    # This function is expected to be implemented by the derived class to verify its own
    # command-line options.
    #
    # returns nothing
    #
    @abstractmethod
    def verify_app_args(self):
        pass

    #
    # This function is expected to be implemented by the derived class to start the real work.
    # In most of the cases, this fuction would have an infinite loop to do some work at some
    # regular interval.
    #
    # returns nothing
    #
    @abstractmethod
    def run_main_thread(self):
        pass

    def execute_app(self):

        # Build parameters local to the application. Refer AppFrameworkSampleProgram.py
        self.build_app_args()

        # Build.m_app_arg_dict and also initiliaze the Logger i.e..m_logger
        self.configure_app()

        # Verify command line parameters
        if not self.verify_app_args():
            self.m_logger.critical("Argument verification fail. Aborting...")
            sys.exit(0)

        # Log all the command line parameters
        self.log_app_args()

        # The real deal.
        self.run_main_thread()

    #
    # This function parse all the command line parameters and also initialize the logger. In a
    # typical use case, this function should be enough to satisfy the requirement of all the apps
    # as far as configuration is concerned. If an app has some specific requirement not fullfilled
    # by this function, that app needs to define its own configure_app function.
    #
    # returns nothing
    #
    def configure_app(self):
        self.m_app_args_dict = vars(self.m_parser.parse_args(self.m_sys_argv_beg_one))
        self.m_logger = Logger.get_logger(self.m_program_name, self.m_app_args_dict['log_level'],
                                          self.m_app_args_dict['log_file'],
                                          self.m_app_args_dict['enable_stdout_log'])

