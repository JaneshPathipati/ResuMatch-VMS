# MySQL Configuration Guide

## Important: MYSQL_USER cannot be "root"

MySQL Docker container does not allow setting `MYSQL_USER=root`. The root user is created automatically and should be controlled separately.

## Environment Variables

### Required Variables

```bash
# Root user password (created automatically)
MYSQL_ROOT_PASSWORD=your_secure_root_password

# Application database name
MYSQL_DATABASE=resumatch_db

# Application user (must NOT be "root")
MYSQL_USERNAME=resumatch_user

# Application user password
MYSQL_PASSWORD=your_secure_password
```

## Default Configuration

The project uses these defaults (defined in `docker compose.yml`):

```bash
MYSQL_ROOT_PASSWORD=Janesh@2006  # Root user password
MYSQL_DATABASE=resumatch_db       # Database name
MYSQL_USERNAME=resumatch_user     # Application user (NOT root)
MYSQL_PASSWORD=Janesh@2006        # Application user password
```

## User Roles

1. **root user**
   - Full admin privileges
   - Password: `MYSQL_ROOT_PASSWORD`
   - Used for: Database administration, health checks
   
2. **resumatch_user** (application user)
   - Limited privileges (only on resumatch_db)
   - Password: `MYSQL_PASSWORD`
   - Used for: Application connections

## Connecting to MySQL

### From Host Machine
```bash
# As root
mysql -h localhost -P 3306 -u root -p
# Enter MYSQL_ROOT_PASSWORD when prompted

# As application user
mysql -h localhost -P 3306 -u resumatch_user -p
# Enter MYSQL_PASSWORD when prompted
```

### From Docker Container
```bash
# Using setup script (connects as application user)
./setup.sh db

# Manual connection as root
docker compose exec mysql mysql -u root -p

# Manual connection as application user
docker compose exec mysql mysql -u resumatch_user -p
```

### From Python Application
The application automatically uses `MYSQL_USERNAME` and `MYSQL_PASSWORD` from environment variables.

## Security Best Practices

### For Development
1. Use the default passwords (already configured)
2. Never commit `.env` file to git
3. Keep `.env.example` as a template only

### For Production
1. **Change all default passwords!**
2. Use strong, unique passwords:
   ```bash
   MYSQL_ROOT_PASSWORD=<generate-strong-password>
   MYSQL_PASSWORD=<generate-different-strong-password>
   ```
3. Enable SSL/TLS:
   ```bash
   MYSQL_USE_SSL=True
   ```
4. Restrict network access to MySQL port
5. Use secrets management (Docker Secrets, Kubernetes Secrets, etc.)

## Troubleshooting

### Error: "Remove MYSQL_USER='root'"
**Cause**: You set `MYSQL_USERNAME=root` in your `.env` file

**Solution**: 
1. Change `MYSQL_USERNAME` to a non-root user (e.g., `resumatch_user`)
2. Restart containers: `./setup.sh restart`

### Error: "Access denied for user"
**Cause**: Wrong username or password

**Solutions**:
1. Check your `.env` file has correct credentials
2. Verify environment variables: `docker compose config | grep MYSQL`
3. Clear volumes and restart: `./setup.sh clean` then `./setup.sh start`

### Database Connection Timeout
**Cause**: Database not ready or network issues

**Solutions**:
1. Wait for MySQL to be healthy: `./setup.sh health`
2. Check MySQL logs: `./setup.sh logs mysql`
3. Verify MySQL is running: `docker compose ps`

## Testing Configuration

Test your MySQL configuration:

```bash
# Start services
./setup.sh start

# Run health check
./setup.sh health

# Test database connection
./setup.sh db
# If you can connect, configuration is correct!
```
