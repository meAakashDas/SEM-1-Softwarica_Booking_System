"""
Admin dashboard and management features for Softwarica Booking System.
Handles hotel, room, user, and booking management with statistics dashboard.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from models import HotelModel, RoomModel, BookingModel, UserModel
from utils import center_window, format_currency
import auth


class AdminDashboard:
    """Main admin dashboard with statistics and navigation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - Softwarica Booking System")
        self.root.configure(bg='#ECF0F1')
        center_window(self.root, 700, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
        self.load_statistics()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.root, bg='#2C3E50', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Admin Dashboard",
            font=('Arial', 22, 'bold'),
            bg='#2C3E50',
            fg='white'
        )
        title_label.pack(pady=30)
        
        # Statistics panel
        stats_frame = tk.Frame(self.root, bg='#ECF0F1')
        stats_frame.pack(pady=20, padx=40, fill=tk.X)
        
        tk.Label(
            stats_frame,
            text="System Statistics",
            font=('Arial', 14, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        ).pack(pady=(0, 15))
        
        # Statistics cards
        self.stats_cards = tk.Frame(stats_frame, bg='#ECF0F1')
        self.stats_cards.pack(fill=tk.X)
        
        self.users_label = self.create_stat_card(self.stats_cards, "Total Users", "0", '#3498DB', 0)
        self.hotels_label = self.create_stat_card(self.stats_cards, "Total Hotels", "0", '#27AE60', 1)
        self.rooms_label = self.create_stat_card(self.stats_cards, "Total Rooms", "0", '#9B59B6', 2)
        self.bookings_label = self.create_stat_card(self.stats_cards, "Total Bookings", "0", '#E67E22', 3)
        self.revenue_label = self.create_stat_card(self.stats_cards, "Revenue", "NPR 0", '#E74C3C', 4)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root, bg='#ECF0F1')
        nav_frame.pack(pady=20, padx=50,  fill=tk.BOTH, expand=True)
        
        buttons = [
            ("Manage Hotels", self.open_manage_hotels, '#3498DB'),
            ("Manage Rooms", self.open_manage_rooms, '#27AE60'),
            ("Manage Users", self.open_manage_users, '#9B59B6'),
            ("View Bookings", self.open_view_bookings, '#E67E22'),
            ("Refresh Statistics", self.load_statistics, '#16A085'),
            ("Logout", self.handle_logout, '#E74C3C')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                nav_frame,
                text=text,
                font=('Arial', 11, 'bold'),
                bg=color,
                fg='white',
                width=25,
                height=1,
                cursor='hand2',
                command=command
            )
            btn.pack(pady=5)
    
    def create_stat_card(self, parent, title, value, color, column):
        """Create a statistics card."""
        card = tk.Frame(parent, bg=color, width=120, height=80)
        card.grid(row=0, column=column, padx=5, pady=5)
        card.pack_propagate(False)
        
        tk.Label(
            card,
            text=title,
            font=('Arial', 9, 'bold'),
            bg=color,
            fg='white'
        ).pack(pady=(10, 5))
        
        value_label = tk.Label(
            card,
            text=value,
            font=('Arial', 14, 'bold'),
            bg=color,
            fg='white'
        )
        value_label.pack()
        
        return value_label
    
    def load_statistics(self):
        """Load and display statistics."""
        # Count users
        users = UserModel.get_all()
        self.users_label.config(text=str(len(users)))
        
        # Count hotels
        hotels = HotelModel.get_all()
        self.hotels_label.config(text=str(len(hotels)))
        
        # Count rooms
        total_rooms = 0
        for hotel in hotels:
            rooms = RoomModel.get_by_hotel(hotel['id'])
            total_rooms += len(rooms)
        self.rooms_label.config(text=str(total_rooms))
        
        # Get booking statistics
        booking_stats = BookingModel.get_statistics()
        self.bookings_label.config(text=str(booking_stats['total_bookings']))
        self.revenue_label.config(text=format_currency(booking_stats['revenue']))
    
    def open_manage_hotels(self):
        """Open hotel management window."""
        manage_win = tk.Toplevel(self.root)
        ManageHotelsWindow(manage_win)
    
    def open_manage_rooms(self):
        """Open room management window."""
        manage_win = tk.Toplevel(self.root)
        ManageRoomsWindow(manage_win)
    
    def open_manage_users(self):
        """Open user management window."""
        manage_win = tk.Toplevel(self.root)
        ManageUsersWindow(manage_win)
    
    def open_view_bookings(self):
        """Open bookings view window."""
        bookings_win = tk.Toplevel(self.root)
        ViewBookingsWindow(bookings_win)
    
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


