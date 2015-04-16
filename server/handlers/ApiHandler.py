#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
import datetime
import random


class ApiHandler(BaseHandler):
    '''
    json access to curriculum keywords store
    groupID (required)
    token (required)
    n = number of entries to return (optional)
    t = number of minutes into the past to look (optional)
    type = ['ADJP','ADVP','PP','NP','VP','ANY']

    '''

    def get(self):
        if self.isAuth():
            n = self.get_argument('n', 3)  # default three terms
            ty = self.get_argument('type', 'any')  # default any type of chunk
            t = self.get_argument('t', 60*24*3)  # default to last 3 days
            earliest = datetime.datetime.utcnow() - datetime.timedelta(minutes=int(t))
            groupID = self.get_argument('groupID')  # these have to be present, isAuth would have failed otherwise
            db = self.settings['db']
            print 'hit the ApiHandler endpoint with n, type, and t = ', n, ty, t
            keywords = []
            found = 0
            if ty == 'any':
                r = db.keywords.find({'latest': {'$gte': earliest}, 'groupID': groupID}, {'keyword': 1, '_id': 0})
            else:
                # insecure! we should have an enum or whitelist of types
                r = db.keywords.find({'latest': {'$gte': earliest}, 'groupID': groupID, 'type': ty.upper()}, {'keyword': 1, 'type': 1, '_id': 0})
            results = [word['keyword'] for word in r]
            # TODO check here if results is non-empty
            if len(results):
                # make usre we have enough results to choose from
                if len(results) < int(n):
                    keywords = results
                else:
                    while found < int(n):
                        k = random.choice(results)
                        if k not in keywords:
                            keywords.append(k)
                            found += 1
            else:
                keywords = ['no results to be found']
            d = {'title': 'curriculum-insular test', 'keywords': keywords}
            self.response = ResponseObject('200', 'Success', d)
        else:
            self.response = ResponseObject('500', 'Authentication failed')
        self.write_response()
        self.finish()
