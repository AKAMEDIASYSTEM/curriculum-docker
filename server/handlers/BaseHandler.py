#!/usr/bin/env python
# curriculum - semantic browsing for groups
# (c)nytlabs 2014

import datetime
import json
import tornado
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import ResponseObject
import traceback
import redis
import logging

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        logging.debug('entering init funciton of BaseHandler')
        try:
            tornado.web.RequestHandler.__init__(self,  *args, **kwargs)
            self.set_header("Access-Control-Allow-Origin", "*")
            self.token = self.get_argument('token')
            self.groupID = self.get_argument('groupID')
            self.response = ResponseObject.ResponseObject()
        except Exception as reason:
            print reason, traceback.format_exc()
  
    def write_response(self):
        try:
            self.write(self.response.response)
        except Exception as reason:
            print reason, traceback.format_exc()
            print self.response.response
    
    def isAuth(self):
        logging.info('entering isAuth function in BaseHandler')
        r_auth = redis.StrictRedis(host='localhost', port=6379, db=2)
        result = r_auth.get(self.groupID)
        logging.debug(result)
        if result is not None and result==self.token:
            return False
        else:
            return True
        print "we shouldn't be here"
        return False
        # db = self.settings['auth'] # TODO change this to redis lookup?
        # isAuth = db.users.find(
        #     {'$and':
        #         [
        #             {'groupID' : self.groupID},
        #             {'token' : self.token}
        #             ]
        #     }).count()
        # logging.info('found %s matches for isAuth'%isAuth)
        # return isAuth