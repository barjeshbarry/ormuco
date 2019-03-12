# Export the following ENV variable.
export MY_TEST_APP="/var/lib/my_test_app"

# Recommended order to review files
appFrameworkPython/Logger/Logger.py
appFrameworkPython/NetworkUtil/NetworkUtil.py
appFrameworkPython/Application/Application.py
CacheHandler.py
tests/CacheHandlerTest.py
Server.py
Client.py

# All the functions/variables have their description at the place 
# of their defintion. What Client/Server can/not do are mentioned in 
# their respective files.

# You may ignore CMakeLists.txt

# You may look at Server/Client log under LRU dir.

############### Server.py --help ###############################

usage: Server [-h] [--log-file LOG_FILE] [--enable-stdout-log]
              [--log-level {info,debug,critical,warning,error}]
              [--cache-dir CACHE_DIR] [--ip IP] [--port PORT]
              [--max-cache-entries MAX_CACHE_ENTRIES]
              [--cache-tracker-thread-interval-min CACHE_TRACKER_THREAD_INTERVAL_MIN]
              [--cache-file-age-min CACHE_FILE_AGE_MIN]

Program: ./Server.py. This program depicts a server machine which recieves a
request and sees whether the response is available in the cache. if not, it
process the request/response, stores the response in the cache along with
doing book-keeping stuff and finally returns the result back to the server.

optional arguments:
  -h, --help            show this help message and exit
  --log-file LOG_FILE   log-file. If you do not want log to go into a file,
                        specify log-file as an empty string ("") (default:
                        /var/lib/my_test_app/log/Server.log)
  --enable-stdout-log   Print log messages to stdout. (default: False)
  --log-level {info,debug,critical,warning,error}
                        log-level (default: info)
  --cache-dir CACHE_DIR
                        Directory where cache files would be stored. (default:
                        /var/lib/my_test_app/cache)
  --ip IP               IP address of the underlying machine. Leave it blank
                        to use the actual IP address. (default: 127.0.0.1)
  --port PORT           port on which this application is available. (default:
                        9999)
  --max-cache-entries MAX_CACHE_ENTRIES
                        Maximum number of cache entries allowed. (default: 10)
  --cache-tracker-thread-interval-min CACHE_TRACKER_THREAD_INTERVAL_MIN
                        Interval at which to run thread to expire caches older
                        than value specified by --cache-file-age-min.
                        (default: 10)
  --cache-file-age-min CACHE_FILE_AGE_MIN
                        Cache file age in mins. (default: 120)

############### Client.py --help ###############################
usage: Client [-h] [--log-file LOG_FILE] [--enable-stdout-log]
              [--log-level {info,debug,critical,warning,error}]
              [--server-info SERVER_INFO]

Program: ./Client.py. This program depicts a client machine which sends out
request in the form of a string to multiple servers and expects the reverse
string. This code aalso maintain the state of all the requests so that if any
server times-out, then it could send the request again.

optional arguments:
  -h, --help            show this help message and exit
  --log-file LOG_FILE   log-file. If you do not want log to go into a file,
                        specify log-file as an empty string ("") (default:
                        /var/lib/my_test_app/log/Client.log)
  --enable-stdout-log   Print log messages to stdout. (default: False)
  --log-level {info,debug,critical,warning,error}
                        log-level (default: info)
  --server-info SERVER_INFO
                        A comma separated list of server information in the
                        form, <ip1:port1>,<ip2:port2">,....,<ipN:portN>. The
                        port is optional. (default: 127.0.0.1:9999)



