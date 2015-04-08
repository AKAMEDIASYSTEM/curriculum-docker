#!/usr/bin/env python
# curriculum-insular
'''
StartDB is in charge of reading a static 'groups.py' file that is NOT in the repo
groups.py has the following structure

grouplist = [
    {'groupID':'foofoofoo', 'token':'SECRET_DIFFERENT_KEY'},
    {'groupID':'foofoofoo1', 'token':'SECRET_DIFFERENT_KEY1'},
    {'groupID':'foofoofoo2', 'token':'SECRET_DIFFERENT_KEY2'},
    {'groupID':'foofoofoo3', 'token':'SECRET_DIFFERENT_KEY3'}
]

'''

import datetime
import logging
import os
import sys
import time
import tornado
from tornado import gen
import tornado.ioloop
import tornado.web
import tornado.options
import groups
import redis

if __name__ == '__main__':
    r_auth = redis.StrictRedis(host='localhost', port=6379, db=2)
    for group in groups.grouplist:
        pipe_text = r_auth.pipeline(transaction=True)
        r_response = pipe_text.set(group['groupID'], group['token']).execute()
        print r_response
    logging.info("Finished setting up Redis DBs")