class ManageHotelsWindow:
    """Window for hotel CRUD operations."""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Manage Hotels")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 1000, 600)
        
        self.create_widgets()
        self.load_hotels()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#3498DB')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="Hotel Management",
            font=('Arial', 16, 'bold'),
            bg='#3498DB',
            fg='white'
        ).pack(pady=15)
        
        # Hotels list
        list_frame = tk.Frame(self.window, bg='#ECF0F1')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        columns = ('ID', 'Name', 'Location', 'Rating', 'Amenities', 'Active')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=200)
        self.tree.column('Location', width=150)
        self.tree.column('Rating', width=80)
        self.tree.column('Amenities', width=300)
        self.tree.column('Active', width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="Add Hotel",
            font=('Arial', 10, 'bold'),
            bg='#27AE60',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.add_hotel
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Edit Hotel",
            font=('Arial', 10),
            bg='#3498DB',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.edit_hotel
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Delete Hotel",
            font=('Arial', 10),
            bg='#E74C3C',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.delete_hotel
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Refresh",
            font=('Arial', 10),
            bg='#95A5A6',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.load_hotels
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 10),
            bg='#7F8C8D',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def load_hotels(self):
        """Load all hotels."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        hotels = HotelModel.get_all()
        
        for hotel in hotels:
            self.tree.insert('', tk.END, values=(
                hotel['id'],
                hotel['name'],
                hotel['location'],
                hotel['rating'],
                hotel['amenities'] or 'N/A',
                'Yes' if hotel['active_status'] else 'No'
            ))
    
    def add_hotel(self):
        """Open add hotel form."""
        form_win = tk.Toplevel(self.window)
        HotelFormWindow(form_win, self, mode='add')
    
    def edit_hotel(self):
        """Open edit hotel form."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a hotel to edit")
            return
        
        item = self.tree.item(selection[0])
        hotel_id = item['values'][0]
        
        form_win = tk.Toplevel(self.window)
        HotelFormWindow(form_win, self, mode='edit', hotel_id=hotel_id)
    
    def delete_hotel(self):
        """Delete selected hotel."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a hotel to delete")
            return
        
        item = self.tree.item(selection[0])
        hotel_id = item['values'][0]
        hotel_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete hotel '{hotel_name}'?\nThis will also delete all associated rooms and bookings."):
            success, message = HotelModel.delete(hotel_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_hotels()
            else:
                messagebox.showerror("Error", message)


class HotelFormWindow:
    """Form for adding/editing hotels."""
    
    def __init__(self, window, parent, mode='add', hotel_id=None):
        self.window = window
        self.parent = parent
        self.mode = mode
        self.hotel_id = hotel_id
        
        title = "Add New Hotel" if mode == 'add' else "Edit Hotel"
        self.window.title(title)
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 500, 650)
        
        self.hotel_data = None
        if mode == 'edit' and hotel_id:
            self.hotel_data = HotelModel.get_by_id(hotel_id)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create form widgets."""
        # Header
        color = '#27AE60' if self.mode == 'add' else '#3498DB'
        header_frame = tk.Frame(self.window, bg=color)
        header_frame.pack(fill=tk.X)
        
        title = "Add New Hotel" if self.mode == 'add' else "Edit Hotel"
        tk.Label(
            header_frame,
            text=title,
            font=('Arial', 16, 'bold'),
            bg=color,
            fg='white'
        ).pack(pady=15)
        
        # Form
        form_frame = tk.Frame(self.window, bg='#ECF0F1')
        form_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Name
        tk.Label(form_frame, text="Hotel Name:", font=('Arial', 11), bg='#ECF0F1').grid(row=0, column=0, sticky='w', pady=8)
        self.name_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.name_entry.grid(row=0, column=1, pady=8, padx=10)
        
        # Location
        tk.Label(form_frame, text="Location:", font=('Arial', 11), bg='#ECF0F1').grid(row=1, column=0, sticky='w', pady=8)
        self.location_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.location_entry.grid(row=1, column=1, pady=8, padx=10)
        
        # Description
        tk.Label(form_frame, text="Description:", font=('Arial', 11), bg='#ECF0F1').grid(row=2, column=0, sticky='nw', pady=8)
        self.description_text = tk.Text(form_frame, font=('Arial', 10), width=30, height=4)
        self.description_text.grid(row=2, column=1, pady=8, padx=10)
        
        # Rating
        tk.Label(form_frame, text="Rating (1-5):", font=('Arial', 11), bg='#ECF0F1').grid(row=3, column=0, sticky='w', pady=8)
        self.rating_var = tk.DoubleVar(value=5.0)
        rating_spinbox = tk.Spinbox(form_frame, from_=1.0, to=5.0, increment=0.5, textvariable=self.rating_var, font=('Arial', 11), width=28)
        rating_spinbox.grid(row=3, column=1, pady=8, padx=10)
        
        # Amenities
        tk.Label(form_frame, text="Amenities:", font=('Arial', 11), bg='#ECF0F1').grid(row=4, column=0, sticky='w', pady=8)
        self.amenities_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.amenities_entry.grid(row=4, column=1, pady=8, padx=10)
        tk.Label(form_frame, text="(comma separated)", font=('Arial', 9), bg='#ECF0F1', fg='gray').grid(row=5, column=1, sticky='w', padx=10)
        
        # Active status
        tk.Label(form_frame, text="Active Status:", font=('Arial', 11), bg='#ECF0F1').grid(row=6, column=0, sticky='w', pady=8)
        self.active_var = tk.IntVar(value=1)
        tk.Checkbutton(form_frame, text="Active", variable=self.active_var, font=('Arial', 11), bg='#ECF0F1').grid(row=6, column=1, sticky='w', padx=10)
        
        # Load existing data if editing
        if self.mode == 'edit' and self.hotel_data:
            self.name_entry.insert(0, self.hotel_data['name'])
            self.location_entry.insert(0, self.hotel_data['location'])
            self.description_text.insert('1.0', self.hotel_data['description'] or '')
            self.rating_var.set(self.hotel_data['rating'])
            self.amenities_entry.insert(0, self.hotel_data['amenities'] or '')
            self.active_var.set(self.hotel_data['active_status'])
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(pady=15)
        
        save_text = "Create Hotel" if self.mode == 'add' else "Update Hotel"
        tk.Button(
            button_frame,
            text=save_text,
            font=('Arial', 11, 'bold'),
            bg=color,
            fg='white',
            width=15,
            cursor='hand2',
            command=self.save_hotel
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def save_hotel(self):
        """Save hotel (create or update)."""
        name = self.name_entry.get().strip()
        location = self.location_entry.get().strip()
        description = self.description_text.get('1.0', tk.END).strip()
        rating = self.rating_var.get()
        amenities = self.amenities_entry.get().strip()
        active_status = self.active_var.get()
        
        if not name or not location:
            messagebox.showerror("Error", "Name and location are required")
            return
        
        if rating < 1 or rating > 5:
            messagebox.showerror("Error", "Rating must be between 1 and 5")
            return
        
        if self.mode == 'add':
            success, message = HotelModel.create(name, location, description, rating, amenities, active_status)
        else:
            success, message = HotelModel.update(self.hotel_id, name, location, description, rating, amenities, active_status)
        
        if success:
            messagebox.showinfo("Success", message)
            self.parent.load_hotels()
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)


