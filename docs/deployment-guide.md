# 🚀 Deployment Guide - Concert Booking App

## Deployment Options Overview

Your concert booking app can be deployed using several approaches. Here are the most popular and recommended options:

## 🌟 **Option 1: Netlify + Railway (Recommended for Beginners)**

### Frontend (Vue.js) → Netlify
- **Free tier available**
- **Automatic builds from Git**
- **Global CDN**
- **Custom domains**

### Backend (Django) → Railway
- **Easy Django deployment**
- **PostgreSQL included**
- **Environment variables**
- **Automatic HTTPS**

### Steps:
1. **Frontend to Netlify:**
   ```bash
   cd frontend
   npm run build
   # Upload dist/ folder to Netlify
   ```

2. **Backend to Railway:**
   - Connect your GitHub repo
   - Railway auto-detects Django
   - Add PostgreSQL database
   - Set environment variables

## 🔥 **Option 2: Vercel + PlanetScale (Modern Stack)**

### Frontend (Vue.js) → Vercel
- **Excellent Vue.js support**
- **Edge functions**
- **Automatic deployments**
- **Free tier**

### Backend (Django) → Railway/Render
- **API deployment**
- **Database included**

### Database → PlanetScale
- **Serverless MySQL**
- **Branching for databases**
- **Free tier**

## ☁️ **Option 3: AWS (Enterprise/Scalable)**

### Frontend → AWS S3 + CloudFront
- **Static site hosting**
- **Global CDN**
- **High availability**

### Backend → AWS EC2/ECS + RDS
- **Full control**
- **Auto-scaling**
- **Managed database**

## 🐳 **Option 4: Docker + Any Cloud Provider**

### Containerized Deployment
- **Consistent environments**
- **Easy scaling**
- **Platform agnostic**

## 📋 **Pre-Deployment Checklist**

### Backend Preparation (SQLite)
- [ ] Ensure db.sqlite3 location is writable on server
- [ ] Set environment variables
- [ ] Configure static files
- [ ] Update CORS settings
- [ ] Set DEBUG=False
- [ ] Configure allowed hosts
- [ ] Update ALLOWED_HOSTS in settings.py with your domain/IP

### Frontend Preparation
- [ ] Update API base URL for production
- [ ] Build for production
- [ ] Configure routing for SPA
- [ ] Optimize assets

## 🛠️ **Detailed Deployment Steps for EC2 (SQLite)**

### Step 1: Prepare Backend for EC2
```python
# In settings.py - Update these settings:

# Set DEBUG to False
DEBUG = False

# Set proper ALLOWED_HOSTS
ALLOWED_HOSTS = ['your-ec2-ip', 'your-domain.com', '127.0.0.1']

# Update CORS for production
CORS_ALLOWED_ORIGINS = [
    "http://your-ec2-ip",
    "https://your-domain.com",
    "http://localhost:8080",  # Keep for testing if needed
]

# Database (SQLite - already configured)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Ensure static files are configured
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Step 2: Create Simplified Setup Script for EC2 (SQLite)
```bash
#!/bin/bash
# Setup for EC2 with SQLite

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies (NO PostgreSQL needed)
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    nginx \
    git \
    curl \
    python3-venv \
    supervisor

# Install Node.js for frontend
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Create app directory
mkdir -p /home/ubuntu/concert-booking-app
cd /home/ubuntu/concert-booking-app

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Clone your repository
git clone https://github.com/your-username/concert-booking-app.git .

# Install Python dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Create Gunicorn socket directory
mkdir -p /run/gunicorn

# Set permissions
sudo chown ubuntu:www-data /home/ubuntu/concert-booking-app
sudo chmod 755 /home/ubuntu/concert-booking-app

echo "Setup completed!"
```

### Step 3: Run Migrations and Populate Data
```bash
cd /home/ubuntu/concert-booking-app/backend
source ../venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Populate sample data
python manage.py populate_sample_data

