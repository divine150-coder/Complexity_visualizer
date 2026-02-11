#!/usr/bin/env python3
"""Fabric script to install MySQL, create database, and run SQL dumps"""

import datetime
from fabric import Connection

with open('password.txt') as f:
    password = f.read().strip()

connection = Connection(
    host='127.0.0.1',
    user='waka',
    connect_kwargs={'password': password}
)

def install_mysql():
    """Install MySQL Server"""
    print("Installing MySQL Server...")
    connection.sudo('apt-get update', password=password)
    connection.sudo('apt-get install -y mysql-server', password=password)
    connection.sudo('systemctl start mysql', password=password)
    connection.sudo('systemctl enable mysql', password=password)
    print("MySQL Server installed successfully")

def create_database():
    """Create database"""
    db_name = 'hbnb_db'
    print(f"Creating database: {db_name}")
    connection.sudo(
        f'mysql -e "CREATE DATABASE IF NOT EXISTS {db_name};"',
        password=password
    )
    print(f"Database {db_name} created successfully")

def run_sql_dump():
    """Run SQL dump file"""
    sql_file = '/home/waka/ALU/Sessions/FabricSession/database_setup.sql'
    db_name = 'hbnb_db'
    print(f"Running SQL dump: {sql_file}")
    connection.sudo(
        f'mysql {db_name} < {sql_file}',
        password=password
    )
    print("SQL dump executed successfully")

def setup_mysql_complete():
    """Complete MySQL setup workflow"""
    install_mysql()
    create_database()
    run_sql_dump()
    print("\nMySQL setup completed successfully!")

if __name__ == '__main__':
    setup_mysql_complete()

