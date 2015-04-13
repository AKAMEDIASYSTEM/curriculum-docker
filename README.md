self-contained curriculum (test)
===============

ec2-based curriculum server test

`sudo apt-get install git beanstalkd mongod build-essential python-dev python-pip -y`
`sudo pip install pattern tornado --upgrade`

Stack:

__Nginx (not yet implemented)__ - listens to the world on port 80, load balances (but not much for us, since we only have one tornado instance running)
/etc/nginx/nginx.conf - this holds the mapping from "listen on" to "send traffic to X servers"

__Upstart (not yet implemented)__ - systemd-like "make sure main apps are running and if not, restart them". Need to document more config stuff for this.

__Supervisord__ - copy the two .conf files to /etc/supervisor/init.d/ and then run supervisor to start:

`sudo cp /curriculum-insular/curriculum_insular_* /etc/supervisor/init.d/`

OR `sudo cp /curriculum-insular/curriculum_insular_* /etc/supervisor/conf.d/` if init.d is absent

`sudo supervisorctl start curriculum_worker`

`sudo supervisorctl start curriculum_server`

to check status at any time, run `sudo supervisorctl` OR just check the logs in /var/log/supervisor/

__MongoDB__ - like its forebear, the new curriculum implementation uses Mongo for storing chunks of language. The DB is called curriculum
* __db.keywords__ - language fragments, probably simple K:V or List. TTL should be 7 days or so
* __db.pages__ - list of URLS we have processed quite recently - TTL here should be ~1 hour. We check against this before re-fetching the page to do any NLP+chunking
* __db.users__ - authentication DB, very static; poplated at boot. It's a DB and not a flatfile so in the future we can perhaps dynamically add groupIDs and tokens but I'm in no rush

__Beanstalk__ - handles the queue of URLS-to-analyze from SubmitHandler. `beanstalk.sh` or the command therein must be run before before __startDB.py__ and __server/server.py__

__/worker.py__ - this takes jobs form Beanstalk, checks db.pages to see if it should be resolved, and resolves it into chunks that are loaded into db.keywords

__startDB.py__ - this shoves credentials from groups.py (NOT in this repo, full o' secrets) into db.users

__/server/server.py__ - this is the main tornado instance.
* ApiHandler.py - services API queries; trying a single endpoint here for flexibility
  * __t=4__ - number of minutes into the past to look
  * __n=4__ - number of entries to return, drawn randomly from the result-set
  * __type=ADJP__ - restrict results to a chunktype. Types available are: {NP, PP, VP, ADJP, ADVP, ANY}
* BaseHandler.py - just a superclass contining the isAuth() function
* BrowserHandler.py - services web queries, currently only ZEN mode (this would be the prototype for other views - add new views to curriculum-insular/server/templates)
* SubmitHandler.py - accepts URLs from Chrome extension.

__/chrome__ - this holds the Chrome extension that submits HTTP URLs to the server
