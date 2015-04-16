self-contained curriculum (test)
===============

ec2-based __dockerized__ curriculum server test B-)

`sudo apt-get install git beanstalkd mongod build-essential python-dev python-pip -y`
`sudo pip install pattern tornado --upgrade`

Stack:

Docker - all the cool kids are doing it while crying

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


***DEPLOYMENT NOTES***

![OHBOY]( http://cdn.gifbay.com/2013/08/oh_neato-77078.gif )

Get docker
`sudo apt-get install docker`
...just kidding! You __must__ follow the absurd wget instructions [here](https://docs.docker.com/installation/ubuntulinux/)

__Note this part to avoid perpetually having to `sudo !!`__
````
If you would like to use Docker as a non-root user, you should now consider
adding your user to the "docker" group with something like:

  sudo usermod -aG docker ubuntu

Remember that you will have to log out and back in for this to take effect!
````

Generate images from dockerfiles:
* mongo image is the default, we don't need to generate it here
* beanstalk: go to /beanstalk, type `docker build -t akabeanstalk . `
* worker: go to /worker, type `docker build -t akaworker . `
* server: go to /server, type `docker build -t akaserver . `

Run each image __in this order__:

* `docker run --name akamongo -d -p 27017:27017 mongo --smallfiles`
* `docker run --name akabeanstalk -d akabeanstalk`
* `docker run --name akaworker -d --link akamongo:akamongo --link akabeanstalk:akabeanstalk akaworker`
* `docker run --name akaserver -d --link akamongo:akamongo --link akabeanstalk:akabeanstalk -p 80:80 akaserver`
* You must be thirsty :beer:
