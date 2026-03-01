"""
Database initialization and connection management for Softwarica Booking System.
Handles SQLite database creation, table schema, and connection pooling.
"""

import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'booking.db')

# Global connection variable
_connection = None


def get_connection():
    """
    Get or create a SQLite database connection.
    Uses singleton pattern to ensure single connection throughout application.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    global _connection
    
    if _connection is None:
        _connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row  # Enable column access by name
        # Enable foreign key constraints
        _connection.execute('PRAGMA foreign_keys = ON')
        _connection.commit()
    
    return _connection


def init_database():
    """
    Initialize the database by creating all required tables.
    This function is idempotent - safe to call multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT CHECK(role IN ('user', 'admin')) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create hotels table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT,
            rating REAL CHECK(rating >= 1 AND rating <= 5),
            amenities TEXT,
            active_status INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create rooms table with foreign key to hotels
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            room_type TEXT CHECK(room_type IN ('Single', 'Double', 'Deluxe', 'Suite')) NOT NULL,
            price REAL NOT NULL,
            capacity INTEGER NOT NULL,
            facilities TEXT,
            availability INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
        )
    ''')
    
    # Create bookings table with foreign keys to users and rooms
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            total_price REAL NOT NULL,
            status TEXT CHECK(status IN ('Pending', 'Confirmed', 'Cancelled')) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    print("Database initialized successfully!")


def create_admin_user():
    """
    Create default admin user if not exists.
    Default credentials: admin@softwarica.edu / admin123
    """
    from utils import hash_password
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ('admin@softwarica.edu',))
    if cursor.fetchone():
        print("Admin user already exists.")
        return
    
    # Create admin user
    admin_password = hash_password('admin123')
    cursor.execute('''
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    ''', ('System Admin', 'admin@softwarica.edu', admin_password, 'admin'))
    
    conn.commit()
    print("Admin user created successfully!")
    print("Email: admin@softwarica.edu")
    print("Password: admin123")


def close_connection():
    """
    Close the database connection.
    Should be called when application exits.
    """
    global _connection
    if _connection:
        _connection.close()
        _connection = None
        print("Database connection closed.")
