#!/bin/bash

# Concert Booking App - EC2 Setup Script (SQLite Version)
# This script sets up the entire app on a single EC2 instance with SQLite

set -e

echo "🚀 Starting Concert Booking App EC2 Setup (SQLite)..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies (NO PostgreSQL)
echo "📦 Installing dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    nginx \
    git \
    curl \
    python3-venv \
    supervisor \
    build-essential

# Install Node.js 18
echo "📦 Installing Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /home/ubuntu/concert-booking-app
sudo chown ubuntu:ubuntu /home/ubuntu/concert-booking-app

# Navigate to app directory
cd /home/ubuntu/concert-booking-app

# Clone repository (adjust URL as needed)
echo "⬇️  Cloning repository..."
git clone https://github.com/YOUR_USERNAME/concert-booking-app.git . 2>/dev/null || echo "Repository already exists"

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p /var/log/gunicorn
mkdir -p /run/gunicorn
sudo chown ubuntu:www-data /var/log/gunicorn
sudo chown ubuntu:www-data /run/gunicorn

# Run migrations
echo "🗄️  Running Django migrations..."
cd backend
python manage.py migrate
echo "✅ Migrations completed"

# Create superuser (optional - commented out)
# python manage.py createsuperuser

# Populate sample data
echo "📊 Populating sample concert data..."
python manage.py populate_sample_data
echo "✅ Sample data populated"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput
echo "✅ Static files collected"

cd /home/ubuntu/concert-booking-app

# Create Gunicorn systemd service
echo "⚙️  Setting up Gunicorn service..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<'EOL'
[Unit]
Description=Gunicorn service for Concert Booking App
After=network.target

[Service]
Type=notify
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/concert-booking-app/backend
Environment="PATH=/home/ubuntu/concert-booking-app/venv/bin"
ExecStart=/home/ubuntu/concert-booking-app/venv/bin/gunicorn \
    --workers 3 \
    --worker-class sync \
    --bind unix:/run/gunicorn/concertbooking.sock \
    --error-logfile /var/log/gunicorn/error.log \
    --access-logfile /var/log/gunicorn/access.log \
    --timeout 120 \
    concertbooking.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Enable and start Gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
echo "✅ Gunicorn service enabled"

# Build frontend
echo "🏗️  Building frontend..."
cd /home/ubuntu/concert-booking-app/frontend
npm install
npm run build
echo "✅ Frontend built"

# Setup Nginx
echo "⚙️  Configuring Nginx..."
sudo tee /etc/nginx/sites-available/concert_booking > /dev/null <<'EOL'
upstream gunicorn {
    server unix:/run/gunicorn/concertbooking.sock fail_timeout=0;
}

server {
    listen 80;
    server_name _;
    client_max_body_size 20M;

    # Frontend - Serve Vue.js SPA
    location / {
        root /home/ubuntu/concert-booking-app/frontend/dist;
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }

    # Backend API
    location /api/ {
        proxy_pass http://gunicorn;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_read_timeout 86400;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /home/ubuntu/concert-booking-app/backend/staticfiles/;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }

    # Deny access to database and sensitive files
    location ~ /db\.sqlite3 {
        deny all;
    }

    location ~ /\.env {
        deny all;
    }

    location ~ /\.git {
        deny all;
    }
}
EOL

# Enable Nginx site
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/concert_booking /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
echo "✅ Nginx configured and started"

# Setup firewall
echo "🔐 Setting up firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
echo "✅ Firewall configured"

# Display status
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ Setup Completed Successfully!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📌 Next Steps:"
echo "1. Update settings.py with your domain name:"
echo "   ALLOWED_HOSTS = ['your-domain.com', 'your-ec2-ip']"
echo ""
echo "2. Update API URL in frontend/src/services/api.js:"
echo "   const API_BASE_URL = 'http://your-ec2-ip/api'"
echo ""
echo "3. Set up SSL with Let's Encrypt:"
echo "   sudo apt-get install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d your-domain.com"
echo ""
echo "4. Create Django superuser (optional):"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   python manage.py createsuperuser"
echo ""
echo "📊 Service Status:"
echo "  Gunicorn:  sudo systemctl status gunicorn"
echo "  Nginx:     sudo systemctl status nginx"
echo ""
echo "📝 Logs:"
echo "  Gunicorn error:  /var/log/gunicorn/error.log"
echo "  Gunicorn access: /var/log/gunicorn/access.log"
echo "  Nginx error:     /var/log/nginx/error.log"
echo ""
echo "🌐 Access your app at:"
echo "  http://your-ec2-public-ip"
echo "  Admin panel: http://your-ec2-public-ip/admin"
echo ""
echo "════════════════════════════════════════════════════════════════"
