#!/usr/bin/env python
# curriculum - semantic browsing for groups
# (c)nytlabs 2014

import tornado
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import ResponseObject
import traceback
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
        # logging.info('entering isAuth function in BaseHandler')
        db = self.settings['db']
        isAuth = db.users.find({'$and': [
            {'groupID': self.groupID},
            {'token': self.token}
            ]}).count()
        logging.info('found %s matches for isAuth' % isAuth)
        return isAuth
