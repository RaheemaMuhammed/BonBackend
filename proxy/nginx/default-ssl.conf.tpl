upstream backend {
    server 0.0.0.0:8000;
}
server {
    listen 80;
    server_name bonappetit.website www.bonappetit.website;

    location /.well-known/acme-challenge{
        root /vol/www/; 
    }
    
    location / {
        return 301 https://$host$request_uri;
    }
    
    location /ws {
        return 301 https://$host$request_uri;  
    }
}

server {
    listen 443 ssl;
    server_name bonappetit.website www.bonappetit.website;

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
         include  /etc/nginx/proxy_params;
         
         
     }

     location /wss {
         proxy_pass http://backend; 
         include /etc/nginx/proxy_params_ws;
         
     }
}
