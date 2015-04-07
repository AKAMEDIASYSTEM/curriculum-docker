self-contained curriculum (test)
===============

ec2-based curriculum server test

Stack:

Nginx - listens to the world on port 80, load balances (but not much for us, since we only have one tornado instance running)
/etc/nginx/nginx.conf - this holds the mapping from "listen on" to "send traffic to X servers"

Upstart - systemd-like "make sure main apps are running and if not, restart them". Need to document more config stuff for this.

Redis - the local curriculum implementation uses Redis for storing chunks of language. Not sure how to port over timestamps (for date-range API queries - necessary?) or do authentication (separate DB seems easiest)
* redis "0" - language fragments, probably simple K:V or List. TTL should be 7 days or so
* redis "1" - list of URLS we have processed quite recently - TTL here should be ~1 hour. We check against this before re-fetching the page to do any NLP+chunking
* redis "2" - authentication DB? Populated at boot form a static groups.py-like file?

Beanstalk - handles the queue of URLS-to-analyze from SubmitHandler

/server/server.py - this is the main tornado instance.
    * ApiHandler.py - services API queries. 
    * BaseHandler.py - just a superclass contining the isAuth() function
    * BrowserHandler.py - services web queries, currently only ZEN mode (this would be the prototype for other views)
    * SubmitHandler.py - accepts URLs from Chrome extension. Note we no longer accept SubmitAnon stuff; need to update Chrome client


/chrome - this holds the Chrome extension that submits HTTP URLs to the server
