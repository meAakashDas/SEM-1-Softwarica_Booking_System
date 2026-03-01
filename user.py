"""
User dashboard and customer-facing features for Softwarica Booking System.
Handles hotel browsing, booking creation, and profile management.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from models import HotelModel, RoomModel, BookingModel, UserModel
from utils import center_window, format_currency, validate_date_range, calculate_nights
import auth


class UserDashboard:
    """Main user dashboard window."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Softwarica Booking System - User Dashboard")
        self.root.configure(bg='#ECF0F1')
        center_window(self.root, 600, 450)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.root, bg='#2C3E50', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=f"Welcome, {auth.current_user['name']}!",
            font=('Arial', 20, 'bold'),
            bg='#2C3E50',
            fg='white'
        )
        title_label.pack(pady=30)
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#ECF0F1')
        content_frame.pack(pady=40, padx=50, fill=tk.BOTH, expand=True)
        
        # Navigation buttons
        buttons = [
            ("Browse Hotels", self.open_browse_hotels, '#3498DB'),
            ("My Bookings", self.open_my_bookings, '#9B59B6'),
            ("Profile", self.open_profile, '#16A085'),
            ("Logout", self.handle_logout, '#E74C3C')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                content_frame,
                text=text,
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white',
                width=20,
                height=2,
                cursor='hand2',
                command=command
            )
            btn.pack(pady=10)
    
    def open_browse_hotels(self):
        """Open browse hotels window."""
        browse_win = tk.Toplevel(self.root)
        BrowseHotelsWindow(browse_win)
    
    def open_my_bookings(self):
        """Open my bookings window."""
        bookings_win = tk.Toplevel(self.root)
        MyBookingsWindow(bookings_win)
    
    def open_profile(self):
        """Open profile window."""
        profile_win = tk.Toplevel(self.root)
        ProfileWindow(profile_win)
    
    def handle_logout(self):
        """Handle logout."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            auth.current_user = None
            self.root.destroy()
            
            # Return to login
            root = tk.Tk()
            auth.LoginWindow(root)
            root.mainloop()
    
    def on_close(self):
        """Handle window close."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


class BrowseHotelsWindow:
    """Window for browsing and searching hotels."""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Browse Hotels")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 900, 600)
        
        self.create_widgets()
        self.load_hotels()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#3498DB')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="Browse Hotels",
            font=('Arial', 16, 'bold'),
            bg='#3498DB',
            fg='white'
        ).pack(pady=15)
        
        # Search frame
        search_frame = tk.Frame(self.window, bg='#ECF0F1')
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            search_frame,
            text="Search by Location:",
            font=('Arial', 11),
            bg='#ECF0F1'
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 11), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=('Arial', 10, 'bold'),
            bg='#3498DB',
            fg='white',
            cursor='hand2',
            command=self.search_hotels
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            search_frame,
            text="Show All",
            font=('Arial', 10),
            bg='#95A5A6',
            fg='white',
            cursor='hand2',
            command=self.load_hotels
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Hotels list
        list_frame = tk.Frame(self.window, bg='#ECF0F1')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'Name', 'Location', 'Rating', 'Amenities')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Column headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Hotel Name')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Rating', text='Rating')
        self.tree.heading('Amenities', text='Amenities')
        
        # Column widths
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=250)
        self.tree.column('Location', width=150)
        self.tree.column('Rating', width=80)
        self.tree.column('Amenities', width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        view_btn = tk.Button(
            button_frame,
            text="View Details",
            font=('Arial', 11, 'bold'),
            bg='#27AE60',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.view_details
        )
        view_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 11),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def load_hotels(self):
        """Load all active hotels."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load hotels
        hotels = HotelModel.get_all(active_only=True)
        
        for hotel in hotels:
            self.tree.insert('', tk.END, values=(
                hotel['id'],
                hotel['name'],
                hotel['location'],
                f"{hotel['rating']} ⭐",
                hotel['amenities'] or 'N/A'
            ))
    
    def search_hotels(self):
        """Search hotels by location."""
        location = self.search_entry.get().strip()
        
        if not location:
            messagebox.showwarning("Warning", "Please enter a location to search")
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search hotels
        hotels = HotelModel.search_by_location(location)
        
        if not hotels:
            messagebox.showinfo("No Results", f"No hotels found in '{location}'")
            return
        
        for hotel in hotels:
            self.tree.insert('', tk.END, values=(
                hotel['id'],
                hotel['name'],
                hotel['location'],
                f"{hotel['rating']} ⭐",
                hotel['amenities'] or 'N/A'
            ))
    
    def view_details(self):
        """View selected hotel details."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a hotel")
            return
        
        item = self.tree.item(selection[0])
        hotel_id = item['values'][0]
        
        # Open hotel details window
        details_win = tk.Toplevel(self.window)
        HotelDetailsWindow(details_win, hotel_id)


