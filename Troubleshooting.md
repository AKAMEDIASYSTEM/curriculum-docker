#Troubleshooting

*If the server is not responding:* ssh into the server and run `docker ps` - you should see four running containers and stats about the uptime. The container `akaworker` is designed to restart frequently, so don't be alarmed by recent restarts for that container - all other containers should show the same uptime.

*If the server is working fine but only serving out "No Results to Be Found"*, this means the timeframe you are asking for has no activity in it. You can resolve this by ensuring your Curriculum Chrome Extension is enabled and visiting some sites - if you're demoing the system and just need to quickly add terms, going to Stack Overflow is a good bet - it's easily parse-able and yields interesting terms.

If you don't want to seed the DB with spurious terms, you can also extend the timeframe of the DB query - just add `t=1000000000` to your query string to be sure you are drawing from all possible terms in the DB.