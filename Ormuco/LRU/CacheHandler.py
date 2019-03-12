#!usr/bin/python
import hashlib
import sys
import os
import time

sys.path.insert(-1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'appFrameworkPython/Logger')))

import Logger
import threading

#TODO (Barjesh 03/11/19) Logger not working in this file. 
#TODO (Barjesh 03/11/19) Synchroniztion is not available yet.

#
# This class handles the caching stuff
#
class CacheHandler:

    # Points to the directory where cache files are stored.
    m_cache_dir = None

    # Max number of cache entries allowed
    _MAX_CACHE_ENTRIES = None
    
    # Dictionary to store count of cache accesses
    m_cache_dict = {}
    
    #
    # This function initialize (static) class member variables m_cache_dir and m_cache_dict
    @staticmethod
    def init(cache_dir, max_cache_entries, cache_tracker_thread_interval_min, cache_file_age_min, run_thread = True):
        
        if not CacheHandler.m_cache_dir:
            CacheHandler.m_cache_dir = cache_dir
            CacheHandler._MAX_CACHE_ENTRIES = max_cache_entries
        if run_thread:
            threading.Thread(target = CacheHandler.cache_tracker,args = (cache_tracker_thread_interval_min, cache_file_age_min)).start()

    #
    # This function wakes up every cache_tracker_thread_interval_min and delete all cache entries
    # older than cache_file_age_min
    #
    # @param cache_tracker_thread_interval_min [in] Thread sleep interval
    # @param cache_file_age_min [in] Cache file age
    #
    # Returns nothing
    #
    @staticmethod
    def cache_tracker(cache_tracker_thread_interval_min, cache_file_age_min):
        while True:
            current_time =  int(time.time())
            temp_list = []
            for k,v in CacheHandler.m_cache_dict.iteritems():
                if (current_time - v['UPDATE_TIME_SEC']) >= (cache_file_age_min * 60):
                    temp_list.append(k)
            for k in temp_list:
                CacheHandler.delete_cache_entry(k)
                print "Deleted key {0} from cache.".format(k)
            time.sleep(cache_tracker_thread_interval_min * 60)
    #
    # This function checks whether cache has an entry for the key. It checks for key in the 
    # internal data structure and also the corresponding file on disc. If key exist in the data
    # structure but not on disc (and vice-versa), it does the clean-up to keep things in sync.
    #
    # @param key [in] Cache key corresponding to the request
    #
    # Returns true if the key exists in the internal dictionary and on disc, false otherwise.
    #
    @staticmethod
    def is_cache_exist(key):
        file_path = os.path.join(CacheHandler.m_cache_dir, key)
        if key in CacheHandler.m_cache_dict and os.path.isfile(file_path):
            return True

        if key in CacheHandler.m_cache_dict:
            del CacheHandler.m_cache_dict[key]

        if os.path.isfile(file_path):
            os.remove(file_path)

        return False
        
    
    #
    # This function checks whether the cache is full or not
    #
    # Returns true id cache is full, false otherwise
    #
    @staticmethod
    def is_cache_full():
        return (len(CacheHandler.m_cache_dict) == CacheHandler._MAX_CACHE_ENTRIES)
    
    # 
    # This function returns the MD5 hash for incoming request
    #
    # @param request [in] Request string
    #
    # Returns MD5 hash for the incoming request.
    #
    @staticmethod
    def get_key(request):
        hash_object = hashlib.md5(request)
        return hash_object.hexdigest()

    #
    # This function writes the cache entry on disc.
    #
    # @param key [in] MD5 hash of the request
    # @param response [in] Response needs to be cached
    #
    # Returns true on success, false otherwise.
    #
    @staticmethod
    def write_cache_file(key, response):
        file_handler = None
        ret_value = True
        try:
            file_path = os.path.join(CacheHandler.m_cache_dir, key)
            file_handler = open(file_path, "w+")
            if file_handler:
                 file_handler.write(response)
            #Logger.g_logger.info("Successfully wrote cache entry to %s", file_path)
            print "Successfully wrote cache entry to {0}".format(file_path)
        except Exception as e: 
            #Logger.g_logger.error("Error while writing cache. Error: %s", str(e));
            print "Error while writing cache. Error: {0}".format(str(e))
            ret_value = False
        else:
            if file_handler:
                file_handler.close()
        return ret_value
    
    #
    # This function delete cache key from the m_cache_dict and also the corresponding cache file
    # from the disc.
    #
    # @param key [in] MD5 hash of Request
    #
    # Returns true on success, false otherwise
    #
    @staticmethod
    def delete_cache_entry(key):
        file_path = os.path.join(CacheHandler.m_cache_dir, key)
        try:
            del CacheHandler.m_cache_dict[key]
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except:
            #Logger.g_logger.error("Error while deleting a cache entry. Error: %s", str(e))
            print "Error while deleting a cache entry. Error: {0}".format(str(e))

        return False
    
    #
    # This function write cache file on disc and also update m_cache_dict. if the m_cache_dict is
    # full, it deletes the LRU entry from it.
    # 
    # @param request [in] Request string
    # @param request [in] Response string
    #
    # Returns true on success, false otherwise
    #
    @staticmethod
    def write_cache_entry(request, response):

        key = CacheHandler.get_key(request)

        sub_dict = {}
        sub_dict['COUNT'] = 0
        sub_dict['UPDATE_TIME_SEC'] = int(time.time())
        if not CacheHandler.is_cache_full() and not CacheHandler.is_cache_exist(key):
            CacheHandler.m_cache_dict[key] = sub_dict
            return CacheHandler.write_cache_file(key, response)
        elif CacheHandler.is_cache_full() and not CacheHandler.is_cache_exist(key):
            sorted((value,key) for (key,value) in CacheHandler.m_cache_dict.items())
            key_to_be_deleted = list(CacheHandler.m_cache_dict)[-1]
            CacheHandler.delete_cache_entry(key_to_be_deleted)
            CacheHandler.m_cache_dict[key] = sub_dict
            return CacheHandler.write_cache_file(key, response)
        else:
            #Logger.g_logger.error("Some invalid condition to write cache")
            print "Some invalid condition to write cache"
        return False

    #
    # This function fetches cache for the incoming request.
    # 
    # @param request [in] Request string
    #
    # Returns (True, response) on success, (False, "") otherwise.
    #
    @staticmethod
    def fetch_cache_entry(request):
        key = CacheHandler.get_key(request)
        response = ""
        ret_value = False
        if CacheHandler.is_cache_exist(key):    
            try:
                file_path = os.path.join(CacheHandler.m_cache_dir, key)
                file_handler = open(file_path, "r")
                for line in file_handler:
                    response += line
                sub_dict = CacheHandler.m_cache_dict[key]
                sub_dict['COUNT'] += 1
                sub_dict['UPDATE_TIME_SEC'] = int(time.time())
                ret_value = True
                #Logger.g_logger.debug("Found cache for the request %s", request)
                print "Found cache for the request" 
            except Exception as e:
                #Logger.g_logger.error("Error while fetching cache. Error: %s", str(e));
                print "Error while fetching cache. Error: {0}".format(str(e))
            else:
                if file_handler:
                    file_handler.close()
        else:
            #Logger.g_logger.debug("Cache does not exist for the request %s", request)
            print "Cache does not exist"
        return ret_value, response
                
            



