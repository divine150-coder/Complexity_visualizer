# Fabric MySQL Setup Script

## Overview
Automates MySQL Server installation, database creation, and SQL dump execution using Fabric.

## Prerequisites
- Python 3.x
- Fabric library
- SSH access to target server
- sudo privileges

## Installation
```bash
pip install fabric
```

## Configuration

1. **Update password.txt:**
```bash
echo "your_ssh_password" > password.txt
```

2. **Update connection details in script:**
```python
connection = Connection(
    host='127.0.0.1',  # Change to your server IP
    user='waka',        # Change to your username
    connect_kwargs={'password': password}
)
```

3. **Update database name and SQL file path:**
```python
db_name = 'hbnb_db'  # Your database name
sql_file = '/path/to/your/dump.sql'  # Your SQL dump file path
```

## Usage

### Run complete setup:
```bash
python fabric_mysql_setup.py
```

### Run individual functions:
```python
from fabric_mysql_setup import install_mysql, create_database, run_sql_dump

# Install MySQL only
install_mysql()

# Create database only
create_database()

# Run SQL dump only
run_sql_dump()
```

## Functions

### 1. install_mysql()
- Updates apt packages
- Installs MySQL Server
- Starts MySQL service
- Enables MySQL on boot

### 2. create_database()
- Creates database if not exists
- Default name: `hbnb_db`

### 3. run_sql_dump()
- Executes SQL dump file
- Imports data into specified database

### 4. setup_mysql_complete()
- Runs all functions in sequence
- Complete automated setup

## Example Output
```
Installing MySQL Server...
MySQL Server installed successfully
Creating database: hbnb_db
Database hbnb_db created successfully
Running SQL dump: /home/waka/ALU/Sessions/FabricSession/database_setup.sql
SQL dump executed successfully

MySQL setup completed successfully!
```

## Security Notes
- Keep `password.txt` secure and add to `.gitignore`
- Use SSH keys instead of passwords for production
- Restrict file permissions: `chmod 600 password.txt`

## Troubleshooting

**Connection refused:**
- Verify SSH service is running
- Check firewall settings
- Confirm correct host/port

**Permission denied:**
- Verify sudo privileges
- Check password is correct
- Ensure user has MySQL access

**SQL dump fails:**
- Verify file path is correct
- Check SQL syntax in dump file
- Ensure database exists before import

