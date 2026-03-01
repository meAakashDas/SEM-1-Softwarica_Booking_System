"""
Softwarica Booking System - Main Entry Point
A desktop hotel booking application using Tkinter and SQLite.

Course: Software Engineering / Database Systems
Version: 1.0
Academic Year: 2026
"""

import tkinter as tk
from tkinter import messagebox
import sys
import traceback

from database import init_database, create_admin_user, close_connection
from auth import LoginWindow


def main():
    """Main application entry point."""
    try:
        # Initialize database
        print("=" * 50)
        print("Softwarica Booking System")
        print("=" * 50)
        print("\nInitializing database...")
        init_database()
        
        # Create admin user if not exists
        print("Checking admin user...")
        create_admin_user()
        
        print("\n" + "=" * 50)
        print("Application started successfully!")
        print("=" * 50)
        print("\nDefault Admin Credentials:")
        print("Email: admin@softwarica.edu")
        print("Password: admin123")
        print("=" * 50 + "\n")
        
        # Create and run login window
        root = tk.Tk()
        LoginWindow(root)
        root.mainloop()
        
        # Cleanup
        print("\nClosing application...")
        close_connection()
        print("Database connection closed.")
        print("Thank you for using Softwarica Booking System!")
        
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred!")
        print(f"Error details: {str(e)}")
        traceback.print_exc()
        
        # Show error dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Application Error",
            f"Failed to start application:\n\n{str(e)}\n\nPlease check the console for details."
        )
        root.destroy()
        
        sys.exit(1)


if __name__ == "__main__":
    main()
