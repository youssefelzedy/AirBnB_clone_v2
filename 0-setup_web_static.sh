#!/usr/bin/env bash
# sets up my web servers for the deployment of web_static

content='
<html>
<head>
</head>
<body>
Holberton School
</body>
</html>
'
new_server='\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t}'

sudo apt-get -y update
sudo apt-get -y install nginx
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
touch /data/web_static/releases/test/index.html
echo "$content" >  /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sed -i "/server_name _;/a\ $new_server" /etc/nginx/sites-available/default
sudo service nginx restart
