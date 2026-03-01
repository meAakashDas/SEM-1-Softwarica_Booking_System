"""
Authentication windows for Softwarica Booking System.
Provides login and registration GUI using Tkinter.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from models import UserModel
from utils import (validate_email, validate_password_strength, center_window,
                   create_styled_button, create_styled_entry, create_styled_label,
                   create_header_frame, COLORS, FONTS, SPACING)


# Global session variable
current_user = None


class LoginWindow:
    """Login window for user authentication."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Softwarica Booking System - Login")
        self.root.configure(bg=COLORS['background'])
        center_window(self.root, 500, 720)
        self.root.resizable(False, False)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        create_header_frame(self.root, "Softwarica Booking System")
        
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['xl'])
        
        # Card frame
        card = tk.Frame(
            main_frame,
            bg=COLORS['surface'],
            relief=tk.FLAT,
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True)
        
        # Form container
        form_frame = tk.Frame(card, bg=COLORS['surface'])
        form_frame.pack(padx=SPACING['xl'], pady=SPACING['xl'])
        
        # Login title
        title = create_styled_label(form_frame, "Login to Your Account", 'heading')
        title.pack(pady=(0, SPACING['xl']))
        
        # Email field
        email_label = create_styled_label(form_frame, "Email Address", 'body')
        email_label.pack(anchor='w', pady=(SPACING['md'], SPACING['xs']))
        
        self.email_entry = create_styled_entry(form_frame, width=35)
        self.email_entry.pack(pady=(0, SPACING['md']), ipady=SPACING['xs'])
        
        # Password field
        password_label = create_styled_label(form_frame, "Password", 'body')
        password_label.pack(anchor='w', pady=(SPACING['md'], SPACING['xs']))
        
        self.password_entry = create_styled_entry(form_frame, width=35, show='●')
        self.password_entry.pack(pady=(0, SPACING['lg']), ipady=SPACING['xs'])
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        button_frame.pack(pady=SPACING['md'])
        
        # Login button
        login_btn = create_styled_button(
            button_frame,
            "Login",
            command=self.handle_login,
            style='primary',
            width=15
        )
        login_btn.pack(pady=SPACING['xs'])

        # Forgot password link
        forgot_btn = tk.Label(
            form_frame,
            text="Forgot Password?",
            font=FONTS['small'],
            bg=COLORS['surface'],
            fg=COLORS['primary'],
            cursor='hand2'
        )
        forgot_btn.pack(pady=(SPACING['xs'], 0))
        forgot_btn.bind('<Button-1>', lambda e: self.open_forgot_password())
        
        # Divider
        divider_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        divider_frame.pack(fill=tk.X, pady=SPACING['md'])
        
        tk.Frame(divider_frame, bg=COLORS['border'], height=1).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(
            divider_frame,
            text=" OR ",
            font=FONTS['small'],
            bg=COLORS['surface'],
            fg=COLORS['text_secondary']
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
        tk.Frame(divider_frame, bg=COLORS['border'], height=1).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Register button
        register_btn = create_styled_button(
            form_frame,
            "Create New Account",
            command=self.open_register,
            style='secondary',
            width=15
        )
        register_btn.pack(pady=SPACING['xs'])
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.handle_login())

    
    def handle_login(self):
        """Handle login button click."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Validation
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        # Authenticate
        user = UserModel.authenticate(email, password)
        
        if user:
            global current_user
            current_user = user
            
            messagebox.showinfo("Success", f"Welcome, {user['name']}!")
            
            # Close login window and open appropriate dashboard
            self.root.destroy()
            
            if user['role'] == 'admin':
                self.open_admin_dashboard()
            else:
                self.open_user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password")
    
    def open_register(self):
        """Open registration window."""
        register_win = tk.Toplevel(self.root)
        RegistrationWindow(register_win, self.root)

    def open_forgot_password(self):
        """Open forgot password window."""
        forgot_win = tk.Toplevel(self.root)
        ForgotPasswordWindow(forgot_win, self.root)
    
    def open_admin_dashboard(self):
        """Open admin dashboard."""
        from admin import AdminDashboard
        root = tk.Tk()
        AdminDashboard(root)
        root.mainloop()
    
    def open_user_dashboard(self):
        """Open user dashboard."""
        from user import UserDashboard
        root = tk.Tk()
        UserDashboard(root)
        root.mainloop()


class RegistrationWindow:
    """Registration window for new users."""
    
    def __init__(self, window, parent):
        self.window = window
        self.parent = parent
        self.window.title("Register New Account")
        self.window.configure(bg=COLORS['background'])
        center_window(self.window, 500, 700)
        self.window.resizable(False, False)
        
        # Disable parent window
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        create_header_frame(self.window, "Create New Account")
        
        # Main container
        main_frame = tk.Frame(self.window, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['xl'])
        
        # Card frame
        card = tk.Frame(
            main_frame,
            bg=COLORS['surface'],
            relief=tk.FLAT,
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True)
        
        # Form container
        form_frame = tk.Frame(card, bg=COLORS['surface'])
        form_frame.pack(padx=SPACING['xl'], pady=SPACING['xl'])
        
        # Full Name
        name_label = create_styled_label(form_frame, "Full Name", 'body')
        name_label.pack(anchor='w', pady=(SPACING['sm'], SPACING['xs']))
        
        self.name_entry = create_styled_entry(form_frame, width=35)
        self.name_entry.pack(pady=(0, SPACING['md']), ipady=SPACING['xs'])
        
        # Email
        email_label = create_styled_label(form_frame, "Email Address", 'body')
        email_label.pack(anchor='w', pady=(SPACING['sm'], SPACING['xs']))
        
        self.email_entry = create_styled_entry(form_frame, width=35)
        self.email_entry.pack(pady=(0, SPACING['md']), ipady=SPACING['xs'])
        
        # Password
        password_label = create_styled_label(form_frame, "Password", 'body')
        password_label.pack(anchor='w', pady=(SPACING['sm'], SPACING['xs']))
        
        self.password_entry = create_styled_entry(form_frame, width=35, show='●')
        self.password_entry.pack(pady=(0, SPACING['md']), ipady=SPACING['xs'])
        
        # Confirm Password
        confirm_label = create_styled_label(form_frame, "Confirm Password", 'body')
        confirm_label.pack(anchor='w', pady=(SPACING['sm'], SPACING['xs']))
        
        self.confirm_password_entry = create_styled_entry(form_frame, width=35, show='●')
        self.confirm_password_entry.pack(pady=(0, SPACING['lg']), ipady=SPACING['xs'])
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        button_frame.pack(pady=SPACING['md'])
        
        # Register button
        register_btn = create_styled_button(
            button_frame,
            "Create Account",
            command=self.handle_register,
            style='success',
            width=15
        )
        register_btn.pack(side=tk.LEFT, padx=SPACING['xs'])
        
        # Cancel button
        cancel_btn = create_styled_button(
            button_frame,
            "Cancel",
            command=self.window.destroy,
            style='secondary',
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=SPACING['xs'])
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.handle_register())

    
    def handle_register(self):
        """Handle registration form submission."""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validation
        if not name or not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        valid, msg = validate_password_strength(password)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Create user
        success, message = UserModel.create(name, email, password, role='user')
        
        if success:
            messagebox.showinfo("Success", "Account created successfully! You can now login.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)


class ForgotPasswordWindow:
    """Window for resetting a forgotten password."""

    def __init__(self, window, parent):
        self.window = window
        self.parent = parent
        self.window.title("Reset Password")
        self.window.configure(bg=COLORS['background'])
        center_window(self.window, 480, 620)
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        self.create_widgets()

    def create_widgets(self):
        """Create and layout all widgets."""
        # Header
        create_header_frame(self.window, "Reset Password")

        # Main container
        main_frame = tk.Frame(self.window, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['xl'])

        # Card
        card = tk.Frame(
            main_frame,
            bg=COLORS['surface'],
            relief=tk.FLAT,
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True)

        # Form
        form_frame = tk.Frame(card, bg=COLORS['surface'])
        form_frame.pack(padx=SPACING['xl'], pady=SPACING['xl'])

        title = create_styled_label(form_frame, "Reset Your Password", 'heading')
        title.pack(pady=(0, SPACING['md']))

        hint = create_styled_label(
            form_frame,
            "Enter your registered email and choose a new password.",
            'small'
        )
        hint.pack(pady=(0, SPACING['xl']))

        # Email
        create_styled_label(form_frame, "Registered Email", 'body').pack(
            anchor='w', pady=(SPACING['sm'], SPACING['xs'])
        )
        self.email_entry = create_styled_entry(form_frame, width=35)
        self.email_entry.pack(pady=(0, SPACING['md']), ipady=SPACING['xs'])

        # New password
        create_styled_label(form_frame, "New Password", 'body').pack(
            anchor='w', pady=(SPACING['sm'], SPACING['xs'])
        )
        self.new_password_entry = create_styled_entry(form_frame, width=35, show='●')
        self.new_password_entry.pack(pady=(0, SPACING['md']), ipady=SPACING['xs'])

        # Confirm new password
        create_styled_label(form_frame, "Confirm New Password", 'body').pack(
            anchor='w', pady=(SPACING['sm'], SPACING['xs'])
        )
        self.confirm_entry = create_styled_entry(form_frame, width=35, show='●')
        self.confirm_entry.pack(pady=(0, SPACING['lg']), ipady=SPACING['xs'])

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        btn_frame.pack(pady=SPACING['md'])

        reset_btn = create_styled_button(
            btn_frame,
            "Reset Password",
            command=self.handle_reset,
            style='primary',
            width=15
        )
        reset_btn.pack(side=tk.LEFT, padx=SPACING['xs'])

        cancel_btn = create_styled_button(
            btn_frame,
            "Cancel",
            command=self.window.destroy,
            style='secondary',
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=SPACING['xs'])

        self.window.bind('<Return>', lambda e: self.handle_reset())

    def handle_reset(self):
        """Handle password reset submission."""
        email = self.email_entry.get().strip()
        new_password = self.new_password_entry.get()
        confirm = self.confirm_entry.get()

        if not email or not new_password or not confirm:
            messagebox.showerror("Error", "All fields are required", parent=self.window)
            return

        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format", parent=self.window)
            return

        valid, msg = validate_password_strength(new_password)
        if not valid:
            messagebox.showerror("Error", msg, parent=self.window)
            return

        if new_password != confirm:
            messagebox.showerror("Error", "Passwords do not match", parent=self.window)
            return

        success, message = UserModel.reset_password(email, new_password)
        if success:
            messagebox.showinfo("Success", "Password reset successfully! Please log in with your new password.", parent=self.window)
            self.window.destroy()
        else:
            messagebox.showerror("Error", message, parent=self.window)


def logout():
    """Logout current user and return to login."""
    global current_user
    current_user = None
    
    # Close all windows and show login
    for widget in tk.Tk().winfo_children():
        widget.destroy()
    
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
