#!/usr/bin/python
# Client.py
# ================

import sys
import os
import random
import asyncore
import posixpath as path
import socket

# TODO (Barjesh 03/11/19) Use __init__.py to get rid of the following sys.path.insert statements
# TODO (Barjesh 03/11/19) This program don't send request to multiple server. I looked at asyncore library
# to implement the functionality but becuase of lack of time, I could not do that. 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/Application')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/Logger')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/NetworkUtil')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/CacheHandler')))

#local imports
from NetworkUtil import NetworkUtil
from Application import Application
from CacheHandler import CacheHandler
import Logger

class Client(Application):
    
    # Max buffer length
    _MAX_BUF_LENGTH = 1024

    # Dictionary to store Server information
    m_server_info_dict = {}

    #
    # Main application thread
    #
    # Returns nothing
    #
    def run_main_thread(self):
        Logger.g_logger.info('Starting {0} thread...'.format(self.__class__.__name__))

        skt = None
        while True:
            try: 
                request = raw_input("Enter a string: ")
                skt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                Logger.g_logger.info("Request: %s", request) 
                dt = list(self.m_server_info_dict)[0]
                ip = dt
                sub_dict = self.m_server_info_dict[ip]
                skt.connect((ip, int(sub_dict['PORT'])))
                skt.send(request.encode('ascii'))
                response = skt.recv(self._MAX_BUF_LENGTH)
                print "Response: {0}".format(str(response.decode('ascii')))
                Logger.g_logger.info("Response: %s", str(response.decode('ascii')))
                skt.close()
            except Exception as e:
                Logger.g_logger.error("Error while connecting to the server. Error: %s", str(e))
            else:
                if skt:
                    skt.close()

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
                    is_cache_exist, response = CacheHandler.fetch_cache_entry(request)

                    if not is_cache_exist:
                        response = self.process_request(request)
                        CacheHandler.write_cache_entry(request, response)

                    conn.send(response)
                else:
                    Logger.g_logger.error("Client no longer connected. Client Addr: %s", addr)
        except Exception as e:
                Logger.g_logger.error("Failed to proess request from the client: %s. Error: ", addr, str(e))
        else:
            if conn:
                conn.close()
    
    # 
    # this function returns the number of hops between the underlying machine and the machine
    # specified using ip. 
    #
    # @param ip [in] Destination IP address
    #
    # Returns number of hops between the underlying machine and the machine specified using ip
    #
    def get_hops(self, ip):
        # In real world, use ip to determine the number of hops between client/server.
        return random.randint(1,11)

    # Command-line options verification
    def verify_app_args(self):
        if not self.m_app_args_dict['server_info']:
            Logger.g_logger.error('--server-info can not be empty.')
            return False

        server_info = self.m_app_args_dict['server_info'].split(",")
        for si in server_info:
            ip,port = si.split(':')
            sub_dict = {}
            sub_dict['PORT'] = port
            sub_dict['HOPS'] = self.get_hops(ip)
            self.m_server_info_dict[ip] = sub_dict

        return True

    # Command line options 
    def build_app_args(self):

        self.m_parser.add_argument('--server-info', default='127.0.0.1:9999', type=str,
                                help= 'A comma separated list of server information in the form, <ip1:port1>,<ip2:port2">,....,<ipN:portN>. The port is optional.')

    # constructor
    def __init__(self):
        program_help = """Program: {0}. This program depicts a client machine which sends out request in the form of a string to multiple servers and expects the reverse string. This code aalso maintain the state of all the requests so that if any server times-out, then it could send the request again.""".format(sys.argv[0])
        super(Client, self).__init__(sys.argv, program_help)

if __name__ == "__main__":
    myClientApp = Client()
    myClientApp.execute_app()
