#Troubleshooting

**If the server is not responding:** ssh into the server and run `docker ps` - you should see four running containers and stats about the uptime. The container `akaworker` is designed to restart frequently, so don't be alarmed by recent restarts for that container - all other containers should show the same uptime. If something looks amiss, it's best to just turn Curriculm off and on again:

First turn everything off:
```
docker stop akaserver akaworker akabeanstalk akamongo
docker rm akaserver akaworker akabeanstalk akamongo
docker rmi mongo akaserver
sudo rm -r /var/lib/mongodb/
cd /curriculum-docker/server
(edit groups.py to add new groups and tokens)
docker build -t akaserver .
```

Then turn everything on again **in this order:**
* `docker run --name akamongo -d -p 27017:27017 -v /var/lib/mongodb/:/data/db --restart=always mongo --smallfiles`
* `docker run --name akabeanstalk -d -p 14711:14711 --restart=always akabeanstalk`
* `docker run --name akaworker -d --link akamongo:akamongo --link akabeanstalk:akabeanstalk --restart=always akaworker`
* `docker run --name akaserver -d --link akamongo:akamongo --link akabeanstalk:akabeanstalk -p 80:80 --restart=always akaserver`
* You must be thirsty :beer:

**If the server is working fine but only serving out "No Results to Be Found"**, this means the timeframe you are asking for has no activity in it. You can resolve this by ensuring your Curriculum Chrome Extension is enabled and visiting some sites - if you're demoing the system and just need to quickly add terms, going to Stack Overflow is a good bet - it's easily parse-able and yields interesting terms.

If you don't want to seed the DB with spurious terms, you can also **extend the timeframe of the DB query** - just add `t=1000000000` to your query string to be sure you are drawing from all possible terms in the DB.

