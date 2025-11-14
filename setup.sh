#!/bin/bash

# ResuMatch-VMS Docker Setup Script
# ===================================
# This script helps you manage Docker containers for ResuMatch VMS

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project name
PROJECT_NAME="ResuMatch-VMS"

# Load PORT from .env file if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep PORT | xargs)
fi
APP_PORT=${PORT:-8080}

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found!"
        if [ -f .env.example ]; then
            print_info "Creating .env from .env.example..."
            cp .env.example .env
            print_warning "Please edit .env file with your actual credentials before running the app"
        else
            print_error "No .env.example file found. Please create .env file manually."
        fi
    else
        print_success ".env file exists"
    fi
}

# Function to check if credentials.json exists
check_credentials() {
    if [ ! -f credentials.json ]; then
        print_warning "credentials.json not found!"
        if [ -f credentials.example.json ]; then
            print_info "You can copy credentials.example.json to credentials.json"
            print_info "Run: cp credentials.example.json credentials.json"
        fi
    else
        print_success "credentials.json exists"
    fi
}

# Function to build Docker images
build() {
    print_info "Building Docker images for $PROJECT_NAME..."
    check_docker
    
    docker-compose build --no-cache
    
    print_success "Docker images built successfully!"
}

# Function to initialize database if tables don't exist
init_database() {
    print_info "Checking if database tables need initialization..."
    
    # Wait for MySQL to be ready
    max_attempts=30
    attempt=0
    
    MYSQL_ROOT_PASS=${MYSQL_ROOT_PASSWORD:-Janesh@2006}
    
    while [ $attempt -lt $max_attempts ]; do
        attempt=$((attempt + 1))
        
        if docker-compose exec -T mysql mysqladmin ping -h localhost -u root -p"${MYSQL_ROOT_PASS}" 2>/dev/null | grep -q "alive"; then
            print_success "MySQL is ready"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            print_error "MySQL did not become ready in time"
            return 1
        fi
        
        echo -n "."
        sleep 2
    done
    
    # Check if volunteers table exists
    TABLE_EXISTS=$(docker-compose exec -T mysql mysql -u root -p"${MYSQL_ROOT_PASS}" -D resumatch_db -e "SHOW TABLES LIKE 'volunteers';" 2>/dev/null | grep -c "volunteers" || echo "0")
    
    if [ "$TABLE_EXISTS" = "0" ]; then
        print_info "Tables not found. Initializing database schema..."
        
        if [ -f "init.sql" ]; then
            docker-compose exec -T mysql mysql -u root -p"${MYSQL_ROOT_PASS}" < init.sql
            
            if [ $? -eq 0 ]; then
                print_success "Database initialized successfully!"
            else
                print_error "Failed to initialize database"
                return 1
            fi
        else
            print_error "init.sql file not found!"
            return 1
        fi
    else
        print_success "Database tables already exist, skipping initialization"
    fi
}

# Function to start containers
start() {
    print_info "Starting $PROJECT_NAME containers..."
    check_docker
    check_env_file
    check_credentials
    
    docker-compose up -d
    
    print_success "Containers started successfully!"
    print_info "Waiting for services to be healthy..."
    
    if wait_healthy; then
        echo ""
        print_success "All services are running and healthy!"
        echo ""
        
        # Initialize database if needed
        init_database
        
        echo ""
        print_info "Application URL: http://localhost:${APP_PORT}"
        print_info "MySQL Port: localhost:3306"
        echo ""
        print_info "Useful commands:"
        print_info "  ./setup.sh health  - Check system health"
        print_info "  ./setup.sh logs    - View application logs"
        print_info "  ./setup.sh status  - Check container status"
    else
        echo ""
        print_warning "Services started but health check timed out"
        print_info "Check logs with: ./setup.sh logs"
    fi
}

# Function to stop containers
stop() {
    print_info "Stopping $PROJECT_NAME containers..."
    
    docker-compose down
    
    print_success "Containers stopped successfully!"
}

# Function to restart containers
restart() {
    print_info "Restarting $PROJECT_NAME containers..."
    
    docker-compose restart
    
    print_success "Containers restarted successfully!"
}

