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

import logging
import pymongo
import groups

TTL_text = 604800  # 7 days
TTL_url = 600  # ten minutes


def startDB(db):
    logging.info('in startDB now')
    create_keywords_collection(db)
    create_pages_collection(db)
    create_users_collection(db)
    logging.info("Finished setting up Mongo DBs")


def create_keywords_collection(db):
    try:
        # db.create_collection('keywords')
        db.keywords.create_index('latest', expireAfterSeconds=TTL_text)
        db.keywords.create_index('keyword')
        db.keywords.create_index('type')
        logging.info('Created TTL-enabled collection "keywords" in database "curriculum"')
    except pymongo.errors.CollectionInvalid:
        # oh! this error is what you get when the collection already exists
        logging.info('keywords collection already existed')
        pass


def create_users_collection(db):
    try:
        # db.create_collection('users')
        db.users.create_index('groupID')
        db.users.insert(groups.grouplist)  # bulk insert FTW
        logging.info('Added all groups.py to db.users DB')
    except pymongo.errors.CollectionInvalid:
        logging.info('users collection already existed')
        pass


def create_pages_collection(db):
    try:
        # db.create_collection('pages')
        db.pages.create_index('timestamp', expireAfterSeconds=TTL_url)
        db.pages.create_index('url')
        logging.info('Created TTL-enabled collection "pages" in database "curriculum"')
    except pymongo.errors.CollectionInvalid:
        logging.info('pages collection already existed')
        pass


if __name__ == '__main__':
    startDB()
