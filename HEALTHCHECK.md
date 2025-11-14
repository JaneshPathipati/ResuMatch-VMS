# Health Check System

This repository includes comprehensive health check functionality for monitoring the ResuMatch-VMS application.

## Health Check Endpoints

### 1. Basic Health Check
```bash
GET /health
GET /api/health
```

Returns a simple health status:
```json
{
  "status": "healthy",
  "service": "ResuMatch-VMS",
  "timestamp": "2025-11-14 10:30:45"
}
```

### 2. Detailed Health Check
```bash
GET /health/detailed
GET /api/health/detailed
```

Returns detailed status of all components:
```json
{
  "status": "healthy",
  "service": "ResuMatch-VMS",
  "components": {
    "database": {
      "status": "healthy",
      "type": "MySQL",
      "host": "mysql"
    },
    "ai_service": {
      "status": "configured",
      "provider": "Azure OpenAI",
      "deployment": "gpt-4.1"
    },
    "resume_matcher": {
      "status": "ready",
      "type": "TF-IDF"
    },
    "resume_parser": {
      "status": "ready"
    }
  }
}
```

## Using Health Checks

### Via Setup Script (Recommended)
```bash
# Perform comprehensive health check
./setup.sh health

# Check container status
./setup.sh status
```

### Via Python Script
```bash
# Run from host
python3 healthcheck.py

# Run inside container
docker-compose exec app python healthcheck.py
```

### Via curl
```bash
# Basic health check
curl http://localhost:5000/health

# Detailed health check
curl http://localhost:5000/health/detailed | python3 -m json.tool
```

### Via Docker Health Check
```bash
# Check Docker health status
docker-compose ps

# View health check logs
docker inspect resumatch_app | grep -A 10 Health
```

## Health Check Features

### Setup Script (`./setup.sh health`)
- ✅ Checks if containers are running
- ✅ Tests basic health endpoint
- ✅ Retrieves detailed health status (JSON formatted)
- ✅ Runs comprehensive Python health check
- ✅ Validates MySQL connectivity

### Python Script (`healthcheck.py`)
- ✅ Flask application connectivity
- ✅ MySQL database accessibility
- ✅ Azure OpenAI configuration status
- ✅ Component-level health details
- ✅ Exit code for CI/CD integration (0 = healthy, 1 = unhealthy)

### Automatic Health Checks
The Flask application container includes automatic health checks:
- **Interval**: Every 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts
- **Start Period**: 40 seconds (grace period for startup)

## Integration with Monitoring

### Docker Compose
Health checks are automatically configured in `docker-compose.yml`:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/stats"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### CI/CD Integration
Use the Python health check script in your CI/CD pipeline:
```bash
# Will exit with code 0 if healthy, 1 if unhealthy
python3 healthcheck.py
if [ $? -eq 0 ]; then
  echo "Deployment successful"
else
  echo "Deployment failed - unhealthy"
  exit 1
fi
```

### Kubernetes/Container Orchestration
Use the health endpoints for liveness and readiness probes:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/detailed
    port: 5000
  initialDelaySeconds: 40
  periodSeconds: 15
```

## Troubleshooting

### Application Not Responding
```bash
# Check logs
./setup.sh logs app

# Restart services
./setup.sh restart

# Perform health check
./setup.sh health
```

### Database Connection Issues
```bash
# Check MySQL logs
./setup.sh logs mysql

# Test database connection
./setup.sh db

# Check database health
docker-compose exec mysql mysqladmin ping -h localhost -u root -p
```

### Component Status Issues
Check the detailed health endpoint to identify which component is failing:
```bash
curl http://localhost:5000/health/detailed | python3 -m json.tool
```

Look for components with `"status": "unhealthy"` or `"status": "error"` and check their error messages.
