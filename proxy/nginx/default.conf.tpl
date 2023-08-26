server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN}

    location /.well-known/acme-challenge{
        root /vol/www/; 
    }
    
    location / {
        return 301 https://$host$request_uri
    }


    }






# upstream backend {
#     server backend:8000;
# }
# server {
#     listen 80;
#     location / {
#         proxy_pass http://backend;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header Host $host;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_http_version 1.1;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection "upgrade";
#     }

#     location /ws {
#         proxy_pass http://backend;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection "upgrade";
#     }
    
#     location /static/ {
#         alias /vol/app/static/;
#     }
#      location /media/ {
#         alias /vol/app/media/ ;
#     }
    


# }