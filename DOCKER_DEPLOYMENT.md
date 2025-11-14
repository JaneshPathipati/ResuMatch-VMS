# 🐳 Docker Deployment Guide - ResuMatch VMS

Complete guide to containerize and deploy ResuMatch VMS using Docker.

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Local Development with Docker](#local-development-with-docker)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)
- `.env` file configured with your credentials

### 1. Clone and Setup
```bash
# Ensure .env file exists with your credentials
cp .env.example .env
# Edit .env with your actual values
```

### 2. Start Everything with Docker Compose
```bash
# Build and start all services (MySQL + Flask App)
docker compose up -d

# View logs
docker compose logs -f

# Check status
docker compose ps
```

### 3. Access Application
- **Web Interface**: http://localhost:5000
- **MySQL Database**: localhost:3306

### 4. Stop Services
```bash
# Stop containers
docker compose down

# Stop and remove volumes (⚠️ deletes data)
docker compose down -v
```

---

## 🏠 Local Development with Docker

### Option 1: Use Docker Compose (Recommended)
Runs both MySQL and Flask app together:

```bash
docker compose up --build
```

### Option 2: Use Local MySQL + Dockerized App
If you prefer to use your existing MySQL Workbench:

```bash
# Build app container only
docker build -t resumatch-app .

# Run app container, connecting to host MySQL
docker run -d \
  --name resumatch-app \
  -p 5000:5000 \
  --env-file .env \
  -e MYSQL_HOST=host.docker.internal \
  resumatch-app
```

**Note**: `host.docker.internal` allows Docker to connect to your host machine's MySQL.

---

## 🌍 Production Deployment

### Option 1: Deploy with Remote MySQL (Oracle Cloud/AWS/Azure)

1. **Update `.env` for production:**
```env
# Remote MySQL Configuration
MYSQL_HOST=mysql-prod.your-cloud.com
MYSQL_PORT=3306
MYSQL_DATABASE=resumatch_db
MYSQL_USERNAME=prod_user
MYSQL_PASSWORD=strong_prod_password
MYSQL_USE_SSL=True

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_production_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
```

2. **Build and run app only:**
```bash
# Build
docker build -t resumatch-app:prod .

# Run
docker run -d \
  --name resumatch-app \
  -p 5000:5000 \
  --env-file .env.production \
  --restart unless-stopped \
  resumatch-app:prod
```

### Option 2: Deploy Complete Stack (App + MySQL)
```bash
# Use production docker compose
docker compose -f docker-compose.prod.yml up -d
```

---

## 🔧 Environment Configuration

### `.env` File Structure
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# Matching Configuration
MAX_VOLUNTEERS_TO_ANALYZE=50
TOP_MATCHES_TO_RETURN=10
MIN_MATCH_SCORE=60

# MySQL Configuration
# For Docker Compose: use "mysql" as host
# For remote MySQL: use actual hostname
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=resumatch_db
MYSQL_USERNAME=resumatch_user
MYSQL_PASSWORD=your_secure_password
MYSQL_USE_SSL=False
```

### Docker Compose Environment
When using `docker compose.yml`, the app automatically connects to the MySQL container using the service name `mysql`.

---

## 🔍 Useful Docker Commands

### Container Management
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# Stop a container
docker stop resumatch-app

# Remove a container
docker rm resumatch-app

# View logs
docker logs resumatch-app -f

# Execute commands inside container
docker exec -it resumatch-app bash
```

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi resumatch-app

# Rebuild image
docker build --no-cache -t resumatch-app .
```

### Docker Compose Commands
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f app
docker compose logs -f mysql

# Restart a service
docker compose restart app

# Rebuild and start
docker compose up -d --build

# Scale services
docker compose up -d --scale app=3
```

---

## 🗄️ Database Management

### Access MySQL Container
```bash
# Connect to MySQL inside container
docker exec -it resumatch_mysql mysql -u root -p

# Run SQL file
docker exec -i resumatch_mysql mysql -u root -p${MYSQL_PASSWORD} resumatch_db < backup.sql
```

### Backup Database
```bash
# Export database
docker exec resumatch_mysql mysqldump -u root -p${MYSQL_PASSWORD} resumatch_db > backup.sql

# Import database
docker exec -i resumatch_mysql mysql -u root -p${MYSQL_PASSWORD} resumatch_db < backup.sql
```

### Persistent Data
Data is stored in Docker volumes:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect resumatch-vms_mysql_data

# Backup volume
docker run --rm -v resumatch-vms_mysql_data:/data -v $(pwd):/backup ubuntu tar czf /backup/mysql_backup.tar.gz /data
```

---

## 🚨 Troubleshooting

### Issue: App can't connect to MySQL
**Solution:**
```bash
# Check if MySQL is healthy
docker compose ps

# View MySQL logs
docker compose logs mysql

# Ensure .env has correct MYSQL_HOST
# For docker compose: MYSQL_HOST=mysql
# For host MySQL: MYSQL_HOST=host.docker.internal
```

### Issue: Port already in use
**Solution:**
```bash
# Find process using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Change port in docker compose.yml
ports:
  - "8080:5000"  # Use port 8080 instead
```

### Issue: Database not initialized
**Solution:**
```bash
# Remove volumes and recreate
docker compose down -v
docker compose up -d

# Or manually run init.sql
docker exec -i resumatch_mysql mysql -u root -p${MYSQL_PASSWORD} resumatch_db < init.sql
```

### Issue: Permission denied errors
**Solution:**
```bash
# Fix file permissions
chmod +x app.py
chmod 644 .env

# Or run container as root
docker run --user root ...
```

---

## 📊 Health Checks

Both services have health checks configured:

### Check App Health
```bash
curl http://localhost:5000/api/stats
```

### Check MySQL Health
```bash
docker exec resumatch_mysql mysqladmin ping -h localhost -u root -p${MYSQL_PASSWORD}
```

---

## 🌐 Deploy to Cloud Platforms

### Deploy to AWS ECS
```bash
# Tag image
docker tag resumatch-app:latest your-account.dkr.ecr.region.amazonaws.com/resumatch-app:latest

# Push to ECR
docker push your-account.dkr.ecr.region.amazonaws.com/resumatch-app:latest
```

### Deploy to Google Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/your-project/resumatch-app

# Deploy
gcloud run deploy resumatch-app \
  --image gcr.io/your-project/resumatch-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy to Azure Container Instances
```bash
# Login to Azure
az login

# Create container
az container create \
  --resource-group resumatch-rg \
  --name resumatch-app \
  --image resumatch-app:latest \
  --dns-name-label resumatch-app \
  --ports 5000
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** ✅ Already in `.gitignore`
2. **Use strong passwords** in production
3. **Enable SSL for MySQL** when using remote databases
4. **Use Docker secrets** for sensitive data in production
5. **Run containers as non-root user** (add to Dockerfile)
6. **Scan images for vulnerabilities**:
   ```bash
   docker scan resumatch-app
   ```

---

## 📈 Monitoring

### View Real-time Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f app

# Last 100 lines
docker compose logs --tail=100 app
```

### Container Stats
```bash
# Real-time stats
docker stats

# Specific container
docker stats resumatch-app
```

---

## 🎯 Next Steps

1. ✅ Container is running
2. Test all features (upload resume, matching, etc.)
3. Configure production environment variables
4. Deploy to your preferred cloud platform
5. Set up CI/CD pipeline (GitHub Actions, Jenkins, etc.)
6. Configure monitoring and logging (Prometheus, Grafana, etc.)

---

**🐳 Happy Dockerizing! Your ResuMatch VMS is now containerized and portable!**

