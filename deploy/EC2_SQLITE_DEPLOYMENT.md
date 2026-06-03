# EC2 Deployment Guide - SQLite Version

## Quick Summary
- **Database**: SQLite (no PostgreSQL needed)
- **Frontend**: Vue.js built and served by Nginx
- **Backend**: Django/Gunicorn
- **Web Server**: Nginx
- **OS**: Ubuntu 22.04 LTS

## Prerequisites
1. EC2 instance running Ubuntu 22.04 LTS
2. Security Group with ports 22, 80, 443 open
3. Public IP address or domain name
4. SSH key configured

## Step-by-Step Deployment

### 1. SSH into Your EC2 Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 2. Clone and Run Setup Script
```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/concert-booking-app.git
cd concert-booking-app

# Run the setup script
chmod +x deploy/setup_ec2_sqlite.sh
./deploy/setup_ec2_sqlite.sh
```

The script will:
- ✅ Install all dependencies
- ✅ Set up Python virtual environment
- ✅ Run Django migrations
- ✅ Populate sample data
- ✅ Build frontend
- ✅ Configure Gunicorn & Nginx
- ✅ Set up firewall

### 3. Configure Your Domain/IP in Settings

Edit `backend/concertbooking/settings.py`:

```python
# Line ~20
ALLOWED_HOSTS = ['your-ec2-ip', 'your-domain.com']

# Line ~130
CORS_ALLOWED_ORIGINS = [
    "http://your-ec2-ip",
    "https://your-domain.com",
    "http://localhost:8080",
]
```

Restart Gunicorn:
```bash
sudo systemctl restart gunicorn
```

### 4. Update Frontend API URL

Edit `frontend/src/services/api.js`:

```javascript
// Line 3
const API_BASE_URL = 'http://your-ec2-ip/api'
// Or for HTTPS:
// const API_BASE_URL = 'https://your-domain.com/api'
```

Rebuild and deploy:
```bash
cd /home/ubuntu/concert-booking-app/frontend
npm run build
sudo cp -r dist/* /home/ubuntu/concert-booking-app/frontend/dist/
sudo systemctl restart nginx
```

### 5. Set Up SSL Certificate (Recommended)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

This will automatically update Nginx to use HTTPS.

## Verification

### Check Services Running
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo ufw status
```

### View Logs
```bash
# Gunicorn logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Test Backend
```bash
curl http://your-ec2-ip/api/concerts/
```

## Database Location
- **SQLite file**: `/home/ubuntu/concert-booking-app/backend/db.sqlite3`
- **Permissions**: Must be writable by `ubuntu` user
- **Backups**: Copy the `.sqlite3` file to backup

## Backup & Recovery

### Backup Database
```bash
cp /home/ubuntu/concert-booking-app/backend/db.sqlite3 ~/db-backup-$(date +%Y%m%d).sqlite3
```

### Restore Database
```bash
cp ~/db-backup-YYYYMMDD.sqlite3 /home/ubuntu/concert-booking-app/backend/db.sqlite3
sudo systemctl restart gunicorn
```

## Troubleshooting

### Services not starting
```bash
# Check Gunicorn status
sudo systemctl status gunicorn -l
sudo journalctl -u gunicorn -n 50

# Check Nginx status
sudo systemctl status nginx -l
sudo journalctl -u nginx -n 50
```

### Database locked error
```bash
# Restart Gunicorn
sudo systemctl restart gunicorn
```

### Frontend not loading
- Check that frontend was built: `ls /home/ubuntu/concert-booking-app/frontend/dist/`
- Restart Nginx: `sudo systemctl restart nginx`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`

### Backend returns 502 Bad Gateway
- Check Gunicorn socket exists: `ls /run/gunicorn/concertbooking.sock`
- Restart Gunicorn: `sudo systemctl restart gunicorn`
- Check Gunicorn logs: `sudo tail -f /var/log/gunicorn/error.log`

## Cost Breakdown
- **EC2 t3.medium**: ~$30/month (or free tier t2.micro)
- **Storage**: ~$5/month for 50GB
- **Data Transfer**: Usually free for typical usage
- **Domain**: $10-15/year (optional)

**Total: ~$35-40/month** (or free for first year with AWS free tier)

## Performance Tips
1. Use CloudFront CDN for static files
2. Enable browser caching with Cache-Control headers
3. Monitor Nginx and Gunicorn logs for errors
4. Set up automatic backups of db.sqlite3
5. Consider t3.large if experiencing high load

## Security Checklist
- ✅ Change Django SECRET_KEY before deployment
- ✅ Set DEBUG = False
- ✅ Restrict ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS
- ✅ Enable SSL/HTTPS
- ✅ Configure firewall properly
- ✅ Keep system packages updated
- ✅ Disable root SSH login
- ✅ Use SSH key authentication (not password)
- ✅ Restrict file permissions on db.sqlite3
- ✅ Regular backups of database

## Updating Your Application

### Pull Latest Changes
```bash
cd /home/ubuntu/concert-booking-app
git pull origin main
```

### Restart Services
```bash
# If backend changed
sudo systemctl restart gunicorn

# If frontend changed
cd frontend
npm run build
sudo systemctl restart nginx
```

## Need Help?
- Check logs first: Gunicorn and Nginx logs will show most issues
- Verify permissions on database and static files
- Ensure ALLOWED_HOSTS matches your domain
- Test API endpoint: `curl http://your-ip/api/concerts/`
