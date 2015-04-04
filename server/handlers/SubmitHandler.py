#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import tornado
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
import beanstalkc

class SubmitHandler(BaseHandler):
    """json submittion to local curriculum store"""
    beanstalk = beanstalkc.Connection(host='localhost', port=14711)

    def post(self):
        if self.isAuth():
            db = self.settings['db']
            url = self.get_argument('url')
            groupID = self.get_argument('groupID')
            print 'hit the SubmitHandler endpoint with url=', url
            # TODO: this doesn't take groups into account! and so is terribly broken.
            # a quick fix is to move all this over to mongo
            # not sure about wisdom of that
            beanstalk.put(url)
            # maybe have a beanstalk queue for every groupID???
            # is that Smart?
        self.response = ResponseObject('200','Success')
        self.write_response()
        self.finish()