class ManageRoomsWindow:
    """Window for room CRUD operations."""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Manage Rooms")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 1000, 600)
        
        self.current_hotel_id = None
        self.create_widgets()
        self.load_hotels()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#27AE60')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="Room Management",
            font=('Arial', 16, 'bold'),
            bg='#27AE60',
            fg='white'
        ).pack(pady=15)
        
        # Hotel selector
        selector_frame = tk.Frame(self.window, bg='#ECF0F1')
        selector_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            selector_frame,
            text="Select Hotel:",
            font=('Arial', 11, 'bold'),
            bg='#ECF0F1'
        ).pack(side=tk.LEFT, padx=5)
        
        self.hotel_var = tk.StringVar()
        self.hotel_dropdown = ttk.Combobox(selector_frame, textvariable=self.hotel_var, state='readonly', font=('Arial', 11), width=40)
        self.hotel_dropdown.pack(side=tk.LEFT, padx=5)
        self.hotel_dropdown.bind('<<ComboboxSelected>>', self.on_hotel_selected)
        
        # Rooms list
        list_frame = tk.Frame(self.window, bg='#ECF0F1')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Room Type', 'Price', 'Capacity', 'Facilities', 'Available')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column('ID', width=60)
        self.tree.column('Room Type', width=120)
        self.tree.column('Price', width=120)
        self.tree.column('Capacity', width=100)
        self.tree.column('Facilities', width=300)
        self.tree.column('Available', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="Add Room",
            font=('Arial', 10, 'bold'),
            bg='#27AE60',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.add_room
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Edit Room",
            font=('Arial', 10),
            bg='#3498DB',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.edit_room
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Delete Room",
            font=('Arial', 10),
            bg='#E74C3C',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.delete_room
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Toggle Availability",
            font=('Arial', 10),
            bg='#E67E22',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.toggle_availability
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 10),
            bg='#95A5A6',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def load_hotels(self):
        """Load hotels into dropdown."""
        hotels = HotelModel.get_all()
        hotel_list = [f"{h['id']} - {h['name']}" for h in hotels]
        self.hotel_dropdown['values'] = hotel_list
        
        if hotel_list:
            self.hotel_dropdown.current(0)
            self.on_hotel_selected(None)
    
    def on_hotel_selected(self, event):
        """Handle hotel selection."""
        selected = self.hotel_var.get()
        if selected:
            self.current_hotel_id = int(selected.split(' - ')[0])
            self.load_rooms()
    
    def load_rooms(self):
        """Load rooms for selected hotel."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.current_hotel_id:
            return
        
        rooms = RoomModel.get_by_hotel(self.current_hotel_id)
        
        for room in rooms:
            self.tree.insert('', tk.END, values=(
                room['id'],
                room['room_type'],
                format_currency(room['price']),
                f"{room['capacity']} persons",
                room['facilities'] or 'Standard',
                'Yes' if room['availability'] else 'No'
            ))
    
    def add_room(self):
        """Open add room form."""
        if not self.current_hotel_id:
            messagebox.showwarning("Warning", "Please select a hotel first")
            return
        
        form_win = tk.Toplevel(self.window)
        RoomFormWindow(form_win, self, mode='add', hotel_id=self.current_hotel_id)
    
    def edit_room(self):
        """Open edit room form."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a room to edit")
            return
        
        item = self.tree.item(selection[0])
        room_id = item['values'][0]
        
        form_win = tk.Toplevel(self.window)
        RoomFormWindow(form_win, self, mode='edit', room_id=room_id)
    
    def delete_room(self):
        """Delete selected room."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a room to delete")
            return
        
        item = self.tree.item(selection[0])
        room_id = item['values'][0]
        room_type = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete {room_type} room?"):
            success, message = RoomModel.delete(room_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_rooms()
            else:
                messagebox.showerror("Error", message)
    
    def toggle_availability(self):
        """Toggle room availability."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a room")
            return
        
        item = self.tree.item(selection[0])
        room_id = item['values'][0]
        current_status = 0 if item['values'][5] == 'Yes' else 1
        
        success, message = RoomModel.update_availability(room_id, current_status)
        
        if success:
            messagebox.showinfo("Success", message)
            self.load_rooms()
        else:
            messagebox.showerror("Error", message)


