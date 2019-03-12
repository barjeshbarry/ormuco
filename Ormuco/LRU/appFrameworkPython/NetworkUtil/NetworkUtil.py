#!usr/bin/python
import socket
import os
import fcntl
import struct

#
# This class provide networking related utility functions.
#
class NetworkUtil(object):
    #
    # Get the IP address of an interface
    #
    @staticmethod
    def GetIpAddress(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    #
    # Get the IP address of the first non-"lo" interface
    #
    @staticmethod
    def GetIpAddress():
        interface = NetworkUtil.GetNetInterface()
        if interface:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915, # SIOCGIFADDR
                struct.pack('256s', interface[:15])
            )[20:24])
        else:
            return None

    #
    # Returns a non-"lo" network interface in the system(in /sys/class/net/).
    #
    @staticmethod
    def GetNetInterface():
        interfaces = [x for x in sorted(os.listdir('/sys/class/net')) if x != 'lo']
        if interfaces:
            return interfaces[0]
        else:
            return None

