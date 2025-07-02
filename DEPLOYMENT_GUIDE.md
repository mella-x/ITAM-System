# ITAM System Deployment Guide

## Quick Start (Development)

### 1. Extract the System
```bash
tar -xzf ITAM_System_Complete.tar.gz
cd ITAM_System_Complete/
```

### 2. Start Backend (Terminal 1)
```bash
cd itam_backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 3. Start Frontend (Terminal 2)
```bash
cd itam-frontend
npm install
npm run dev
```

### 4. Access the System
- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000/api/v1/itam/api/
- **Admin Panel**: http://localhost:8000/admin/

## Production Deployment

### Option 1: Traditional Server Deployment

#### Backend (Django)
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Create production settings
# itam_backend/itam_backend/production_settings.py
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 itam_backend.wsgi:application
```

#### Frontend (Vue.js)
```bash
# Build for production
npm run build

# Serve with Nginx
# /etc/nginx/sites-available/itam
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/itam-frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Docker Deployment

#### Create Dockerfile for Backend
```dockerfile
# itam_backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "itam_backend.wsgi:application"]
```

#### Create Dockerfile for Frontend
```dockerfile
# itam-frontend/Dockerfile
FROM node:20-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: itam_db
      POSTGRES_USER: itam_user
      POSTGRES_PASSWORD: itam_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./itam_backend
    ports:
      - "8000:8000"
    environment:
      - DB_NAME=itam_db
      - DB_USER=itam_user
      - DB_PASSWORD=itam_password
      - DB_HOST=db
    depends_on:
      - db

  frontend:
    build: ./itam-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Option 3: Cloud Deployment

#### Heroku Deployment
```bash
# Backend
cd itam_backend
echo "web: gunicorn itam_backend.wsgi" > Procfile
echo "python-3.11.0" > runtime.txt
git init
heroku create your-itam-backend
heroku addons:create heroku-postgresql:hobby-dev
git add .
git commit -m "Initial commit"
git push heroku main

# Frontend
cd itam-frontend
npm run build
# Deploy dist folder to Netlify, Vercel, or similar
```

#### AWS Deployment
- **Backend**: Deploy to Elastic Beanstalk or ECS
- **Frontend**: Deploy to S3 + CloudFront
- **Database**: Use RDS PostgreSQL

## Environment Configuration

### Backend Environment Variables
```bash
# .env file for backend
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_NAME=itam_production
DB_USER=itam_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend Environment Variables
```bash
# .env file for frontend
VITE_API_BASE_URL=https://your-backend-domain.com/api/v1/itam/api
VITE_APP_TITLE=ITAM System
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CORS origins
- [ ] Set up database backups
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular security updates

## Performance Optimization

### Backend
- Use Redis for caching
- Optimize database queries
- Set up database indexing
- Use CDN for static files

### Frontend
- Enable gzip compression
- Optimize images
- Use lazy loading
- Implement service workers

## Monitoring & Maintenance

### Health Checks
```bash
# Backend health check
curl http://localhost:8000/api/v1/itam/api/dashboard/stats/

# Frontend health check
curl http://localhost:5173
```

### Backup Strategy
```bash
# Database backup
pg_dump itam_production > backup_$(date +%Y%m%d).sql

# File backup
tar -czf itam_backup_$(date +%Y%m%d).tar.gz /path/to/itam/
```

### Log Monitoring
- Set up centralized logging (ELK stack)
- Monitor API response times
- Track user activity
- Set up alerts for errors

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS_ALLOWED_ORIGINS in Django settings
   - Verify frontend API base URL

2. **Database Connection Issues**
   - Check database credentials
   - Verify database server is running
   - Check network connectivity

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT settings

4. **Frontend Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify environment variables

### Support Commands
```bash
# Check Django configuration
python manage.py check

# Test database connection
python manage.py dbshell

# View logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Implement database read replicas
- Use container orchestration (Kubernetes)

### Vertical Scaling
- Increase server resources
- Optimize database performance
- Use caching strategies

---

**For additional support, refer to the main README.md file or contact the development team.**