class HotelDetailsWindow:
    """Window for viewing hotel details and available rooms."""
    
    def __init__(self, window, hotel_id):
        self.window = window
        self.hotel_id = hotel_id
        self.window.title("Hotel Details")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 800, 600)
        
        self.hotel = HotelModel.get_by_id(hotel_id)
        
        self.create_widgets()
        self.load_rooms()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#16A085')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text=self.hotel['name'],
            font=('Arial', 18, 'bold'),
            bg='#16A085',
            fg='white'
        ).pack(pady=15)
        
        # Hotel info
        info_frame = tk.Frame(self.window, bg='white', relief=tk.RIDGE, bd=2)
        info_frame.pack(fill=tk.X, padx=20, pady=15)
        
        info_text = f"""
Location: {self.hotel['location']}
Rating: {self.hotel['rating']} ⭐
Amenities: {self.hotel['amenities'] or 'N/A'}

Description:
{self.hotel['description'] or 'No description available'}
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 11),
            bg='white',
            fg='#2C3E50',
            justify=tk.LEFT,
            anchor='w'
        ).pack(padx=20, pady=15, fill=tk.X)
        
        # Rooms section
        tk.Label(
            self.window,
            text="Available Rooms",
            font=('Arial', 14, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        ).pack(pady=(10, 5))
        
        # Rooms list
        list_frame = tk.Frame(self.window, bg='#ECF0F1')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Type', 'Price', 'Capacity', 'Facilities')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        self.tree.heading('ID', text='Room ID')
        self.tree.heading('Type', text='Room Type')
        self.tree.heading('Price', text='Price/Night')
        self.tree.heading('Capacity', text='Capacity')
        self.tree.heading('Facilities', text='Facilities')
        
        self.tree.column('ID', width=80)
        self.tree.column('Type', width=120)
        self.tree.column('Price', width=120)
        self.tree.column('Capacity', width=100)
        self.tree.column('Facilities', width=300)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        book_btn = tk.Button(
            button_frame,
            text="Book Room",
            font=('Arial', 11, 'bold'),
            bg='#27AE60',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.book_room
        )
        book_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 11),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def load_rooms(self):
        """Load available rooms for this hotel."""
        rooms = RoomModel.get_by_hotel(self.hotel_id, available_only=True)
        
        for room in rooms:
            self.tree.insert('', tk.END, values=(
                room['id'],
                room['room_type'],
                format_currency(room['price']),
                f"{room['capacity']} persons",
                room['facilities'] or 'Standard'
            ))
    
    def book_room(self):
        """Open booking window for selected room."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a room to book")
            return
        
        item = self.tree.item(selection[0])
        room_id = item['values'][0]
        
        # Open booking window
        booking_win = tk.Toplevel(self.window)
        BookingWindow(booking_win, room_id)


