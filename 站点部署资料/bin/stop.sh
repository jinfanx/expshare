kill -9 `ps -ef|grep wsgi|awk '{print $2}'`
