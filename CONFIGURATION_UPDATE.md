# Configuration Update - External URL Support

## Summary
Updated the application to use configurable host and base URL instead of hardcoded `http://localhost` references.

## Changes Made

### 1. Configuration (`config.py`)
Added new configuration variables:
- `APP_HOST`: The hostname where the application is accessible (default: `localhost`)
- `APP_BASE_URL`: The full base URL of the application (default: auto-constructed from APP_HOST and PORT)

### 2. Environment Variables (`.env.example`)
Added new optional environment variables:
```bash
# Application Configuration
PORT=5000
APP_HOST=localhost
# APP_BASE_URL is auto-constructed from APP_HOST and PORT if not provided
# APP_BASE_URL=http://localhost:5000
```

### 3. Updated Files

#### `healthcheck.py`
- Updated `check_flask_app()` to use `config.APP_BASE_URL` instead of hardcoded `http://localhost:{port}`
- Updated `check_detailed_health()` to use `config.APP_BASE_URL` instead of hardcoded `http://localhost:{port}`

#### `app.py`
- Updated startup message to use `config.APP_BASE_URL` instead of hardcoded `http://localhost:{config.PORT}`

## Usage

### Default Behavior (No changes needed)
If you don't set these variables, the application will work as before with `http://localhost:5000`

### Custom Domain/Host
To use a custom domain or hostname, add to your `.env` file:
```bash
APP_HOST=your-domain.com
PORT=5000
```
The APP_BASE_URL will be auto-constructed as `http://your-domain.com:5000`

### Custom Base URL (Advanced)
For complex scenarios (e.g., behind a proxy, custom protocol, or path prefix):
```bash
APP_BASE_URL=https://your-domain.com/api
```
This will override the auto-constructed URL.

## Docker Considerations

The Docker healthcheck commands in `Dockerfile` and `docker-compose.yml` still use `http://localhost` because:
1. They run **inside** the container
2. They need to check the local container's health
3. The container always listens on `0.0.0.0` internally

This is the correct behavior and should not be changed.

## Testing

Run the health check script to verify:
```bash
python healthcheck.py
```

The script will now use the configured APP_BASE_URL to check the application's health.

## Migration Notes

- **No breaking changes**: Existing deployments will continue to work without any .env changes
- **Backward compatible**: Default values maintain the original behavior
- **Optional configuration**: Only add these variables if you need custom domain support
