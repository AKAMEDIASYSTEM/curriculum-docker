#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import tornado
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
import datetime
import random

class ApiHandler(BaseHandler):
    """json access to local curriculum store"""

    def get(self):
        if self.isAuth():
            n = self.get_argument('n',3) # three hours, should be global EXPIRE_IN from worker.py
            earliest = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            groupID = self.get_argument('groupID') # these have to be present, isAuth would have failed otherwise
            db = self.settings['db']
            print 'hit the ApiHandler endpoint with n=', n
            keywords = []
            found = 0
            r = db.keywords.find({'latest':{'$gte':earliest},'groupID':groupID},{'keyword':1,'_id':0})
            results = [word['keyword'] for word in r]
            while found < 4:
                k = random.choice(results)
                if k not in keywords:
                    keywords.append(k)
                    found += 1
            d = {'title':'curriculum-insular test',
            'keywords':keywords}
            self.response = ResponseObject('200','Success', d)
        else:
            self.response = ResponseObject('500','Authentication failed')
        self.write_response()
        self.finish()