#self-contained curriculum

ec2-based __dockerized__ curriculum server

### Stack:

Docker - all the cool kids are doing it while crying

__MongoDB__ - like its forebear, the new curriculum implementation uses Mongo for storing chunks of language. The DB is called curriculum
* __db.keywords__ - language fragments, probably simple K:V or List. TTL should be 7 days or so
* __db.pages__ - list of URLS we have processed quite recently - TTL here should be ~1 hour. We check against this before re-fetching the page to do any NLP+chunking
* __db.users__ - authentication DB, very static; poplated at boot. It's a DB and not a flatfile so in the future we can perhaps dynamically add groupIDs and tokens but I'm in no rush

__Beanstalk__ - handles the queue of URLS-to-analyze from SubmitHandler. `beanstalk.sh` or the command therein must be run before before __startDB.py__ and __server/server.py__

__/worker.py__ - this takes jobs form Beanstalk, checks db.pages to see if it should be resolved, and resolves it into chunks that are loaded into __db.keywords__. When the worker encounters a URL that chokes it, worker dies and is auto-restarted by Docker.

__/server/server.py__ - this is the main tornado instance.
* ApiHandler.py - services API queries; trying a single endpoint here for flexibility
  * __t=4__ - number of minutes into the past to look
  * __n=4__ - number of entries to return, drawn randomly from the result-set
  * __type=ADJP__ - restrict results to a chunktype. Types available are: {NP, PP, VP, ADJP, ADVP, ANY}
* BaseHandler.py - just a superclass contining the isAuth() function
* BrowserHandler.py - services web queries, currently only ZEN mode (this would be the prototype for other views - add new views to curriculum-insular/server/templates)
* SubmitHandler.py - accepts URLs from Chrome extension.

__/chrome__ - this holds the Chrome extension that submits HTTP URLs to the server. The extension will prompt you for a groupID and token upon first install.

__/firefox__ - this holds the Firefox extension that submits HTTP URLs to the server. *Note*, you must enter your groupID and token to /data/submitter.js manually before installing.


### DEPLOYMENT NOTES

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

Git pull this repo

MANUALLY add the 'groups.py' file necessary for authentication to work

Generate images from dockerfiles:
* mongo image is the default, we don't need to generate it here
* beanstalk: go to /beanstalk, type `docker build -t akabeanstalk . `
* worker: go to /worker, type `docker build -t akaworker . `
* server: go to /server, type `docker build -t akaserver . `

Run each image __in this order__:

* `docker run --name akamongo -d -p 27017:27017 -v /var/lib/mongodb/:/data/db --restart=always mongo --smallfiles`
* `docker run --name akabeanstalk -d -p 14711:14711 --restart=always akabeanstalk`
* `docker run --name akaworker -d --link akamongo:akamongo --link akabeanstalk:akabeanstalk --restart=always akaworker`
* `docker run --name akaserver -d --link akamongo:akamongo --link akabeanstalk:akabeanstalk -p 80:80 --restart=always akaserver`
* You must be thirsty :beer:


### Restarting and adding new groups:
This currently sucks. If the server crashes, you must manually wipe the DB before restarting.
```
docker stop akaserver akaworker akabeanstalk akamongo
docker rm akaserver akaworker akabeanstalk akamongo
docker rmi mongo akaserver
sudo rm -r /var/lib/mongodb/
cd /curriculum-docker/server
(edit groups.py to add new groups and tokens)
docker build -t akaserver .
```
...then execute the four "run" steps in the section above