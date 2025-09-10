#!/bin/bash

# Update package lists and upgrade existing packages
sudo apt-get update && sudo apt-get upgrade -y

# Install system dependencies
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    curl \
    libpcre3 \
    libpcre3-dev \
    python3-venv \
    supervisor

# Install Node.js and npm (for frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.12.3
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-venv python3.12-dev python3.12-distutils

# Set Python 3.12 as the default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Ensure pip is installed for Python 3.12
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# Install and configure PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE concert_db;"
sudo -u postgres psql -c "CREATE USER concert_user WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "ALTER ROLE concert_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE concert_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE concert_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE concert_db TO concert_user;"

# Create a directory for the application
mkdir -p /home/ubuntu/concert-booking-app

# Set up Python virtual environment
python3 -m venv /home/ubuntu/venv
source /home/ubuntu/venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install gunicorn psycopg2-binary

# Set up Gunicorn service
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOL
[Unit]
Description=Gunicorn service for Concert Booking App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/concert-booking-app/backend
ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/concert-booking-app/backend/concertbooking.sock concertbooking.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Set up Nginx
sudo tee /etc/nginx/sites-available/concert_booking > /dev/null <<EOL
server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/concert-booking-app/backend;
    }

    location /media/ {
        root /home/ubuntu/concert-booking-app/backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/concert-booking-app/backend/concertbooking.sock;
    }
}
EOL

# Enable the site and restart Nginx
sudo ln -s /etc/nginx/sites-available/concert_booking /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx

# Enable and start Gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# Set up firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw --force enable

echo "Setup completed successfully!"
echo "Please remember to:"
echo "1. Update the database settings in settings.py"
echo "2. Set up your domain name in the Nginx configuration"
echo "3. Set up SSL certificates with Let's Encrypt"
