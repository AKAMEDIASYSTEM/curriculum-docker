#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
import datetime
import random


class AddUserHandler(BaseHandler):
    '''
    Master-account-only endpoint for adding groups to Curriculum

    Should be accompanied by a deletion endpoint
    (do we instantly delete a group's keywords, or just let them expire?)
    (once groupID is deleted, no API calls for a deleted group will succeed)

    '''

    def get(self):
        master_group = self.get_argument('groupID')
        master_token = self.get_argument('token')
        new_groupID = self.get_argument('new_groupID')
        new_token = self.get_argument('new_token')
        db = self.settings['db']
        dbq = db.users.find({'$and': [
            {'groupID': master_group},
            {'token': master_token}
            ]}).count()
        if dbq == 1:
            r = db.users.update({'groupID': new_groupID, 'token': new_token})
            print 'db insertion result is ', r
            keywords = ['added %s and %s to users DB' % (new_groupID, new_token)]
            d = {'title': 'curriculum-docker', 'keywords': keywords}
            self.response = ResponseObject('200', 'Success', d)
        else:
            keywords = ['master authorization credentials were rejected']
            self.response = ResponseObject('500', 'Master Authentication failed', dbq)
        # check token against submitted token
        # if pass, add two other vars to users DB
        # return message confirming addition if successful
        self.write_response()
        self.finish()
