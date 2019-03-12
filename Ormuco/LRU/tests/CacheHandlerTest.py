#!/usr/bin/python

import unittest
import logging
import sys
import os
import posixpath as path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(-1, os.path.abspath(os.path.join(os.path.dirname(__file__), '../appFrameworkPython/Logger')))

from CacheHandler import CacheHandler

class CacheHandlerUnitTest(unittest.TestCase):
    _CACHE_DIR = "/tmp"
    _MAX_CACHE_ENTRIES = 2
    def setUp(self):
        CacheHandler.init(cache_dir = self._CACHE_DIR, max_cache_entries = self._MAX_CACHE_ENTRIES,
            cache_tracker_thread_interval_min = None, cache_file_age_min = None, run_thread = False)

    def write_and_fetch_basic_test(self):
        self.assertEqual(len(CacheHandler.m_cache_dict), 0)
        request = "abc"
        response = "def"
        ret_value = CacheHandler.write_cache_entry(request, response)
        self.assertEqual(ret_value, True)

        ret_value, actual_response = CacheHandler.fetch_cache_entry(request)
        self.assertEqual(ret_value, True)
        self.assertEqual(response, actual_response)

    def write_and_fetch_cache_full_test(self):
        # Fetch count 1
        CacheHandler.m_cache_dict.clear()
        self.assertEqual(len(CacheHandler.m_cache_dict), 0)
        request1 = "abc"
        response1 = "def"
        ret_value = CacheHandler.write_cache_entry(request1, response1)
        self.assertEqual(ret_value, True)
        ret_value, actual_response = CacheHandler.fetch_cache_entry(request1)
        self.assertEqual(ret_value, True)
        self.assertEqual(response1, actual_response)

        # Fetch count 2
        request2 = "mno"
        response2 = "pqr"
        ret_value = CacheHandler.write_cache_entry(request2, response2)
        self.assertEqual(ret_value, True)
        ret_value, actual_response = CacheHandler.fetch_cache_entry(request2)
        self.assertEqual(ret_value, True)
        self.assertEqual(response2, actual_response)
        ret_value, actual_response = CacheHandler.fetch_cache_entry(request2)
        self.assertEqual(ret_value, True)
        self.assertEqual(response2, actual_response)

        key1 = CacheHandler.get_key(request1)
        sub_dict = CacheHandler.m_cache_dict[key1]
        self.assertEqual(sub_dict['COUNT'], 1)
        
        key2 = CacheHandler.get_key(request2)
        sub_dict = CacheHandler.m_cache_dict[key2]
        self.assertEqual(sub_dict['COUNT'], 2)
        self.assertEqual(CacheHandler.is_cache_full(), True)

        # Now the Cache is full ( = 2), insert a new entry. It shoule through key corresponding to
        # the request1 out of cache.
        request3 = "jkl"
        response3 = "xyz"
        ret_value = CacheHandler.write_cache_entry(request3, response3)
        key3 = CacheHandler.get_key(request3)
        sub_dict = CacheHandler.m_cache_dict[key3]
        self.assertEqual(sub_dict['COUNT'], 0)
        self.assertEqual(CacheHandler.is_cache_full(), True)
        self.assertEqual(CacheHandler.is_cache_exist(key1), False)
        

def cache_hander_unit_test_suite():
    ts = unittest.TestSuite()
    ts.addTest(CacheHandlerUnitTest('write_and_fetch_basic_test'))
    ts.addTest(CacheHandlerUnitTest('write_and_fetch_cache_full_test'))
    return ts

runner = unittest.TextTestRunner()
cache_handler_unit_test_suite_ts = cache_hander_unit_test_suite()
runner.run(cache_handler_unit_test_suite_ts)