# Collect static files
python manage.py collectstatic --noinput
```

### Step 4: Set Up Gunicorn Service
```bash
# Create systemd service file
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOL
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
    --bind unix:/run/gunicorn/concertbooking.sock \
    --error-logfile /var/log/gunicorn/error.log \
    --access-logfile /var/log/gunicorn/access.log \
    concertbooking.wsgi:application
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOL

# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:www-data /var/log/gunicorn

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### Step 5: Build and Deploy Frontend
```bash
cd /home/ubuntu/concert-booking-app/frontend

# Update API URL in src/services/api.js
# Change line: const API_BASE_URL = 'http://localhost:8000/api'
# To: const API_BASE_URL = 'http://your-ec2-ip/api'

# Build frontend
npm install
npm run build

# Copy to Nginx directory
sudo mkdir -p /var/www/concert-app
sudo cp -r dist/* /var/www/concert-app/
sudo chown -R www-data:www-data /var/www/concert-app
```

### Step 6: Configure Nginx
```bash
sudo tee /etc/nginx/sites-available/concert_booking > /dev/null <<EOL
server {
    listen 80;
    server_name your_ec2_ip your_domain;

    client_max_body_size 20M;

    # Frontend
    location / {
        root /var/www/concert-app;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn/concertbooking.sock;
    }

    # Admin panel
    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn/concertbooking.sock;
    }

    # Static files
    location /static/ {
        alias /home/ubuntu/concert-booking-app/backend/staticfiles/;
    }

    # Deny access to db.sqlite3
    location ~ /db\.sqlite3 {
        deny all;
    }
}
EOL

# Enable site
sudo ln -s /etc/nginx/sites-available/concert_booking /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and reload
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Set Up SSL Certificate (Let's Encrypt)
```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Step 8: Configure Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

## 🌐 **Environment Variables for Production**

Create `.env` file in `/home/ubuntu/concert-booking-app/backend/`:
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=your-ec2-ip,your-domain.com
CORS_ALLOWED_ORIGINS=http://your-ec2-ip,https://your-domain.com
```

## 🌐 **Environment Variables Needed**

### Backend (EC2)
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-ec2-ip,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-frontend-domain,http://your-ec2-ip
```

### Frontend (Update API URL)
```javascript
// src/services/api.js
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'http://your-ec2-ip/api'  // or https://your-domain.com/api after SSL setup
  : 'http://localhost:8000/api'
```

## 🔒 **Security Considerations**

### Production Security Checklist
- [ ] Change Django SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up HTTPS (SSL certificates)
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Add rate limiting
- [ ] Set up monitoring

## 📊 **Monitoring & Maintenance**

### Recommended Tools
- **Error Tracking**: Sentry
- **Performance**: New Relic/DataDog
- **Uptime**: UptimeRobot
- **Analytics**: Google Analytics
- **Logs**: CloudWatch/Papertrail

## 💰 **Cost Estimates (AWS EC2)**

### Development (Free Tier)
- **EC2**: t2.micro - Free for 12 months (new AWS accounts)
- **Storage**: 30GB EBS - Free for 12 months
- **Total**: $0/month (first year)

### Production (Small Scale)
- **EC2**: t3.medium - ~$30/month
- **Storage**: 50GB EBS - ~$5/month
- **Data Transfer**: Included (up to 100GB/month free)
- **Total**: ~$35-40/month

### Production (Medium Scale)
- **EC2**: t3.large - ~$60/month
- **Storage**: 100GB EBS - ~$10/month
- **Backup**: Snapshots - ~$5/month
- **Total**: ~$75/month

### Notes on SQLite
- ✅ No separate database costs
- ✅ Backups are just file copies
- ⚠️ Not recommended for 1000+ concurrent users
- 💡 Works great for small-medium applications

## 🎯 **Recommended Deployment Path**

For your concert booking app, I recommend:

1. **Start with**: Netlify (frontend) + Railway (backend)
2. **Upgrade to**: Vercel + dedicated server when scaling
3. **Enterprise**: AWS/GCP with full infrastructure

This gives you a professional deployment that can handle real users and scale as your app grows!
