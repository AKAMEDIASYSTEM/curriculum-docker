#!/usr/bin/env python
# curriculum-insular


import logging
import datetime
import tornado
import random
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
from tornado.template import Template
from tornado.template import Loader

class BrowserHandler(BaseHandler):
    """HTML display of Keywords browsed in the last day"""
    def __init__(self, *args, **kwargs):
        BaseHandler.__init__(self,  *args, **kwargs)  

    def get(self):
        logging.debug('hit the BrowserHandler endpoint')
        if self.isAuth():
            logging.debug('inside isAuth conditional in BrowserHandler')
            self.set_header("Content-Type", "text/html")
            earliest = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            logging.debug('earliest is %s' % earliest)
            db = self.settings['db']
            groupID = self.get_argument('groupID')
            logging.debug('groupID is %s' % groupID)
            r = db.keywords.find({'latest':{'$gte':earliest},'groupID':groupID},{'keyword':1,'_id':0})
            d = [word['keyword'] for word in r]
            loader = tornado.template.Loader('../templates')
            
            keywords = []
            found = 0
            while found < 4:
                k = random.choice(d)
                if k not in keywords:
                    keywords.append(k)
                    found += 1

            self.write(loader.load("keyword-single.html").generate(keywords=keywords))
        else:
            # _groupID = self.get_argument('groupID')
            # _token = self.get_argument('token')
            self.response = ResponseObject('500','Error - authentication failed')
        
        self.finish()