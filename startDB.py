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
from pymongo import MongoClient
import groups

TTL_text = 604800  # 7 days
TTL_url = 600  # ten minutes


def create_keywords_collection(db):
    db.create_collection('keywords')
    db.keywords.ensure_index('latest', expireAfterSeconds=TTL_text)
    db.keywords.ensure_index('keyword')
    db.keywords.ensure_index('type')
    logging.info('Created TTL-enabled collection "keywords" in database "curriculum"')


def create_users_collection(db):
    db.create_collection('users')
    db.users.ensure_index('groupID')
    logging.info('Created UNcapped collection "users" in database "curriculum"')
    db.users.insert(groups.grouplist)  # bulk insert FTW
    logging.info('Added all groups.py to db.users DB')


def create_pages_collection(db):
    db.create_collection('pages')
    db.pages.ensure_index('timestamp', expireAfterSeconds=TTL_url)
    db.pages.ensure_index('url')
    logging.info('Created TTL-enabled collection "pages" in database "curriculum"')


if __name__ == '__main__':
    client = MongoClient(tz_aware=True)
    curr_db = client.curriculum
    try:
        create_keywords_collection(curr_db)
    except pymongo.errors.CollectionInvalid:
        pass
    try:
        create_pages_collection(curr_db)
    except pymongo.errors.CollectionInvalid:
        pass
    try:
        create_users_collection(curr_db)
    except pymongo.errors.CollectionInvalid:
        pass
    logging.info("Finished setting up Mongo DBs")