class RoomFormWindow:
    """Form for adding/editing rooms."""
    
    def __init__(self, window, parent, mode='add', hotel_id=None, room_id=None):
        self.window = window
        self.parent = parent
        self.mode = mode
        self.hotel_id = hotel_id
        self.room_id = room_id
        
        title = "Add New Room" if mode == 'add' else "Edit Room"
        self.window.title(title)
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 450, 550)
        
        self.room_data = None
        if mode == 'edit' and room_id:
            self.room_data = RoomModel.get_by_id(room_id)
            self.hotel_id = self.room_data['hotel_id']
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create form widgets."""
        # Header
        color = '#27AE60' if self.mode == 'add' else '#3498DB'
        header_frame = tk.Frame(self.window, bg=color)
        header_frame.pack(fill=tk.X)
        
        title = "Add New Room" if self.mode == 'add' else "Edit Room"
        tk.Label(
            header_frame,
            text=title,
            font=('Arial', 16, 'bold'),
            bg=color,
            fg='white'
        ).pack(pady=15)
        
        # Form
        form_frame = tk.Frame(self.window, bg='#ECF0F1')
        form_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Room Type
        tk.Label(form_frame, text="Room Type:", font=('Arial', 11), bg='#ECF0F1').grid(row=0, column=0, sticky='w', pady=10)
        self.type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(form_frame, textvariable=self.type_var, state='readonly', font=('Arial', 11), width=28)
        type_dropdown['values'] = ('Single', 'Double', 'Deluxe', 'Suite')
        type_dropdown.grid(row=0, column=1, pady=10, padx=10)
        type_dropdown.current(0)
        
        # Price
        tk.Label(form_frame, text="Price per Night:", font=('Arial', 11), bg='#ECF0F1').grid(row=1, column=0, sticky='w', pady=10)
        self.price_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.price_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Capacity
        tk.Label(form_frame, text="Capacity (persons):", font=('Arial', 11), bg='#ECF0F1').grid(row=2, column=0, sticky='w', pady=10)
        self.capacity_spinbox = tk.Spinbox(form_frame, from_=1, to=10, font=('Arial', 11), width=28)
        self.capacity_spinbox.grid(row=2, column=1, pady=10, padx=10)
        
        # Facilities
        tk.Label(form_frame, text="Facilities:", font=('Arial', 11), bg='#ECF0F1').grid(row=3, column=0, sticky='w', pady=10)
        self.facilities_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.facilities_entry.grid(row=3, column=1, pady=10, padx=10)
        
        # Availability
        tk.Label(form_frame, text="Availability:", font=('Arial', 11), bg='#ECF0F1').grid(row=4, column=0, sticky='w', pady=10)
        self.avail_var = tk.IntVar(value=1)
        tk.Checkbutton(form_frame, text="Available", variable=self.avail_var, font=('Arial', 11), bg='#ECF0F1').grid(row=4, column=1, sticky='w', padx=10)
        
        # Load existing data if editing
        if self.mode == 'edit' and self.room_data:
            self.type_var.set(self.room_data['room_type'])
            self.price_entry.insert(0, str(self.room_data['price']))
            self.capacity_spinbox.delete(0, tk.END)
            self.capacity_spinbox.insert(0, str(self.room_data['capacity']))
            self.facilities_entry.insert(0, self.room_data['facilities'] or '')
            self.avail_var.set(self.room_data['availability'])
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(pady=15)
        
        save_text = "Create Room" if self.mode == 'add' else "Update Room"
        tk.Button(
            button_frame,
            text=save_text,
            font=('Arial', 11, 'bold'),
            bg=color,
            fg='white',
            width=15,
            cursor='hand2',
            command=self.save_room
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def save_room(self):
        """Save room (create or update)."""
        room_type = self.type_var.get()
        price_str = self.price_entry.get().strip()
        capacity_str = self.capacity_spinbox.get()
        facilities = self.facilities_entry.get().strip()
        availability = self.avail_var.get()
        
        if not room_type or not price_str or not capacity_str:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            price = float(price_str)
            capacity = int(capacity_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or capacity")
            return
        
        if price <= 0:
            messagebox.showerror("Error", "Price must be greater than 0")
            return
        
        if self.mode == 'add':
            success, message = RoomModel.create(self.hotel_id, room_type, price, capacity, facilities, availability)
        else:
            success, message = RoomModel.update(self.room_id, room_type, price, capacity, facilities, availability)
        
        if success:
            messagebox.showinfo("Success", message)
            self.parent.load_rooms()
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)


class ManageUsersWindow:
    """Window for viewing users."""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Manage Users")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 900, 500)
        
        self.create_widgets()
        self.load_users()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#9B59B6')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="User Management",
            font=('Arial', 16, 'bold'),
            bg='#9B59B6',
            fg='white'
        ).pack(pady=15)
        
        # Users list
        list_frame = tk.Frame(self.window, bg='#ECF0F1')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        columns = ('ID', 'Name', 'Email', 'Role', 'Created At')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column('ID', width=60)
        self.tree.column('Name', width=200)
        self.tree.column('Email', width=250)
        self.tree.column('Role', width=100)
        self.tree.column('Created At', width=180)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="Refresh",
            font=('Arial', 10),
            bg='#3498DB',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.load_users
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 10),
            bg='#95A5A6',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def load_users(self):
        """Load all users."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        users = UserModel.get_all()
        
        for user in users:
            self.tree.insert('', tk.END, values=(
                user['id'],
                user['name'],
                user['email'],
                user['role'].capitalize(),
                user['created_at']
            ))


