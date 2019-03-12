#!/usr/bin/python

import time
import json
import sys
import os
import argparse
import posixpath as path

my_path = path.join(sys.path[0], os.environ['PI_APP_FRAMEWORK_PATH'] + "/Application")
if my_path not in sys.path:
    sys.path.append( my_path )

from Application import Application

my_path = path.join(sys.path[0], os.environ['PI_APP_FRAMEWORK_PATH'] + "/Logger")
if my_path not in sys.path:
    sys.path.append( my_path )

import Logger

#
# Sample program
#
class AppFrameworkSampleProgram(Application):

    #
    # This function defines the real app's work.
    #
    # returns nothing
    #
    def run_main_thread(self):
        Logger.g_logger.info("My sample program is about to start...!!!")
        number_of_runs = self.m_app_args_dict['number_of_runs']

        i = 0
        while True:
            Logger.g_logger.info("Wow, my sample program is actually running...")
            i = i + 1
            if number_of_runs and i == number_of_runs:
                Logger.g_logger.info("Coming out of infinite loop")
                break
            time.sleep(self.m_app_args_dict['run_interval_seconds'])

    #
    # This function validate command line options defined explicitely by the
    # AppFrameworkSampleProgram.py. If you want to add a generic option,
    # please add it to the Application class.
    #
    # returns true if all command line parameters are good, false otherwise.
    #
    def verify_app_args(self):

        if (self.m_app_args_dict['number_of_runs'] < 0):
            Logger.g_logger.critical("The --number_of_runs option is %d but it should be >= 0." %
                                    self.m_app_args_dict['number_of_runs']);
            return False

        if (self.m_app_args_dict['run_interval_seconds'] < 0):
            Logger.g_logger.critical("The --number_of_runs option is %d but it should be >= 0." %
                                    self.m_app_args_dict['run_interval_seconds']);
            return False

        # Everything is good.
        return True

    #
    # Add ONLY AppFrameworkSampleProgram specific command line options here.
    #
    # returns nothing.
    #
    def build_app_args(self):
        self.m_parser.add_argument('--run-interval-seconds',
                                       default=10,
                                       type=int,
                                       metavar='Int[0, infinity]',
                                       help='This parameter specify how often to run the program. '
                                            'The default is 10 secconds. In testing '
                                            'environment, you may want to set it to zero along '
                                            'with a postive --number-of-runs.')

        self.m_parser.add_argument('--number-of-runs',
                                       default=0,
                                       type=int,
                                       metavar='Int[0, infinity]',
                                       help='This parameter specify how many times to run the program. '
                                            'The default value zero means run forever. In testing '
                                            'environment, you may want to set it to > 0 along with '
                                            'smaller --run-interval-seconds.')

    #
    # AppFrameworkSampleProgram's Constructor
    #
    # returns nothing.
    #
    def __init__(self):

        program_help = "This program is developed as a sample to see how a typical python program would look like using the framework."
        super(AppFrameworkSampleProgram, self).__init__(sys.argv, program_help)

if __name__ == "__main__":

    myProgram = AppFrameworkSampleProgram()
    myProgram.execute_app()


