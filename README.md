# Softwarica Booking System

This is my college project - a desktop hotel booking app I made using Python and Tkinter. It's like a mini version of Booking.com where users can search for hotels and make reservations, while admins can manage everything.

## Project Details

**Name:** Softwarica Booking System  
**Tech Stack:** Python 3.10+, Tkinter (for GUI), SQLite (database), bcrypt (password security)  
**Made For:** SEM 1 College Assignment

## What It Does

### For Regular Users

- Sign up and login to your account
- Browse hotels with ratings and see what amenities they have
- Search for hotels by city/location
- Book rooms by picking check-in and check-out dates
- See your booking history and cancel if needed
- App calculates the total cost based on how many nights you're staying

### For Admins

- Dashboard showing total users, hotels, rooms, bookings and revenue
- Add, edit, or delete hotels
- Manage rooms for each hotel (add/edit/delete, mark as available or not)
- See all registered users
- View all bookings and update their status
- Track total earnings from confirmed bookings

## 🗄️ Database Schema

### Tables

**users**

- id (PRIMARY KEY)
- name, email, password_hash
- role (user/admin)
- created_at

**hotels**

- id (PRIMARY KEY)
- name, location, description
- rating (1-5), amenities
- active_status

**rooms**

- id (PRIMARY KEY)
- hotel_id (FOREIGN KEY → hotels.id)
- room_type (Single/Double/Deluxe/Suite)
- price, capacity, facilities
- availability

**bookings**

- id (PRIMARY KEY)
- user_id (FOREIGN KEY → users.id)
- room_id (FOREIGN KEY → rooms.id)
- check_in, check_out, total_price
- status (Pending/Confirmed/Cancelled)

## 📁 Project Structure

```
softwarica_booking_app/
│
├── main.py              # Application entry point
├── database.py          # Database initialization and connection
├── models.py            # Data models and CRUD operations
├── utils.py             # Utility functions (hashing, validation, formatting)
├── auth.py              # Login and registration windows
├── user.py              # User dashboard and features
├── admin.py             # Admin dashboard and management
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── booking.db           # SQLite database (created on first run)
```

## How to Run

**Requirements** bcrypt==4.1.2

### What You Need

- Python 3.10 or newer installed on your computer
- pip should come with Python

### Installation Steps

1. First, install the required package:

```bash
pip install -r requirements.txt
```

This installs bcrypt which I use for password security.

2. Then just run:

```bash
python main.py
```

That's it! The app will create the database automatically on first run.

## Login Info

### Admin Login

- **Email:** admin@softwarica.edu
- **Password:** admin123

### Regular User

You can register a new account from the login screen.

## How to Use

### As a User

1. **Sign Up**: Click "Create New Account" button
   - Fill in your name, email, password
   - Click Register

2. **Login**: Use your email and password
   - Enter full name, email, and password
   - Click "Register" to create account

3. **Login**: Use your email and password

4. **Browse Hotels**:
   - Click "Browse Hotels" from dashboard
   - Use search bar to filter by location
   - Click "View Details" to see hotel information

5. **Book a Room**:
   - Select a hotel and view details
   - Click "Book Room" for your preferred room
   - Enter check-in and check-out dates (YYYY-MM-DD format)
   - Click "Calculate Total" to see price
   - Click "Confirm Booking"

6. **Manage Bookings**:
   - Click "My Bookings" from dashboard
   - View all your bookings
   - Cancel bookings if needed

7. **Update Profile**:
   - Click "Profile" from dashboard
   - Update name or email
   - Click "Update Profile"

### For Admins

1. **Login**: Use admin credentials

2. **View Dashboard**:
   - See real-time statistics
   - Total users, hotels, rooms, bookings
   - Estimated revenue

3. **Manage Hotels**:
   - Add new hotels with details
   - Edit existing hotels
   - Delete hotels (cascades to rooms)
   - Toggle active status

4. **Manage Rooms**:
   - Select hotel from dropdown
   - Add rooms with type, price, capacity
   - Edit room details
   - Delete rooms
   - Toggle availability

5. **View Users**:
   - See all registered users
   - View user details and roles

6. **Manage Bookings**:
   - View all bookings
   - Filter by status
   - Change booking status (Pending/Confirmed/Cancelled)

## How I Built It

### Code Organization

- **models.py**: All the database stuff (CRUD operations)
- **auth.py, user.py, admin.py**: The GUI windows
- **main.py**: Starts everything up
- **utils.py**: Helper functions I use everywhere
- **database.py**: Sets up the SQLite database

### Security Features

- Passwords are hashed with bcrypt (not storing plain text!)
- Using parameterized queries to prevent SQL injection
- Email and date validation on all inputs

## UI Design

I tried to make the UI look modern and clean. Here's what I did:

### Colors

- **Main Color**: `#667eea` (purple-blue) - used for primary buttons
- **Success**: `#48bb78` (green) - for positive actions
- **Danger**: `#f56565` (red) - for delete buttons
- **Background**: `#f7fafc` (light gray)
- **Text**: Dark gray for good readability

### Font

Using Segoe UI because it looks clean and comes with Windows

### Design Style

- Card-style layouts (those white boxes with subtle shadows)
- Buttons change color when you hover over them
- Nice spacing so it's not cramped
- Input fields highlight when you click them

## Testing

I tested these main things:

**Login/Register:**

- New user signup works
- Login with right password works
- Wrong password shows error
- Can't register same email twice

**Booking:**

- Can browse and search hotels
- Can book rooms with valid dates
- Can't book past dates (shows error)
- Can't double-book same room
- Can cancel bookings

**Admin:**

- Can add/edit/delete hotels
- Adding rooms works
- Deleting hotel removes its rooms too (cascade)
- Dashboard shows correct counts

## 📄 License

This is a college project for educational purposes.

## 🤝 Acknowledgments

Special thanks to:

- **Softwarica College of IT & E-Commerce** - For project guidance and support
- **Project Supervisor** - For valuable feedback and technical direction
- **Python Community** - For comprehensive Tkinter and SQLite documentation
- **bcrypt Contributors** - For providing robust password hashing library

**Project Completed:** ✅  
**Status:** Production Ready  
**Version:** 1.0  
**Academic Year:** 2026  
**Course:** Software Engineering / Database Systems
