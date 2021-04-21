#!/bin/bash
echo  "server {
    listen 80;
    listen [::]:80;
    server_name "$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)";
    root /var/www/moneyline/moneyline-app/dist/moneyline-app;
    server_tokens off;
    index index.html index.htm;
    location / {
        # First attempt to server request as file, then
        # as directory, then fall back to displaying a 404.
        try_files \$uri \$uri/ /index.html =404;
    }
    location /api {
       proxy_pass https://balldontlie.io/api/v1/;
       proxy_ssl_server_name on;
}
    location /get {
       proxy_pass http://moneyline-flask-env.eba-c2pzpmqb.us-east-2.elasticbeanstalk.com;
       proxy_ssl_server_name on;
}
}" >  /etc/nginx/sites-available/moneyline-app

cd /etc/nginx/sites-enabled
ln -s ../sites-available/moneyline-app
rm default
service nginx restart
