#!/usr/bin/env python
# curriculum-docker


import logging
import datetime
import tornado
import random
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject


class BrowserHandler(BaseHandler):
    '''
    HTML display of Keywords browsed in the last day
    groupID (required)
    token (required)
    n = number of entries to return (optional)
    t = number of minutes into the past to look (optional)
    type = ['ADJP','ADVP','PP','NP','VP','ANY']


    '''
    # def __init__(self, *args, **kwargs):
    #     BaseHandler.__init__(self,  *args, **kwargs)

    def get(self):
        logging.debug('hit the BrowserHandler endpoint')
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
            loader = tornado.template.Loader('templates')
            self.write(loader.load('zen.html').generate(keywords=keywords))
        else:
            self.response = ResponseObject('500', 'Error - authentication failed')
        self.finish()
