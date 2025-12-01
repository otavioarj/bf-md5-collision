# 🚀 Deployment Guide

This guide covers different deployment options for the Brainfuck MD5 Collision Challenge.

---

## 📋 Table of Contents

- [Quick Deploy (Docker)](#quick-deploy-docker)
- [Production Deployment](#production-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Security Considerations](#security-considerations)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## 🐳 Quick Deploy (Docker)

### Prerequisites

- Docker installed
- Docker Compose (optional but recommended)

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/maycon/bf-md5-collision.git
cd bf-md5-collision

# Start the application
docker compose up -d

# View logs
docker compose logs -f

# Stop the application
docker compose down
```

The application will be available at `http://localhost:8000`

### Using Docker directly

```bash
# Build the image
docker build -t bf-md5-collision .

# Run the container
docker run -d \
  --name bf-collision \
  -p 8000:8000 \
  -e FLAG="FLAG{your_custom_flag_here}" \
  bf-md5-collision

# View logs
docker logs -f bf-collision

# Stop and remove
docker stop bf-collision
docker rm bf-collision
```

---

## 🏭 Production Deployment

### 1. Environment Setup

Create a `.env` file (DO NOT commit this):

```bash
# .env
FLAG=FLAG{your_production_flag_here}
SECRET_KEY=your-secure-secret-key-here
FLASK_ENV=production
WORKERS=4
TIMEOUT=60
```

### 2. Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/bf-collision
server {
    listen 80;
    server_name collision.hacknroll.academy;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=upload_limit:10m rate=10r/m;
    limit_req zone=upload_limit burst=20 nodelay;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # File upload limits
    client_max_body_size 1M;
}
```

Enable and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/bf-collision /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. SSL/TLS with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d collision.hacknroll.academy

# Auto-renewal is set up automatically
sudo certbot renew --dry-run
```

### 4. Systemd Service

Create `/etc/systemd/system/bf-collision.service`:

```ini
[Unit]
Description=Brainfuck MD5 Collision Challenge
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/bf-md5-collision
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bf-collision
sudo systemctl start bf-collision
sudo systemctl status bf-collision
```

---

## ☁️ Cloud Platforms

### AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.micro or larger
   - Security group: Allow 80, 443

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose nginx certbot python3-certbot-nginx
   sudo usermod -aG docker ubuntu
   ```

3. **Deploy application**
   ```bash
   git clone https://github.com/maycon/bf-md5-collision.git
   cd bf-md5-collision
   docker compose up -d
   ```

4. **Configure Nginx and SSL** (see above)

### AWS ECS (Fargate)

```yaml
# ecs-task-definition.json
{
  "family": "bf-collision",
  "containerDefinitions": [
    {
      "name": "bf-collision",
      "image": "your-ecr-repo/bf-collision:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLAG",
          "value": "FLAG{production_flag}"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/bf-collision",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "256",
  "memory": "512"
}
```

### Google Cloud Run

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/bf-collision

# Deploy to Cloud Run
gcloud run deploy bf-collision \
  --image gcr.io/PROJECT_ID/bf-collision \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLAG=FLAG{your_flag}
```

### DigitalOcean App Platform

```yaml
# .do/app.yaml
name: bf-collision
services:
  - name: web
    github:
      repo: maycon/bf-md5-collision
      branch: main
    dockerfile_path: Dockerfile
    http_port: 8000
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
      - key: FLAG
        value: FLAG{production_flag}
        scope: RUN_TIME
    health_check:
      http_path: /
```

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create bf-collision-app

# Set buildpack
heroku buildpacks:set heroku/python

# Configure environment
heroku config:set FLAG=FLAG{your_flag}

# Deploy
git push heroku main
```

---

## 🔒 Security Considerations

### 1. Rate Limiting

Implement rate limiting to prevent abuse:

```python
# Using Flask-Limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/', methods=['POST'])
@limiter.limit("10 per minute")
def upload_files():
    # ...
```

### 2. Input Validation

Already implemented:
- File size limits
- File type validation
- Brainfuck code validation
- Timeout protection

### 3. Security Headers

Add security headers in production:

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### 4. HTTPS Only

Enforce HTTPS in production:

```python
# Using Flask-Talisman
from flask_talisman import Talisman

if not app.debug:
    Talisman(app, force_https=True)
```

### 5. Secret Management

Use environment variables or secret managers:

```python
import os
from dotenv import load_dotenv

load_dotenv()

FLAG = os.environ.get('FLAG', 'FLAG{default_dev_flag}')
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
```

---

## 📊 Monitoring and Maintenance

### 1. Logging

Configure structured logging:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/bf-collision.log',
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('BF Collision Challenge startup')
```

### 2. Health Checks

Add a health check endpoint:

```python
@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }, 200
```

### 3. Metrics

Use Prometheus for metrics:

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Custom metrics
metrics.info('app_info', 'Application info', version='1.0.0')
```

### 4. Log Aggregation

Use ELK Stack or similar:

```yaml
# docker-compose.yml addition
  elasticsearch:
    image: elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  kibana:
    image: kibana:8.5.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

### 5. Backup Strategy

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/bf-collision"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup docker volumes
docker compose down
tar czf "$BACKUP_DIR/backup_$DATE.tar.gz" /var/lib/docker/volumes/
docker compose up -d

# Keep only last 7 backups
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
```

### 6. Update Process

```bash
#!/bin/bash
# update.sh

echo "Pulling latest changes..."
git pull

echo "Rebuilding Docker image..."
docker compose build

echo "Restarting services..."
docker compose down
docker compose up -d

echo "Cleaning up old images..."
docker image prune -f

echo "Update complete!"
```

---

## 📈 Performance Optimization

### 1. Caching

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@app.route('/source')
@cache.cached(timeout=3600)
def source():
    # ...
```

### 2. CDN for Static Files

Use CloudFlare, AWS CloudFront, or similar for static assets.

### 3. Database (if needed)

For tracking submissions:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/bf'
db = SQLAlchemy(app)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t bf-collision .
      
      - name: Deploy to production
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
        run: |
          echo "$SSH_PRIVATE_KEY" > key.pem
          chmod 600 key.pem
          ssh -i key.pem user@server 'cd /opt/bf-collision && git pull && docker compose up -d --build'
```

---

## 🆘 Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs -f

# Check container status
docker compose ps

# Restart
docker compose restart
```

### High memory usage

```bash
# Check container resources
docker stats

# Adjust worker count in compose.yaml
environment:
  - WORKERS=2  # Reduce workers
```

### Slow response times

- Check Gunicorn worker count
- Enable caching
- Use CDN for static files
- Monitor with Prometheus/Grafana

---

## 📞 Support

For deployment issues:
- Open an [issue](https://github.com/maycon/bf-md5-collision/issues)
- Check [discussions](https://github.com/maycon/bf-md5-collision/discussions)

---

**Happy Deploying! 🚀**