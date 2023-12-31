upstream backend {
    server backend:8000;
}
server {
    listen 80;
    server_name bonappetit.website www.bonappetit.website;
    client_max_body_size 100M;
    location /.well-known/acme-challenge{
        root /vol/www/; 
    }
    
    location / {
        return 301 https://$host$request_uri;
    }
    location /ws/ {
        return 301 https://$host$request_uri;
    }
    
}

server {
    listen 443 ssl;
    server_name bonappetit.website www.bonappetit.website;
    client_max_body_size 100M;
    ssl_certificate     /etc/letsencrypt/live/bonappetit.website/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bonappetit.website/privkey.pem;

    include /etc/nginx/options-ssl-nginx.conf;

    ssl_dhparam /vol/proxy/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location /static/ {
         alias /vol/app/static/;
     }
      location /media/ {
         alias /vol/app/media/ ;
     }

   
     location / {
         proxy_pass http://backend;
         proxy_set_header    HOST    ${DOLLAR}host;
         proxy_set_header    X-Real-IP   ${DOLLAR}remote_addr;
        proxy_set_header    X-Forwarded-for ${DOLLAR}remote_addr;
        proxy_set_header X-Forwarded-Proto ${DOLLAR}scheme;
        proxy_http_version 1.1;
        port_in_redirect off;
        proxy_set_header Upgrade ${DOLLAR}http_upgrade;
        proxy_set_header Connection "upgrade";
       
     }

     location /wss/ {
         proxy_pass http://backend; 
         proxy_set_header X-Real-IP ${DOLLAR}remote_addr;
        proxy_set_header X-Forwarded-for ${DOLLAR}proxy_add_x_forwarded_for;
        proxy_set_header Host ${DOLLAR}http_host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade ${DOLLAR}http_upgrade;
        proxy_set_header Connection "upgrade";
         
     }
}
