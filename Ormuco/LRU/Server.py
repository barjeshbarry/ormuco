#!/usr/bin/python
# Server.py
# ================

import sys
import os
import posixpath as path
import threading

# TODO (Barjesh 03/11/19) Use __init__.py to get rid of the following sys.path.insert statements
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/Application')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/Logger')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/NetworkUtil')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/CacheHandler')))

#local imports
from NetworkUtil import NetworkUtil
from Application import Application
from CacheHandler import CacheHandler
import Logger
import socket
import time

class Server(Application):

    # Max buffer size
    _MAX_BUF_LENGTH = 1024

    #
    # Main application thread
    #
    # Returns nothing
    #
    def run_main_thread(self):
        Logger.g_logger.info('Starting {0} thread...'.format(self.__class__.__name__))

        try: 
            # Create a socket
            skt = socket.socket()

            # Bind to a port
            skt.bind((self.m_app_args_dict['ip'], self.m_app_args_dict['port']))
            Logger.g_logger.info("socket binded to %s:%d", self.m_app_args_dict['ip'], self.m_app_args_dict['port'])

            CacheHandler.init(self.m_app_args_dict['cache_dir'], self.m_app_args_dict['max_cache_entries'], 
                                self.m_app_args_dict['cache_tracker_thread_interval_min'],
                                self.m_app_args_dict['cache_file_age_min'])

        except Exception as e:
            Logger.g_logger.critical("Failed to create/bind socket. Error: %s. Exiting!", str(e))
            sys.exit()

        while True:
            conn = None
            try:
                # Put socket into listening mode
                skt.listen(5)
                Logger.g_logger.info("socket is in listening mode.")
                conn, addr = skt.accept()      
                conn.settimeout(60)
                Logger.g_logger.info("Recieved connection from: %s", addr)
                threading.Thread(target = self.request_handler,args = (conn, addr)).start()
        
            except Exception as e:
                Logger.g_logger.error("Error occured while connecting/responding to %s", addr)
                if conn:
                    conn.close()

    #
    # This function process the incoming request and returns the response. To keep the logic simple, this function simply returns the reverse of incoming request string.
    #
    # @param self [in] This pointer
    # @param request [in] request string // Could be a protobuf message
    #
    # Returns reverse of the request string
    #
    def process_request(self, request):
        return request[::-1]

    #
    # This function handles client request
    #
    # @param self [in] This pointer
    # @param conn [in] Connection object
    # @param addr [in] Client Address
    # 
    # Returns nothing
    #
    def request_handler(self, conn, addr):
        try:
            while True:
                request = conn.recv(self._MAX_BUF_LENGTH)
                if request:
                    request_str = str(request.decode('ascii'))
                    print request_str
                    is_cache_exist, response = CacheHandler.fetch_cache_entry(request_str)

                    if not is_cache_exist:
                        response = self.process_request(request_str)
                        CacheHandler.write_cache_entry(request, response)

                    conn.send(response.encode('ascii'))
                else:
                    raise Exception('Client disconnected')
        except Exception as e:
                #Logger.g_logger.error("Status: %s", str(e))
                print "Status: {0}".format(str(e))
        else:
            if conn:
                conn.close()
    
    # Command-line options verification
    def verify_app_args(self):
        if self.m_app_args_dict['max_cache_entries']  < 0:
            Logger.g_logger.error('--max-cache-entries should be greater than or equal to zero.')
            return False

        if self.m_app_args_dict['port']  < 0:
            Logger.g_logger.error('--port can not be less than or equal to 0.')
            return False

        if not self.m_app_args_dict['ip']:
            self.m_app_args_dict['ip'] = NetworkUtil.GetIpAddress()

        if not os.path.exists(self.m_app_args_dict['cache_dir']):
            try:
                os.makedirs(self.m_app_args_dict['cache_dir'])
            except Exception as e:
                Logger.g_logger.critical('Failed to create cache directory structure %s specified by --cache-dir. Error: %s', self.m_app_args_dict['cache_dir'], str(e))
                return False

        return True

    # Command line options 
    def build_app_args(self):

        cacheDir = path.join(os.environ['MY_TEST_APP'], 'cache')
        self.m_parser.add_argument('--cache-dir', default=cacheDir, type=str,
                                help= 'Directory where cache files would be stored.')

        self.m_parser.add_argument('--ip', type=str, default="127.0.0.1",
                                help= 'IP address of the underlying machine. Leave it blank to use the actual IP address.')

        self.m_parser.add_argument('--port', type=int, default=9999,
                                help= 'port on which this application is available.')

        self.m_parser.add_argument('--max-cache-entries', default=10, type=int,
                                help= 'Maximum number of cache entries allowed.')

        self.m_parser.add_argument('--cache-tracker-thread-interval-min', default=10, type=int,
                                help= 'Interval at which to run thread to expire caches older than value specified by --cache-file-age-min.')

        self.m_parser.add_argument('--cache-file-age-min', default=120, type=int,
                                help= 'Cache file age in mins.')

    # constructor
    def __init__(self):
        program_help = """Program: {0}. This program depicts a server machine which recieves a request and sees whether the response is available in the cache. if not, it process the request/response, stores the response in the cache along with doing book-keeping stuff and finally returns the result back to the server.""".format(sys.argv[0])
        super(Server, self).__init__(sys.argv, program_help)

if __name__ == "__main__":
    myServerApp = Server()
    myServerApp.execute_app()