class BookingWindow:
    """Window for creating a new booking."""
    
    def __init__(self, window, room_id):
        self.window = window
        self.room_id = room_id
        self.window.title("Book Room")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 500, 650)
        
        self.room = RoomModel.get_by_id(room_id)
        self.hotel = HotelModel.get_by_id(self.room['hotel_id'])
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#27AE60')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="Create Booking",
            font=('Arial', 16, 'bold'),
            bg='#27AE60',
            fg='white'
        ).pack(pady=15)
        
        # Booking details
        details_frame = tk.Frame(self.window, bg='white', relief=tk.RIDGE, bd=2)
        details_frame.pack(fill=tk.X, padx=20, pady=15)
        
        details_text = f"""
Hotel: {self.hotel['name']}
Location: {self.hotel['location']}
Room Type: {self.room['room_type']}
Price per Night: {format_currency(self.room['price'])}
Capacity: {self.room['capacity']} persons
        """
        
        tk.Label(
            details_frame,
            text=details_text,
            font=('Arial', 11),
            bg='white',
            fg='#2C3E50',
            justify=tk.LEFT
        ).pack(padx=20, pady=15)
        
        # Form frame
        form_frame = tk.Frame(self.window, bg='#ECF0F1')
        form_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Check-in date
        tk.Label(
            form_frame,
            text="Check-in Date (YYYY-MM-DD):",
            font=('Arial', 11),
            bg='#ECF0F1'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.checkin_entry = tk.Entry(form_frame, font=('Arial', 11), width=25)
        self.checkin_entry.grid(row=0, column=1, pady=10, padx=10)
        self.checkin_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Check-out date
        tk.Label(
            form_frame,
            text="Check-out Date (YYYY-MM-DD):",
            font=('Arial', 11),
            bg='#ECF0F1'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.checkout_entry = tk.Entry(form_frame, font=('Arial', 11), width=25)
        self.checkout_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Calculate button
        calc_btn = tk.Button(
            form_frame,
            text="Calculate Total",
            font=('Arial', 10),
            bg='#3498DB',
            fg='white',
            cursor='hand2',
            command=self.calculate_total
        )
        calc_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Total price label
        self.total_label = tk.Label(
            form_frame,
            text="Total: NPR 0.00",
            font=('Arial', 12, 'bold'),
            bg='#ECF0F1',
            fg='#27AE60'
        )
        self.total_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        confirm_btn = tk.Button(
            button_frame,
            text="Confirm Booking",
            font=('Arial', 11, 'bold'),
            bg='#27AE60',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.confirm_booking
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def calculate_total(self):
        """Calculate total price based on dates."""
        check_in = self.checkin_entry.get().strip()
        check_out = self.checkout_entry.get().strip()
        
        # Validate dates
        valid, msg = validate_date_range(check_in, check_out)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        # Calculate nights
        nights = calculate_nights(check_in, check_out)
        
        if nights <= 0:
            messagebox.showerror("Error", "Invalid date range")
            return
        
        # Calculate total
        total = nights * self.room['price']
        self.total_label.config(text=f"Total: {format_currency(total)} ({nights} nights)")
    
    def confirm_booking(self):
        """Create the booking."""
        check_in = self.checkin_entry.get().strip()
        check_out = self.checkout_entry.get().strip()
        
        # Validate dates
        valid, msg = validate_date_range(check_in, check_out)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        # Calculate total
        nights = calculate_nights(check_in, check_out)
        if nights <= 0:
            messagebox.showerror("Error", "Invalid date range")
            return
        
        total_price = nights * self.room['price']
        
        # Create booking
        success, message = BookingModel.create(
            auth.current_user['id'],
            self.room_id,
            check_in,
            check_out,
            total_price
        )
        
        if success:
            messagebox.showinfo("Success", f"Booking created successfully!\nTotal: {format_currency(total_price)}")
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)


class MyBookingsWindow:
    """Window for viewing user's bookings."""
    
    def __init__(self, window):
        self.window = window
        self.window.title("My Bookings")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 1000, 500)
        
        self.create_widgets()
        self.load_bookings()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#9B59B6')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="My Bookings",
            font=('Arial', 16, 'bold'),
            bg='#9B59B6',
            fg='white'
        ).pack(pady=15)
        
        # Bookings list
        list_frame = tk.Frame(self.window, bg='#ECF0F1')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        columns = ('ID', 'Hotel', 'Location', 'Room Type', 'Check-in', 'Check-out', 'Price', 'Status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column('ID', width=60)
        self.tree.column('Hotel', width=180)
        self.tree.column('Location', width=120)
        self.tree.column('Room Type', width=100)
        self.tree.column('Check-in', width=100)
        self.tree.column('Check-out', width=100)
        self.tree.column('Price', width=120)
        self.tree.column('Status', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel Booking",
            font=('Arial', 11),
            bg='#E74C3C',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.cancel_booking
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            button_frame,
            text="Refresh",
            font=('Arial', 11),
            bg='#3498DB',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.load_bookings
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 11),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def load_bookings(self):
        """Load user's bookings."""
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load bookings
        bookings = BookingModel.get_user_bookings(auth.current_user['id'])
        
        for booking in bookings:
            self.tree.insert('', tk.END, values=(
                booking['id'],
                booking['hotel_name'],
                booking['location'],
                booking['room_type'],
                booking['check_in'],
                booking['check_out'],
                format_currency(booking['total_price']),
                booking['status']
            ))
    
    def cancel_booking(self):
        """Cancel selected booking."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a booking to cancel")
            return
        
        item = self.tree.item(selection[0])
        booking_id = item['values'][0]
        status = item['values'][7]
        
        if status == 'Cancelled':
            messagebox.showinfo("Info", "This booking is already cancelled")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
            success, message = BookingModel.cancel(booking_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_bookings()
            else:
                messagebox.showerror("Error", message)


class ProfileWindow:
    """Window for viewing and editing user profile."""
    
    def __init__(self, window):
        self.window = window
        self.window.title("My Profile")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 450, 480)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#16A085')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="My Profile",
            font=('Arial', 16, 'bold'),
            bg='#16A085',
            fg='white'
        ).pack(pady=15)
        
        # Form frame
        form_frame = tk.Frame(self.window, bg='#ECF0F1')
        form_frame.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)
        
        # Name
        tk.Label(
            form_frame,
            text="Full Name:",
            font=('Arial', 11),
            bg='#ECF0F1'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.name_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.name_entry.grid(row=0, column=1, pady=10, padx=10)
        self.name_entry.insert(0, auth.current_user['name'])
        
        # Email
        tk.Label(
            form_frame,
            text="Email:",
            font=('Arial', 11),
            bg='#ECF0F1'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.email_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.email_entry.grid(row=1, column=1, pady=10, padx=10)
        self.email_entry.insert(0, auth.current_user['email'])
        
        # Role (read-only)
        tk.Label(
            form_frame,
            text="Role:",
            font=('Arial', 11),
            bg='#ECF0F1'
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        role_label = tk.Label(
            form_frame,
            text=auth.current_user['role'].capitalize(),
            font=('Arial', 11, 'bold'),
            bg='#ECF0F1',
            fg='#27AE60'
        )
        role_label.grid(row=2, column=1, sticky='w', pady=10, padx=10)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='#ECF0F1')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        update_btn = tk.Button(
            button_frame,
            text="Update Profile",
            font=('Arial', 11, 'bold'),
            bg='#27AE60',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.update_profile
        )
        update_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 11),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def update_profile(self):
        """Update user profile."""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not name or not email:
            messagebox.showerror("Error", "All fields are required")
            return
        
        from utils import validate_email
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        success, message = UserModel.update(auth.current_user['id'], name, email)
        
        if success:
            # Update session
            auth.current_user['name'] = name
            auth.current_user['email'] = email
            
            messagebox.showinfo("Success", message)
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)
