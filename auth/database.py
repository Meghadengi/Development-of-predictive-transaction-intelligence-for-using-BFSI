"""
Database module for user authentication
Handles SQLite database operations for user management
"""
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthDatabase:
    """Handle all database operations for authentication"""
    
    def __init__(self, db_path="auth/users.db"):
        """Initialize database connection"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with users table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, name, email, password):
        """
        Create a new user account
        Returns: (success: bool, message: str)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                conn.close()
                return False, "Email already registered"
            
            # Hash password and insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            
            conn.commit()
            conn.close()
            logger.info(f"User created successfully: {email}")
            return True, "Account created successfully"
        
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False, f"Error: {str(e)}"
    
    def verify_user(self, email, password):
        """
        Verify user credentials
        Returns: (success: bool, user_data: dict or None)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE email = ? AND password = ? AND is_active = 1",
                (email, hashed_password)
            )
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.now(), user[0])
                )
                conn.commit()
                
                user_data = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'created_at': user[3]
                }
                
                conn.close()
                logger.info(f"User logged in: {email}")
                return True, user_data
            else:
                conn.close()
                return False, None
        
        except Exception as e:
            logger.error(f"Error verifying user: {e}")
            return False, None
    
    def get_user_by_email(self, email):
        """Get user information by email"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, name, email, created_at, last_login FROM users WHERE email = ? AND is_active = 1",
                (email,)
            )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'created_at': user[3],
                    'last_login': user[4]
                }
            return None
        
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def update_user_profile(self, email, name):
        """Update user profile information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET name = ? WHERE email = ?",
                (name, email)
            )
            
            conn.commit()
            conn.close()
            logger.info(f"Profile updated for: {email}")
            return True, "Profile updated successfully"
        
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return False, f"Error: {str(e)}"
    
    def change_password(self, email, old_password, new_password):
        """Change user password"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verify old password
            old_hashed = self.hash_password(old_password)
            cursor.execute(
                "SELECT id FROM users WHERE email = ? AND password = ?",
                (email, old_hashed)
            )
            
            if not cursor.fetchone():
                conn.close()
                return False, "Current password is incorrect"
            
            # Update to new password
            new_hashed = self.hash_password(new_password)
            cursor.execute(
                "UPDATE users SET password = ? WHERE email = ?",
                (new_hashed, email)
            )
            
            conn.commit()
            conn.close()
            logger.info(f"Password changed for: {email}")
            return True, "Password changed successfully"
        
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return False, f"Error: {str(e)}"
    
    def get_user_count(self):
        """Get total number of registered users"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0
