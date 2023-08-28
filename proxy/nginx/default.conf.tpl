server {
    listen 80;
    server_name bonappetit.website www.bonappetit.website;

    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

