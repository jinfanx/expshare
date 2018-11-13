docker exec expserver1 nohup uwsgi --http 172.17.0.3:8000 --chdir /data/expshare --module expshare.wsgi>server1.log &
docker exec expserver2 nohup uwsgi --http 172.17.0.4:8001 --chdir /data/expshare --module expshare.wsgi>server2.log &   
