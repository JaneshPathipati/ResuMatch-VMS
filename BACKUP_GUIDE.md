# Database Backup Guide

## Overview
The MySQL database data is now stored in a local directory (`./mysql_data`) instead of a Docker named volume. This makes it easy to back up and restore your database.

## Database Location
- **Directory**: `./mysql_data/`
- **Full Path**: `/Users/govind.varshney/code4/ResuMatch-VMS/mysql_data/`

This directory contains all MySQL database files including the `resumatch_db` database.

## Backup Methods

### Method 1: Directory Backup (Recommended for Full System Backup)
Simply copy the entire `mysql_data` directory when containers are stopped:

```bash
# Stop the containers first
./setup.sh stop

# Create a backup
cp -r mysql_data mysql_data_backup_$(date +%Y%m%d_%H%M%S)

# Or compress it
tar -czf mysql_data_backup_$(date +%Y%m%d_%H%M%S).tar.gz mysql_data/

# Restart containers
./setup.sh start
```

### Method 2: SQL Dump (Recommended for Database Export)
Use the built-in backup command while containers are running:

```bash
# Creates a timestamped SQL dump file
./setup.sh backup
```

This creates a file like `backup_20251114_123456.sql` that you can restore to any MySQL instance.

### Method 3: Manual SQL Dump
```bash
docker-compose exec -T mysql mysqldump -u resumatch_user -p resumatch_db > backup.sql
# Enter password when prompted
```

## Restore Methods

### Restore from Directory Backup
```bash
# Stop containers
./setup.sh stop

# Remove current data
rm -rf mysql_data/

# Restore from backup
cp -r mysql_data_backup_YYYYMMDD_HHMMSS mysql_data/

# Or extract from compressed backup
tar -xzf mysql_data_backup_YYYYMMDD_HHMMSS.tar.gz

# Start containers
./setup.sh start
```

### Restore from SQL Dump
```bash
# Make sure containers are running
./setup.sh start

# Restore from SQL file
docker-compose exec -T mysql mysql -u resumatch_user -p resumatch_db < backup.sql
# Enter password when prompted
```

## Automated Backup Script

Create a backup script for regular backups:

```bash
#!/bin/bash
# backup_db.sh

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# SQL dump backup
./setup.sh backup
mv backup_*.sql $BACKUP_DIR/

# Directory backup (optional)
tar -czf $BACKUP_DIR/mysql_data_$TIMESTAMP.tar.gz mysql_data/

echo "Backup completed: $BACKUP_DIR/mysql_data_$TIMESTAMP.tar.gz"
```

Make it executable:
```bash
chmod +x backup_db.sh
```

Run it:
```bash
./backup_db.sh
```

## Backup Schedule Recommendations

- **Daily**: SQL dumps (lightweight, version-controlled)
- **Weekly**: Full directory backups (complete system state)
- **Before Updates**: Always backup before system updates or migrations

## Important Notes

1. **The `mysql_data/` directory is ignored by git** (added to `.gitignore`)
2. **Always stop containers before copying the directory** to ensure data consistency
3. **SQL dumps can be made while containers are running**
4. **Keep backups in a separate location** (external drive, cloud storage, etc.)
5. **Test your restore process** periodically to ensure backups are valid

## Cloud Backup Options

### To AWS S3
```bash
aws s3 cp mysql_data_backup.tar.gz s3://your-bucket/backups/
```

### To Google Cloud Storage
```bash
gsutil cp mysql_data_backup.tar.gz gs://your-bucket/backups/
```

### Using rsync to Remote Server
```bash
rsync -avz mysql_data/ user@remote-server:/backup/path/
```