class ViewBookingsWindow:
    """Window for viewing and managing all bookings."""
    
    def __init__(self, window):
        self.window = window
        self.window.title("View Bookings")
        self.window.configure(bg='#ECF0F1')
        center_window(self.window, 1100, 600)
        
        self.create_widgets()
        self.load_bookings()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg='#E67E22')
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="Booking Management",
            font=('Arial', 16, 'bold'),
            bg='#E67E22',
            fg='white'
        ).pack(pady=15)
        
        # Filter frame
        filter_frame = tk.Frame(self.window, bg='#ECF0F1')
        filter_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            filter_frame,
            text="Filter by Status:",
            font=('Arial', 11),
            bg='#ECF0F1'
        ).pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar(value='All')
        status_dropdown = ttk.Combobox(filter_frame, textvariable=self.status_var, state='readonly', font=('Arial', 11), width=15)
        status_dropdown['values'] = ('All', 'Pending', 'Confirmed', 'Cancelled')
        status_dropdown.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            filter_frame,
            text="Apply Filter",
            font=('Arial', 10),
            bg='#3498DB',
            fg='white',
            cursor='hand2',
            command=self.load_bookings
        ).pack(side=tk.LEFT, padx=5)
        
        # Bookings list
        list_frame = tk.Frame(self.window, bg='#ECF0F1')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'User', 'Email', 'Hotel', 'Room Type', 'Check-in', 'Check-out', 'Price', 'Status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=13)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column('ID', width=50)
        self.tree.column('User', width=130)
        self.tree.column('Email', width=180)
        self.tree.column('Hotel', width=150)
        self.tree.column('Room Type', width=100)
        self.tree.column('Check-in', width=90)
        self.tree.column('Check-out', width=90)
        self.tree.column('Price', width=100)
        self.tree.column('Status', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#ECF0F1')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="Change Status",
            font=('Arial', 10),
            bg='#3498DB',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.change_status
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Refresh",
            font=('Arial', 10),
            bg='#27AE60',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.load_bookings
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 10),
            bg='#95A5A6',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def load_bookings(self):
        """Load bookings based on filter."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        bookings = BookingModel.get_all()
        status_filter = self.status_var.get()
        
        for booking in bookings:
            if status_filter != 'All' and booking['status'] != status_filter:
                continue
            
            self.tree.insert('', tk.END, values=(
                booking['id'],
                booking['user_name'],
                booking['email'],
                booking['hotel_name'],
                booking['room_type'],
                booking['check_in'],
                booking['check_out'],
                format_currency(booking['total_price']),
                booking['status']
            ))
    
    def change_status(self):
        """Change booking status."""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a booking")
            return
        
        item = self.tree.item(selection[0])
        booking_id = item['values'][0]
        current_status = item['values'][8]
        
        # Create status selection window
        status_win = tk.Toplevel(self.window)
        status_win.title("Change Status")
        status_win.configure(bg='#ECF0F1')
        center_window(status_win, 300, 200)
        
        tk.Label(
            status_win,
            text="Select New Status:",
            font=('Arial', 12, 'bold'),
            bg='#ECF0F1'
        ).pack(pady=20)
        
        status_var = tk.StringVar(value=current_status)
        for status in ['Pending', 'Confirmed', 'Cancelled']:
            tk.Radiobutton(
                status_win,
                text=status,
                variable=status_var,
                value=status,
                font=('Arial', 11),
                bg='#ECF0F1'
            ).pack(anchor='w', padx=50)
        
        def update_status():
            new_status = status_var.get()
            success, message = BookingModel.update_status(booking_id, new_status)
            
            if success:
                messagebox.showinfo("Success", message)
                status_win.destroy()
                self.load_bookings()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            status_win,
            text="Update",
            font=('Arial', 11, 'bold'),
            bg='#3498DB',
            fg='white',
            width=15,
            cursor='hand2',
            command=update_status
        ).pack(pady=20)
