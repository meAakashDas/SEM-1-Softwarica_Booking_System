"""
Utility functions for Softwarica Booking System.
Provides password hashing, validation, date calculations, and UI helpers.
"""

import bcrypt
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk


# ============================================================================
# MODERN DESIGN SYSTEM
# ============================================================================

# Color Palette
COLORS = {
    'primary': '#667eea',
    'primary_dark': '#5568d3',
    'secondary': '#764ba2',
    'success': '#48bb78',
    'danger': '#f56565',
    'warning': '#ed8936',
    'background': '#f7fafc',
    'surface': '#ffffff',
    'text_primary': '#2d3748',
    'text_secondary': '#718096',
    'border': '#e2e8f0',
    'hover': '#f0f4f8'
}

# Typography
FONTS = {
    'heading_large': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 18, 'bold'),
    'subheading': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 11),
    'body_large': ('Segoe UI', 12),
    'small': ('Segoe UI', 10),
}

# Spacing
SPACING = {
    'xs': 5,
    'sm': 10,
    'md': 15,
    'lg': 20,
    'xl': 30
}


def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password (decoded to string for SQLite storage)
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed):
    """
    Verify a password against its hash.
    
    Args:
        password (str): Plain text password to verify
        hashed (str): Stored password hash
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def validate_email(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def calculate_nights(check_in_str, check_out_str):
    """
    Calculate number of nights between two dates.
    
    Args:
        check_in_str (str): Check-in date in YYYY-MM-DD format
        check_out_str (str): Check-out date in YYYY-MM-DD format
        
    Returns:
        int: Number of nights, or -1 if invalid
    """
    try:
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d')
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d')
        delta = check_out - check_in
        return delta.days
    except (ValueError, TypeError, AttributeError):
        return -1



def validate_date_range(check_in_str, check_out_str):
    """
    Validate that check-out is after check-in and both are in the future.
    
    Args:
        check_in_str (str): Check-in date in YYYY-MM-DD format
        check_out_str (str): Check-out date in YYYY-MM-DD format
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d')
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d')
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if check_in < today:
            return False, "Check-in date cannot be in the past"
        
        if check_out <= check_in:
            return False, "Check-out date must be after check-in date"
        
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"


def format_currency(amount):
    """
    Format amount as currency.
    
    Args:
        amount (float): Amount to format
        
    Returns:
        str: Formatted currency string
    """
    return f"NPR {amount:,.2f}"


def center_window(window, width, height):
    """
    Center a Tkinter window on the screen.
    
    Args:
        window: Tkinter window object (Tk or Toplevel)
        width (int): Window width
        height (int): Window height
    """
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set geometry
    window.geometry(f'{width}x{height}+{x}+{y}')


def validate_password_strength(password):
    """
    Validate password strength.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    return True, ""


def parse_amenities(amenities_str):
    """
    Parse amenities string into a list.
    
    Args:
        amenities_str (str): Comma-separated amenities
        
    Returns:
        list: List of amenities
    """
    if not amenities_str:
        return []
    return [a.strip() for a in amenities_str.split(',')]


def format_amenities(amenities_list):
    """
    Format amenities list into a string.
    
    Args:
        amenities_list (list): List of amenities
        
    Returns:
        str: Comma-separated amenities string
    """
    if not amenities_list:
        return ""
    return ", ".join(amenities_list)


# ============================================================================
# MODERN UI COMPONENTS
# ============================================================================

def create_styled_button(parent, text, command=None, style='primary', width=None):
    """
    Create a modern styled button.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Button command function
        style: 'primary', 'success', 'danger', 'secondary'
        width: Button width in characters
        
    Returns:
        tk.Button: Styled button widget
    """
    colors = {
        'primary': (COLORS['primary'], COLORS['primary_dark'], COLORS['surface']),
        'success': (COLORS['success'], '#38a169', COLORS['surface']),
        'danger': (COLORS['danger'], '#e53e3e', COLORS['surface']),
        'secondary': (COLORS['text_secondary'], '#4a5568', COLORS['surface'])
    }
    
    bg, active_bg, fg = colors.get(style, colors['primary'])
    
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONTS['body_large'],
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=fg,
        relief=tk.FLAT,
        cursor='hand2',
        padx=SPACING['lg'],
        pady=SPACING['sm']
    )
    
    if width:
        btn.config(width=width)
    
    # Hover effect
    def on_enter(e):
        btn['bg'] = active_bg
    
    def on_leave(e):
        btn['bg'] = bg
    
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    
    return btn


def create_styled_entry(parent, placeholder='', width=30, show=None):
    """
    Create a modern styled entry field.
    
    Args:
        parent: Parent widget
        placeholder: Placeholder text
        width: Entry width
        show: Show character (for passwords)
        
    Returns:
        tk.Entry: Styled entry widget
    """
    entry = tk.Entry(
        parent,
        font=FONTS['body_large'],
        width=width,
        relief=tk.FLAT,
        bg=COLORS['surface'],
        fg=COLORS['text_primary'],
        insertbackground=COLORS['primary'],
        highlightthickness=2,
        highlightbackground=COLORS['border'],
        highlightcolor=COLORS['primary']
    )
    
    if show:
        entry.config(show=show)
    
    return entry


def create_styled_label(parent, text, style='body'):
    """
    Create a modern styled label.
    
    Args:
        parent: Parent widget
        text: Label text
        style: 'heading_large', 'heading', 'subheading', 'body', 'small'
        
    Returns:
        tk.Label: Styled label widget
    """
    font = FONTS.get(style, FONTS['body'])
    color = COLORS['text_primary'] if 'heading' in style else COLORS['text_primary']
    
    label = tk.Label(
        parent,
        text=text,
        font=font,
        fg=color,
        bg=COLORS['surface']
    )
    
    return label


def create_card_frame(parent, padx=20, pady=20):
    """
    Create a card-style frame with modern styling.
    
    Args:
        parent: Parent widget
        padx: Horizontal padding
        pady: Vertical padding
        
    Returns:
        tk.Frame: Styled card frame
    """
    frame = tk.Frame(
        parent,
        bg=COLORS['surface'],
        relief=tk.FLAT,
        borderwidth=1,
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    
    return frame


def create_header_frame(parent, title):
    """
    Create a modern header frame with gradient-like effect.
    
    Args:
        parent: Parent widget
        title: Header title text
        
    Returns:
        tk.Frame: Header frame
    """
    header = tk.Frame(parent, bg=COLORS['primary'], height=80)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    title_label = tk.Label(
        header,
        text=title,
        font=FONTS['heading_large'],
        fg=COLORS['surface'],
        bg=COLORS['primary']
    )
    title_label.pack(expand=True)
    
    return header
