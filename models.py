"""
Data models and CRUD operations for Softwarica Booking System.
Provides database abstraction layer for users, hotels, rooms, and bookings.
"""

from database import get_connection
from utils import hash_password, verify_password
from datetime import datetime


class UserModel:
    """User authentication and management."""
    
    @staticmethod
    def create(name, email, password, role='user'):
        """
        Create a new user.
        
        Args:
            name (str): User's full name
            email (str): User's email (must be unique)
            password (str): Plain text password (will be hashed)
            role (str): 'user' or 'admin'
            
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return False, "Email already registered"
            
            # Hash password and insert
            password_hash = hash_password(password)
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (name, email, password_hash, role))
            
            conn.commit()
            return True, "User created successfully"
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
    
    @staticmethod
    def authenticate(email, password):
        """
        Authenticate user credentials.
        
        Args:
            email (str): User's email
            password (str): Plain text password
            
        Returns:
            dict or None: User data if authenticated, None otherwise
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if user and verify_password(password, user['password_hash']):
                return {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    
    @staticmethod
    def update(user_id, name, email):
        """
        Update user profile.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if new email is taken by another user
            cursor.execute("SELECT id FROM users WHERE email = ? AND id != ?", (email, user_id))
            if cursor.fetchone():
                return False, "Email already in use"
            
            cursor.execute('''
                UPDATE users SET name = ?, email = ?
                WHERE id = ?
            ''', (name, email, user_id))
            
            conn.commit()
            return True, "Profile updated successfully"
        except Exception as e:
            return False, f"Error updating profile: {str(e)}"
    
    @staticmethod
    def get_by_email(email):
        """Get user by email address."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None

    @staticmethod
    def reset_password(email, new_password):
        """
        Reset a user's password by email.

        Args:
            email (str): Registered email address
            new_password (str): New plain-text password (will be hashed)

        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if not cursor.fetchone():
                return False, "No account found with that email address"

            password_hash = hash_password(new_password)
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE email = ?",
                (password_hash, email)
            )
            conn.commit()
            return True, "Password reset successfully"
        except Exception as e:
            return False, f"Error resetting password: {str(e)}"

    @staticmethod
    def get_all():
        """Get all users."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        return cursor.fetchall()


class HotelModel:
    """Hotel management operations."""
    
    @staticmethod
    def create(name, location, description, rating, amenities, active_status=1):
        """
        Create a new hotel.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO hotels (name, location, description, rating, amenities, active_status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, location, description, rating, amenities, active_status))
            
            conn.commit()
            return True, "Hotel created successfully"
        except Exception as e:
            return False, f"Error creating hotel: {str(e)}"
    
    @staticmethod
    def get_all(active_only=False):
        """
        Get all hotels.
        
        Args:
            active_only (bool): If True, return only active hotels
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute("SELECT * FROM hotels WHERE active_status = 1 ORDER BY name")
        else:
            cursor.execute("SELECT * FROM hotels ORDER BY name")
        
        return cursor.fetchall()
    
    @staticmethod
    def get_by_id(hotel_id):
        """Get hotel by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hotels WHERE id = ?", (hotel_id,))
        return cursor.fetchone()
    
    @staticmethod
    def search_by_location(location):
        """Search hotels by location (case-insensitive)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM hotels 
            WHERE active_status = 1 AND location LIKE ?
            ORDER BY name
        ''', (f'%{location}%',))
        return cursor.fetchall()
    
    @staticmethod
    def update(hotel_id, name, location, description, rating, amenities, active_status):
        """
        Update hotel details.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE hotels 
                SET name = ?, location = ?, description = ?, rating = ?, 
                    amenities = ?, active_status = ?
                WHERE id = ?
            ''', (name, location, description, rating, amenities, active_status, hotel_id))
            
            conn.commit()
            return True, "Hotel updated successfully"
        except Exception as e:
            return False, f"Error updating hotel: {str(e)}"
    
    @staticmethod
    def delete(hotel_id):
        """
        Delete hotel (cascade deletes rooms and bookings).
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM hotels WHERE id = ?", (hotel_id,))
            conn.commit()
            return True, "Hotel deleted successfully"
        except Exception as e:
            return False, f"Error deleting hotel: {str(e)}"


class RoomModel:
    """Room management operations."""
    
    @staticmethod
    def create(hotel_id, room_type, price, capacity, facilities, availability=1):
        """
        Create a new room.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO rooms (hotel_id, room_type, price, capacity, facilities, availability)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (hotel_id, room_type, price, capacity, facilities, availability))
            
            conn.commit()
            return True, "Room created successfully"
        except Exception as e:
            return False, f"Error creating room: {str(e)}"
    
    @staticmethod
    def get_by_hotel(hotel_id, available_only=False):
        """
        Get all rooms for a specific hotel.
        
        Args:
            hotel_id (int): Hotel ID
            available_only (bool): If True, return only available rooms
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        if available_only:
            cursor.execute('''
                SELECT * FROM rooms 
                WHERE hotel_id = ? AND availability = 1
                ORDER BY room_type
            ''', (hotel_id,))
        else:
            cursor.execute('''
                SELECT * FROM rooms 
                WHERE hotel_id = ?
                ORDER BY room_type
            ''', (hotel_id,))
        
        return cursor.fetchall()
    
    @staticmethod
    def get_by_id(room_id):
        """Get room by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        return cursor.fetchone()
    
    @staticmethod
    def update(room_id, room_type, price, capacity, facilities, availability):
        """
        Update room details.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE rooms 
                SET room_type = ?, price = ?, capacity = ?, facilities = ?, availability = ?
                WHERE id = ?
            ''', (room_type, price, capacity, facilities, availability, room_id))
            
            conn.commit()
            return True, "Room updated successfully"
        except Exception as e:
            return False, f"Error updating room: {str(e)}"
    
    @staticmethod
    def update_availability(room_id, availability):
        """Toggle room availability."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("UPDATE rooms SET availability = ? WHERE id = ?", (availability, room_id))
            conn.commit()
            return True, "Room availability updated"
        except Exception as e:
            return False, f"Error updating availability: {str(e)}"
    
    @staticmethod
    def delete(room_id):
        """
        Delete room.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
            conn.commit()
            return True, "Room deleted successfully"
        except Exception as e:
            return False, f"Error deleting room: {str(e)}"
    
    @staticmethod
    def check_availability(room_id, check_in, check_out):
        """
        Check if room is available for given dates.
        Checks for overlapping bookings that are not cancelled.
        
        Returns:
            bool: True if available, False otherwise
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check room's availability status
        cursor.execute("SELECT availability FROM rooms WHERE id = ?", (room_id,))
        room = cursor.fetchone()
        if not room or room['availability'] == 0:
            return False
        
        # Check for overlapping bookings
        cursor.execute('''
            SELECT COUNT(*) as count FROM bookings 
            WHERE room_id = ? 
            AND status != 'Cancelled'
            AND (
                (check_in <= ? AND check_out > ?) OR
                (check_in < ? AND check_out >= ?) OR
                (check_in >= ? AND check_out <= ?)
            )
        ''', (room_id, check_in, check_in, check_out, check_out, check_in, check_out))
        
        result = cursor.fetchone()
        return result['count'] == 0


