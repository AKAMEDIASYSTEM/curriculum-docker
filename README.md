self-contained curriculum (test)
===============

ec2-based curriculum server test

sudo apt-get install git redis-server libxml2-dev libxslt-dev beanstalkd build-essential python-dev python-pip python-imaging -y
sudo pip install pattern tornado --upgrade

Stack:

__Nginx__ - listens to the world on port 80, load balances (but not much for us, since we only have one tornado instance running)
/etc/nginx/nginx.conf - this holds the mapping from "listen on" to "send traffic to X servers"

__Upstart__ - systemd-like "make sure main apps are running and if not, restart them". Need to document more config stuff for this.

__Redis__ - the local curriculum implementation uses Redis for storing chunks of language. Not sure how to port over timestamps (for date-range API queries - necessary?) or do authentication (separate DB seems easiest)
* redis "0" - language fragments, probably simple K:V or List. TTL should be 7 days or so
* redis "1" - list of URLS we have processed quite recently - TTL here should be ~1 hour. We check against this before re-fetching the page to do any NLP+chunking
* redis "2" - authentication DB? Populated at boot form a static groups.py-like file?

__Beanstalk__ - handles the queue of URLS-to-analyze from SubmitHandler

__/worker.py__ - this takes jobs form Beanstalk, checks Redis.1 to see if it should be resolved, and resolves it into chunks that are loaded into Redis.0 (HEY, how are we going to keep track of groupIDs here?)

__startDB.py__ - this shoves credentials from groups.py (NOT in this repo, full o' secrets) into Redis.2

__beanstalk.sh__ - must be run on boot, before __startDB.py__ and __server/server.py__

__/server/server.py__ - this is the main tornado instance.
* ApiHandler.py - services API queries. 
* BaseHandler.py - just a superclass contining the isAuth() function
* BrowserHandler.py - services web queries, currently only ZEN mode (this would be the prototype for other views)
* SubmitHandler.py - accepts URLs from Chrome extension. Note we no longer accept SubmitAnon stuff; need to update Chrome client


__/chrome__ - this holds the Chrome extension that submits HTTP URLs to the server
