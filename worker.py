#!/usr/bin/env python

# AKA resonator local curriculum resolver/worker

import beanstalkc
from pattern.web import URL, plaintext, URLError, MIMETYPE_WEBPAGE, MIMETYPE_PLAINTEXT, HTTPError
from pattern.en import parse as text_parse # to keep distinct from urllib's parse
from pattern.en import parsetree
import sys
from pymongo import MongoClient

EXPIRE_IN = 10800 # this is 3 hours in seconds

beanstalk = beanstalkc.Connection(host='localhost', port=14711)
client = MongoClient(tz_aware=True)
db = client.curriculum
# c=0 # debug counter
# output = open('test_output_redis.txt','w') # deprecated, was for debug


while True:
    # take URL and groupID
    # resolve URL into chunks and shove them in 'keywords' with same groupID
    # delete job
    print 'starting worker outer loop'
    job = beanstalk.reserve() # this is blocking, waits till there's something on the stalk
    pay = job.body.split('|')
    groupID = pay[0]
    url = URL(pay[-1])
    print 'new url, we think', url
    try:
        s = url.download(cached=True)
        print url.mimetype
        if (url.mimetype in MIMETYPE_WEBPAGE) or (url.mimetype in MIMETYPE_PLAINTEXT):
            s = plaintext(s)
            '''
            parsetree(string,
                   tokenize = True,         # Split punctuation marks from words?
                       tags = True,         # Parse part-of-speech tags? (NN, JJ, ...)
                     chunks = True,         # Parse chunks? (NP, VP, PNP, ...)
                  relations = False,        # Parse chunk relations? (-SBJ, -OBJ, ...)
                    lemmata = False,        # Parse lemmata? (ate => eat)
                   encoding = 'utf-8'       # Input string encoding.
                     tagset = None)         # Penn Treebank II (default) or UNIVERSAL.
            '''
            # parsed = text_parse(s, chunks = True)
            parsed = parsetree(s, chunks=True)
            for sentence in parsed:
                # only noun phrases for now but let's pick some good other ones next week
                # seeing ADJP, ADVP, PP and VP mostly tho NP are predominant
                # gen = (the_chunk for the_chunk in sentence.chunks if the_chunk.type=='NP')
                # for chunk in gen:
                for chunk in sentence.chunks:
                    d = db.keywords.update(
                            {'keyword':chunk.string, 'type':chunk.type, 'groupID':groupID},
                            {'$push' : {'timestamp':timestamp, 'url':url}, '$set' : {'latest':timestamp}},
                            upsert=True
                            )
                    print d
        else:
            'we failed the mimetype test again wtf'
    except HTTPError, e:
        # e = sys.exc_info()[0]
        # print 'URLError on ', url
        print url
        print e
    # end of if(isThere < 2)
    job.delete()
    randy = r_text.randomkey()
    print randy.upper()
    print 'that key has this much time to live', r_text.ttl(randy)