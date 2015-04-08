#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import tornado.ioloop
import tornado.web
from handlers.BrowserHandler import BrowserHandler
from handlers.ApiHandler import ApiHandler
from handlers.SubmitHandler import SubmitHandler
import redis



db = redis.StrictRedis(host='localhost', port=6379, db=1)
auth = redis.StrictRedis(host='localhost', port=6379, db=2)
# settings = {'debug':True}
# settings = {'debug':True, 'auth':auth} # not sure this will work, strike this first if stuff doesn't work
settings = {'debug':True, 'auth':True}
# TODO: here populate the auth db with the credentials from keys.py or groups.py
# also consider an api-based way to add groups (poss involving master key), this might be rly easy to scale?
# no master keys w/o someone doing a security audit, maybe

application = tornado.web.Application([
    (r"/api", ApiHandler),
    (r"/submit", SubmitHandler),
    (r"/", BrowserHandler),
], db=db, **settings)

if __name__ == "__main__":
    application.listen(80)
    print 'starting server'
    tornado.ioloop.IOLoop.instance().start()