#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import tornado.ioloop
import tornado.web
from pymongo import MongoClient
from handlers.BrowserHandler import BrowserHandler
from handlers.ApiHandler import ApiHandler
from handlers.SubmitHandler import SubmitHandler
import startDB
import os

# client = MongoClient(tz_aware=True)
mongoAddress = os.getenv("AKAMONGO_PORT_27017_TCP_ADDR")
client = MongoClient(mongoAddress, tz_aware=True)
db = client.curriculum
settings = {'debug': True, "static_path": os.path.join(os.path.dirname(__file__), "static")}
# also consider an api-based way to add groups (poss involving master key), this might be rly easy to scale?
# no master keys w/o someone doing a security audit, maybe

test_q = db.users.find().count()
if test_q < 1:
    print 'starting DB for the first time we think'
    startDB.startDB(db)
    print 'started DB'
else:
    print 'DB seems already to be set up, continuing server launch'

application = tornado.web.Application([
    (r"/api", ApiHandler),
    (r"/submit", SubmitHandler),
    (r"/", BrowserHandler),
], db=db, **settings)

if __name__ == "__main__":
    application.listen(80)
    print 'starting server'
    tornado.ioloop.IOLoop.instance().start()
