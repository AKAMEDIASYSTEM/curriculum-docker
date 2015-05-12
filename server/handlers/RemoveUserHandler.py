#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject


class RemoveUserHandler(BaseHandler):
    '''
    Master-account-only endpoint for adding groups to Curriculum

    Should be accompanied by a deletion endpoint
    (do we instantly delete a group's keywords, or just let them expire?)
    (once groupID is deleted, no API calls for a deleted group will succeed)

    '''

    def get(self):
        print 'hit the removeUser handler'
        db = self.settings['db']
        master_group = self.get_argument('groupID')
        master_token = self.get_argument('token')
        new_groupID = self.get_argument('new_groupID')
        new_token = self.get_argument('new_token')
        # ruff check for obv prob
        if new_groupID is master_group:
            self.response = ResponseObject('500', 'Choose another groupID')
            self.write_response()
            self.finish()
        else:
            dbq = db.users.find({'$and': [
                {'groupID': master_group},
                {'token': master_token},
                {'privileged': True},
                ]}).count()
            if dbq == 1:
                r = db.users.remove_one({'groupID': new_groupID, 'token': new_token}, True)
                print 'db removal result is ', r
                keywords = ['removed %s and %s to users DB' % (new_groupID, new_token)]
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