class BookingModel:
    """Booking management operations."""
    
    @staticmethod
    def create(user_id, room_id, check_in, check_out, total_price):
        """
        Create a new booking.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            # First check availability
            if not RoomModel.check_availability(room_id, check_in, check_out):
                return False, "Room is not available for selected dates"
            
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO bookings (user_id, room_id, check_in, check_out, total_price, status)
                VALUES (?, ?, ?, ?, ?, 'Pending')
            ''', (user_id, room_id, check_in, check_out, total_price))
            
            conn.commit()
            return True, "Booking created successfully"
        except Exception as e:
            return False, f"Error creating booking: {str(e)}"
    
    @staticmethod
    def get_user_bookings(user_id):
        """Get all bookings for a specific user with hotel and room details."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, r.room_type, r.price, h.name as hotel_name, h.location
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            JOIN hotels h ON r.hotel_id = h.id
            WHERE b.user_id = ?
            ORDER BY b.created_at DESC
        ''', (user_id,))
        
        return cursor.fetchall()
    
    @staticmethod
    def get_all():
        """Get all bookings with user, hotel, and room details."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, u.name as user_name, u.email, 
                   r.room_type, h.name as hotel_name
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN rooms r ON b.room_id = r.id
            JOIN hotels h ON r.hotel_id = h.id
            ORDER BY b.created_at DESC
        ''')
        
        return cursor.fetchall()
    
    @staticmethod
    def cancel(booking_id):
        """
        Cancel a booking.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE bookings SET status = 'Cancelled'
                WHERE id = ?
            ''', (booking_id,))
            
            conn.commit()
            return True, "Booking cancelled successfully"
        except Exception as e:
            return False, f"Error cancelling booking: {str(e)}"
    
    @staticmethod
    def update_status(booking_id, status):
        """
        Update booking status.
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
            conn.commit()
            return True, f"Booking status updated to {status}"
        except Exception as e:
            return False, f"Error updating status: {str(e)}"
    
    @staticmethod
    def calculate_revenue():
        """Calculate total revenue from confirmed bookings."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COALESCE(SUM(total_price), 0) as revenue
            FROM bookings
            WHERE status = 'Confirmed'
        ''')
        
        result = cursor.fetchone()
        return result['revenue'] if result else 0
    
    @staticmethod
    def get_statistics():
        """Get booking statistics for admin dashboard."""
        conn = get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total bookings
        cursor.execute("SELECT COUNT(*) as count FROM bookings")
        stats['total_bookings'] = cursor.fetchone()['count']
        
        # Pending bookings
        cursor.execute("SELECT COUNT(*) as count FROM bookings WHERE status = 'Pending'")
        stats['pending_bookings'] = cursor.fetchone()['count']
        
        # Confirmed bookings
        cursor.execute("SELECT COUNT(*) as count FROM bookings WHERE status = 'Confirmed'")
        stats['confirmed_bookings'] = cursor.fetchone()['count']
        
        # Total revenue
        stats['revenue'] = BookingModel.calculate_revenue()
        
        return stats