# Function to view logs
logs() {
    print_info "Showing logs for $PROJECT_NAME..."
    
    if [ -z "$1" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$1"
    fi
}

# Function to check status
status() {
    print_info "Status of $PROJECT_NAME containers:"
    echo ""
    docker-compose ps
    echo ""
    
    # Check if app is responding
    if curl -s http://localhost:${APP_PORT}/api/stats > /dev/null 2>&1; then
        print_success "Application is responding at http://localhost:${APP_PORT}"
    else
        print_warning "Application is not responding at http://localhost:${APP_PORT}"
    fi
}

# Function to perform health check
health() {
    print_info "Performing health check on $PROJECT_NAME..."
    echo ""
    
    # Check if containers are running
    if ! docker-compose ps | grep -q "Up"; then
        print_error "Containers are not running. Start them with: ./setup.sh start"
        return 1
    fi
    
    # Basic health check
    print_info "Checking basic health endpoint..."
    if curl -s http://localhost:${APP_PORT}/health > /dev/null 2>&1; then
        print_success "Basic health check: PASSED"
    else
        print_error "Basic health check: FAILED"
    fi
    
    # Detailed health check
    print_info "Checking detailed health status..."
    echo ""
    
    health_response=$(curl -s http://localhost:${APP_PORT}/health/detailed 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "$health_response" | python3 -m json.tool 2>/dev/null || echo "$health_response"
        echo ""
        print_success "Detailed health check completed"
    else
        print_error "Could not retrieve detailed health information"
    fi
    
    # Run Python health check script if available
    if [ -f "healthcheck.py" ]; then
        echo ""
        print_info "Running comprehensive health check script..."
        echo ""
        docker-compose exec -T app python healthcheck.py
    fi
    
    echo ""
    print_info "MySQL Health Check:"
    # Use environment variable or default password
    MYSQL_ROOT_PASS=${MYSQL_ROOT_PASSWORD:-Janesh@2006}
    if docker-compose exec -T mysql mysqladmin ping -h localhost -u root -p"${MYSQL_ROOT_PASS}" 2>/dev/null | grep -q "alive"; then
        print_success "MySQL is alive and responding"
    else
        print_error "MySQL health check failed"
    fi
}

# Function to wait for services to be healthy
wait_healthy() {
    print_info "Waiting for services to become healthy..."
    
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        attempt=$((attempt + 1))
        
        # Check if app health endpoint responds
        if curl -s http://localhost:${APP_PORT}/health > /dev/null 2>&1; then
            print_success "Services are healthy!"
            return 0
        fi
        
        echo -n "."
        sleep 2
    done
    
    echo ""
    print_warning "Services did not become healthy within expected time"
    print_info "Check logs with: ./setup.sh logs"
    return 1
}

# Function to clean up everything
clean() {
    print_warning "This will stop containers and remove volumes (including database data)!"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        print_info "Cleaning up..."
        docker-compose down -v
        print_success "Cleanup complete!"
    else
        print_info "Cleanup cancelled"
    fi
}

# Function to rebuild and restart
rebuild() {
    print_info "Rebuilding and restarting $PROJECT_NAME..."
    
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    
    print_success "Rebuild complete!"
    print_info "Application is running at: http://localhost:${APP_PORT}"
}

# Function to execute commands in app container
exec_app() {
    print_info "Executing command in app container..."
    
    if [ -z "$1" ]; then
        docker-compose exec app bash
    else
        docker-compose exec app "$@"
    fi
}

# Function to execute commands in MySQL container
exec_db() {
    print_info "Connecting to MySQL..."
    
    docker-compose exec mysql mysql -u resumatch_user -p resumatch_db
}

# Function to backup database
backup() {
    print_info "Backing up database..."
    
    # Use environment variables or defaults
    MYSQL_USER=${MYSQL_USERNAME:-resumatch_user}
    MYSQL_PASS=${MYSQL_PASSWORD:-Janesh@2006}
    MYSQL_DB=${MYSQL_DATABASE:-resumatch_db}
    
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    docker-compose exec -T mysql mysqldump -u "${MYSQL_USER}" -p"${MYSQL_PASS}" "${MYSQL_DB}" > "$BACKUP_FILE"
    
    print_success "Database backed up to: $BACKUP_FILE"
}

# Function to show help
help() {
    echo ""
    echo "======================================"
    echo "  $PROJECT_NAME - Docker Setup Script"
    echo "======================================"
    echo ""
    echo "Usage: ./setup.sh [command]"
    echo ""
    echo "Available commands:"
    echo ""
    echo "  build       - Build Docker images"
    echo "  start       - Start all containers"
    echo "  stop        - Stop all containers"
    echo "  restart     - Restart all containers"
    echo "  rebuild     - Rebuild images and restart containers"
    echo "  status      - Show status of containers"
    echo "  health      - Perform comprehensive health check"
    echo "  init-db     - Initialize database schema (if tables don't exist)"
    echo "  logs [svc]  - Show logs (optionally for specific service: app, mysql)"
    echo "  clean       - Stop containers and remove volumes (⚠️  deletes data)"
    echo "  exec        - Execute bash in app container"
    echo "  db          - Connect to MySQL database"
    echo "  backup      - Backup database to SQL file"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./setup.sh              # Build and start (default)"
    echo "  ./setup.sh build        # Build images"
    echo "  ./setup.sh start        # Start services"
    echo "  ./setup.sh health       # Check system health"
    echo "  ./setup.sh init-db      # Initialize database schema"
    echo "  ./setup.sh logs app     # View app logs"
    echo "  ./setup.sh exec         # Open bash in app container"
    echo "  ./setup.sh status       # Check container status"
    echo ""
}

# Main script logic
case "$1" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    rebuild)
        rebuild
        ;;
    logs)
        logs "$2"
        ;;
    status)
        status
        ;;
    health)
        health
        ;;
    init-db)
        init_database
        ;;
    clean)
        clean
        ;;
    exec)
        shift
        exec_app "$@"
        ;;
    db)
        exec_db
        ;;
    backup)
        backup
        ;;
    help|--help|-h)
        help
        ;;
    *)
        if [ -z "$1" ]; then
            # Default behavior: build and start
            print_info "No command specified. Building and starting services..."
            echo ""
            build
            echo ""
            start
        else
            print_error "Unknown command: $1"
            echo ""
            help
            exit 1
        fi
        ;;
esac
