import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import numpy as np
from PIL import Image, ImageTk
import os
import json
from hill_cipher import HillCipher
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

class HillCipherGUI:
    """
    User-friendly GUI for Hill Cipher Image Encryption/Decryption.
    Designed for non-IT users with intuitive interface.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hill Cipher Image Encryption Tool")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize Hill Cipher
        self.cipher = HillCipher()
        
        # Variables
        self.input_image_path = tk.StringVar()
        self.output_image_path = tk.StringVar()
        self.key_file_path = tk.StringVar()
        
        # Image display variables
        self.original_image = None
        self.processed_image = None
        
        self.create_widgets()
        self.create_menu()
        
    def create_menu(self):
        """Create application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Key", command=self.generate_new_key)
        file_menu.add_command(label="Load Key", command=self.load_key)
        file_menu.add_command(label="Save Key", command=self.save_key)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Use", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Hill Cipher Image Encryption Tool", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Encryption tab
        self.encrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encrypt_frame, text="Encrypt Image")
        self.create_encrypt_tab()
        
        # Decryption tab
        self.decrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decrypt_frame, text="Decrypt Image")
        self.create_decrypt_tab()
        
        # Key Management tab
        self.key_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.key_frame, text="Key Management")
        self.create_key_tab()
        
        # Analysis tab
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="Analysis")
        self.create_analysis_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, bg='lightgray')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_encrypt_tab(self):
        """Create encryption tab interface."""
        # Input section
        input_frame = ttk.LabelFrame(self.encrypt_frame, text="1. Select Input Image", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Entry(input_frame, textvariable=self.input_image_path, width=60).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_input_image).pack(side='left', padx=5)
        
        # Key section
        key_frame = ttk.LabelFrame(self.encrypt_frame, text="2. Encryption Key", padding=10)
        key_frame.pack(fill='x', padx=10, pady=5)
        
        key_buttons_frame = ttk.Frame(key_frame)
        key_buttons_frame.pack(fill='x')
        
        ttk.Button(key_buttons_frame, text="Generate Random Key", 
                  command=self.generate_new_key).pack(side='left', padx=5)
        ttk.Button(key_buttons_frame, text="Load Key from File", 
                  command=self.load_key).pack(side='left', padx=5)
        ttk.Button(key_buttons_frame, text="Enter Key Manually", 
                  command=self.manual_key_entry).pack(side='left', padx=5)
        
        # Current key display
        self.key_display = scrolledtext.ScrolledText(key_frame, height=4, width=50)
        self.key_display.pack(pady=5)
        
        # Output section
        output_frame = ttk.LabelFrame(self.encrypt_frame, text="3. Output Location", padding=10)
        output_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_image_path, width=60).pack(side='left', padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_output_image).pack(side='left', padx=5)
        
        # Action buttons
        action_frame = ttk.Frame(self.encrypt_frame)
        action_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(action_frame, text="Encrypt Image", command=self.encrypt_image,
                  style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="Save Key", command=self.save_key).pack(side='left', padx=5)
        
        # Progress bar
        self.encrypt_progress = ttk.Progressbar(self.encrypt_frame, mode='indeterminate')
        self.encrypt_progress.pack(fill='x', padx=10, pady=5)
        
        # Image preview frame
        preview_frame = ttk.LabelFrame(self.encrypt_frame, text="Image Preview")
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.encrypt_image_frame = ttk.Frame(preview_frame)
        self.encrypt_image_frame.pack(fill='both', expand=True)
        
        # Bind resize event to update preview
        self.encrypt_image_frame.bind('<Configure>', self.on_encrypt_frame_resize)
    
    def create_decrypt_tab(self):
        """Create decryption tab interface."""
        # Input section
        input_frame = ttk.LabelFrame(self.decrypt_frame, text="1. Select Encrypted Image", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        self.decrypt_input_path = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.decrypt_input_path, width=60).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_decrypt_input).pack(side='left', padx=5)
        
        # Key section
        key_frame = ttk.LabelFrame(self.decrypt_frame, text="2. Decryption Key", padding=10)
        key_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(key_frame, text="Load Key from File", command=self.load_key).pack(side='left', padx=5)
        ttk.Button(key_frame, text="Use Current Key", command=self.use_current_key).pack(side='left', padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(self.decrypt_frame, text="3. Output Location", padding=10)
        output_frame.pack(fill='x', padx=10, pady=5)
        
        self.decrypt_output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.decrypt_output_path, width=60).pack(side='left', padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_decrypt_output).pack(side='left', padx=5)
        
        # Action buttons
        action_frame = ttk.Frame(self.decrypt_frame)
        action_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(action_frame, text="Decrypt Image", command=self.decrypt_image,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        # Progress bar
        self.decrypt_progress = ttk.Progressbar(self.decrypt_frame, mode='indeterminate')
        self.decrypt_progress.pack(fill='x', padx=10, pady=5)
        
        # Image preview frame
        preview_frame = ttk.LabelFrame(self.decrypt_frame, text="Image Preview")
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.decrypt_image_frame = ttk.Frame(preview_frame)
        self.decrypt_image_frame.pack(fill='both', expand=True)
        
        # Bind resize event to update preview
        self.decrypt_image_frame.bind('<Configure>', self.on_decrypt_frame_resize)
    
    def create_key_tab(self):
        """Create key management tab."""
        # Key generation section
        gen_frame = ttk.LabelFrame(self.key_frame, text="Generate New Key", padding=10)
        gen_frame.pack(fill='x', padx=10, pady=5)
        
        size_frame = ttk.Frame(gen_frame)
        size_frame.pack(fill='x', pady=5)
        
        ttk.Label(size_frame, text="Key Matrix Size:").pack(side='left', padx=5)
        self.key_size_var = tk.IntVar(value=2)
        size_combo = ttk.Combobox(size_frame, textvariable=self.key_size_var, values=[2, 3, 4], 
                                 state='readonly', width=5)
        size_combo.pack(side='left', padx=5)
        
        ttk.Button(gen_frame, text="Generate Random Key", 
                  command=self.generate_new_key).pack(pady=5)
        
        # Manual key entry section
        manual_frame = ttk.LabelFrame(self.key_frame, text="Manual Key Entry", padding=10)
        manual_frame.pack(fill='x', padx=10, pady=5)
        
        # Matrix size selection
        size_frame = ttk.Frame(manual_frame)
        size_frame.pack(fill='x', pady=5)
        
        ttk.Label(size_frame, text="Matrix Size:").pack(side='left', padx=5)
        self.matrix_size_var = tk.StringVar(value="2")
        size_combo = ttk.Combobox(size_frame, textvariable=self.matrix_size_var, 
                                 values=["2", "3", "4"], state="readonly", width=5)
        size_combo.pack(side='left', padx=5)
        size_combo.bind('<<ComboboxSelected>>', self.on_matrix_size_change)
        
        # Matrix input grid
        self.matrix_input_frame = ttk.Frame(manual_frame)
        self.matrix_input_frame.pack(pady=10)
        
        # Store entry widgets
        self.matrix_entries = []
        
        # Create initial 2x2 grid
        self.create_matrix_input_grid(2)
        
        # Buttons frame
        buttons_frame = ttk.Frame(manual_frame)
        buttons_frame.pack(pady=5)
        
        ttk.Button(buttons_frame, text="Clear Matrix", 
                  command=self.clear_matrix_inputs).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Random Fill", 
                  command=self.random_fill_matrix).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Set Key from Matrix", 
                  command=self.set_manual_key).pack(side='left', padx=5)
        
        # ...removed legacy text input (advanced) feature...
        
        # Key display section
        display_frame = ttk.LabelFrame(self.key_frame, text="Current Key Matrix", padding=10)
        display_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.key_matrix_display = scrolledtext.ScrolledText(display_frame, height=10)
        self.key_matrix_display.pack(fill='both', expand=True, pady=5)
        
        # Key file operations
        file_frame = ttk.Frame(self.key_frame)
        file_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(file_frame, text="Load Key", command=self.load_key).pack(side='left', padx=5)
        ttk.Button(file_frame, text="Save Key", command=self.save_key).pack(side='left', padx=5)
    
    def create_analysis_tab(self):
        """Create image analysis tab."""
        # Analysis controls
        control_frame = ttk.LabelFrame(self.analysis_frame, text="Analysis Controls", padding=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Analyze Original vs Encrypted", 
                  command=self.analyze_images).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Show Histogram", 
                  command=self.show_histogram).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Calculate Entropy", 
                  command=self.calculate_entropy).pack(side='left', padx=5)
        
        # Analysis results
        self.analysis_notebook = ttk.Notebook(self.analysis_frame)
        self.analysis_notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Statistics tab
        stats_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(stats_frame, text="Statistics")
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=20, 
            font=('Consolas', 10)
        )
        self.stats_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Visualization tab
        self.viz_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(self.viz_frame, text="Visualization")
        
        self.viz_content_frame = ttk.Frame(self.viz_frame)
        self.viz_content_frame.pack(fill='both', expand=True)
    
    def browse_input_image(self):
        """Browse for input image file and automatically show preview."""
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                      ("All files", "*.*")]
        )
        if filename:
            self.input_image_path.set(filename)
            self.status_var.set(f"Selected input: {os.path.basename(filename)}")
            # Automatically show preview when image is selected
            self.preview_input_image()
    
    def browse_output_image(self):
        """Browse for output image location."""
        filename = filedialog.asksaveasfilename(
            title="Save Encrypted Image As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                      ("JPEG files", "*.jpg"),
                      ("All files", "*.*")]
        )
        if filename:
            self.output_image_path.set(filename)
    
    def browse_decrypt_input(self):
        """Browse for encrypted image to decrypt and automatically show preview."""
        filename = filedialog.askopenfilename(
            title="Select Encrypted Image File",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                      ("All files", "*.*")]
        )
        if filename:
            self.decrypt_input_path.set(filename)
            # Automatically show preview when image is selected
            self.preview_decrypt_image()
    
    def browse_decrypt_output(self):
        """Browse for decrypted image output location."""
        filename = filedialog.asksaveasfilename(
            title="Save Decrypted Image As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                      ("JPEG files", "*.jpg"),
                      ("All files", "*.*")]
        )
        if filename:
            self.decrypt_output_path.set(filename)
    
    def preview_input_image(self):
        """Preview the selected input image."""
        if not self.input_image_path.get():
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        
        try:
            # Clear previous preview
            for widget in self.encrypt_image_frame.winfo_children():
                widget.destroy()
            
            # Load and display image
            image = Image.open(self.input_image_path.get())
            
            # Get the available space for the image
            self.encrypt_image_frame.update_idletasks()
            frame_width = self.encrypt_image_frame.winfo_width()
            frame_height = self.encrypt_image_frame.winfo_height()
            
            # Calculate available space (leave some padding)
            available_width = max(frame_width - 40, 400)  # Minimum 400px
            available_height = max(frame_height - 80, 300)  # Minimum 300px, leave space for info
            
            # Resize image to fit available space while maintaining aspect ratio
            image.thumbnail((available_width, available_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Create a frame for centering
            image_container = ttk.Frame(self.encrypt_image_frame)
            image_container.pack(fill='both', expand=True, padx=10, pady=10)
            
            label = ttk.Label(image_container, image=photo)
            label.image = photo  # Keep a reference
            label.pack(expand=True)
            
            # Show image info at the bottom
            info_label = ttk.Label(self.encrypt_image_frame, 
                                  text=f"Size: {image.size}, Mode: {image.mode}")
            info_label.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot preview image: {str(e)}")
    
    def preview_decrypt_image(self):
        """Preview the selected encrypted image for decryption."""
        if not self.decrypt_input_path.get():
            messagebox.showwarning("Warning", "Please select an encrypted image first!")
            return
        
        try:
            # Clear previous preview
            for widget in self.decrypt_image_frame.winfo_children():
                widget.destroy()
            
            # Load and display image
            image = Image.open(self.decrypt_input_path.get())
            
            # Get the available space for the image
            self.decrypt_image_frame.update_idletasks()
            frame_width = self.decrypt_image_frame.winfo_width()
            frame_height = self.decrypt_image_frame.winfo_height()
            
            # Calculate available space (leave some padding)
            available_width = max(frame_width - 40, 400)  # Minimum 400px
            available_height = max(frame_height - 80, 300)  # Minimum 300px, leave space for info
            
            # Resize image to fit available space while maintaining aspect ratio
            image.thumbnail((available_width, available_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Create a frame for centering
            image_container = ttk.Frame(self.decrypt_image_frame)
            image_container.pack(fill='both', expand=True, padx=10, pady=10)
            
            label = ttk.Label(image_container, image=photo)
            label.image = photo  # Keep a reference
            label.pack(expand=True)
            
            # Show image info at the bottom
            info_label = ttk.Label(self.decrypt_image_frame, 
                                  text=f"Size: {image.size}, Mode: {image.mode}")
            info_label.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot preview image: {str(e)}")
    
    def generate_new_key(self):
        """Generate a new random key matrix."""
        try:
            self.cipher.block_size = self.key_size_var.get()
            key_matrix = self.cipher.generate_random_key()
            self.update_key_display()
            self.status_var.set("New key generated successfully!")
            messagebox.showinfo("Success", "New encryption key generated!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate key: {str(e)}")
    
    def load_key(self):
        """Load key from file."""
        filename = filedialog.askopenfilename(
            title="Load Encryption Key",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            if self.cipher.load_key(filename):
                self.update_key_display()
                self.status_var.set(f"Key loaded from {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Key loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load key file!")
    
    def save_key(self):
        """Save current key to file."""
        if self.cipher.key_matrix is None:
            messagebox.showwarning("Warning", "No key to save! Generate or load a key first.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Encryption Key",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            if self.cipher.save_key(filename):
                self.status_var.set(f"Key saved to {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Key saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save key!")
    
    def manual_key_entry(self):
        """Open enhanced manual key entry dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manual Key Entry")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        title_label = ttk.Label(dialog, text="Enter Key Matrix Values", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Matrix size selection
        size_frame = ttk.Frame(dialog)
        size_frame.pack(pady=5)
        
        ttk.Label(size_frame, text="Matrix Size:").pack(side='left', padx=5)
        dialog_size_var = tk.StringVar(value="2")
        size_combo = ttk.Combobox(size_frame, textvariable=dialog_size_var, 
                                 values=["2", "3", "4"], state="readonly", width=5)
        size_combo.pack(side='left', padx=5)
        
        # Matrix input container
        matrix_container = ttk.Frame(dialog)
        matrix_container.pack(pady=10, expand=True, fill='both')
        
        dialog_entries = []
        
        def create_dialog_grid(size):
            # Clear existing widgets
            for widget in matrix_container.winfo_children():
                widget.destroy()
            
            dialog_entries.clear()
            
            # Create validation for numbers only
            vcmd = (dialog.register(lambda P: P == "" or (P.isdigit() and 0 <= int(P) <= 255)), '%P')
            
            # Create entry grid
            for i in range(size):
                row_entries = []
                for j in range(size):
                    entry = ttk.Entry(matrix_container, 
                                    width=8, 
                                    justify='center',
                                    validate='key',
                                    validatecommand=vcmd)
                    entry.grid(row=i, column=j, padx=3, pady=3)
                    entry.insert(0, "0")
                    
                    # Bind events
                    entry.bind('<FocusIn>', lambda e: e.widget.select_range(0, 'end'))
                    
                    row_entries.append(entry)
                dialog_entries.append(row_entries)
            
            # Add example values for 2x2
            if size == 2:
                dialog_entries[0][0].delete(0, 'end')
                dialog_entries[0][0].insert(0, "3")
                dialog_entries[0][1].delete(0, 'end')
                dialog_entries[0][1].insert(0, "2")
                dialog_entries[1][0].delete(0, 'end')
                dialog_entries[1][0].insert(0, "5")
                dialog_entries[1][1].delete(0, 'end')
                dialog_entries[1][1].insert(0, "7")
        
        # Bind size change
        def on_size_change(event=None):
            size = int(dialog_size_var.get())
            create_dialog_grid(size)
        
        size_combo.bind('<<ComboboxSelected>>', on_size_change)
        
        # Create initial grid
        create_dialog_grid(2)
        
        # Buttons frame
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def generate_random():
            size = int(dialog_size_var.get())
            temp_cipher = HillCipher(block_size=size)
            random_key = temp_cipher.generate_random_key()
            
            for i in range(size):
                for j in range(size):
                    dialog_entries[i][j].delete(0, 'end')
                    dialog_entries[i][j].insert(0, str(random_key[i][j]))
        
        def apply_key():
            try:
                size = int(dialog_size_var.get())
                matrix = []
                
                for i in range(size):
                    row = []
                    for j in range(size):
                        value_str = dialog_entries[i][j].get().strip()
                        if not value_str:
                            value_str = "0"
                        value = int(value_str)
                        
                        if value < 0 or value > 255:
                            raise ValueError(f"Values must be between 0 and 255. Found: {value}")
                        
                        row.append(value)
                    matrix.append(row)
                
                key_matrix = np.array(matrix)
                
                # Validate matrix
                det = int(np.round(np.linalg.det(key_matrix))) % 256
                if self.cipher.gcd(det, 256) != 1:
                    messagebox.showerror("Invalid Matrix", 
                        f"Matrix is not invertible mod 256 (determinant: {det}).\n"
                        "Please use 'Generate Random' for a valid matrix.")
                    return
                
                if self.cipher.set_key_matrix(key_matrix):
                    self.update_key_display()
                    
                    # Update main interface
                    self.matrix_size_var.set(str(size))
                    self.create_matrix_input_grid(size)
                    
                    # Fill main grid with values
                    for i in range(size):
                        for j in range(size):
                            self.matrix_entries[i][j].delete(0, 'end')
                            self.matrix_entries[i][j].insert(0, str(key_matrix[i][j]))
                    
                    dialog.destroy()
                    messagebox.showinfo("Success", "Key matrix set successfully!")
                else:
                    messagebox.showerror("Error", "Failed to set key matrix!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        ttk.Button(button_frame, text="Generate Random", 
                  command=generate_random).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Apply", 
                  command=apply_key).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side='left', padx=5)
        
        # Help text
        help_text = ttk.Label(dialog, 
            text="Enter values between 0-255. Use 'Generate Random' for a guaranteed valid matrix.",
            font=('Arial', 9),
            foreground='gray')
        help_text.pack(pady=5)
    
    def set_manual_key(self):
        """Set key from matrix input grid."""
        try:
            size = int(self.matrix_size_var.get())
            matrix = []
            
            # Collect values from grid
            for i in range(size):
                row = []
                for j in range(size):
                    value_str = self.matrix_entries[i][j].get().strip()
                    if not value_str:
                        value_str = "0"
                    value = int(value_str)
                    
                    # Validate range (0-255 for image processing)
                    if value < 0 or value > 255:
                        raise ValueError(f"Matrix values must be between 0 and 255. Found: {value}")
                    
                    row.append(value)
                matrix.append(row)
            
            key_matrix = np.array(matrix)
            
            # Validate matrix properties
            if key_matrix.shape[0] != key_matrix.shape[1]:
                raise ValueError("Matrix must be square!")
            
            # Check if matrix is valid for Hill Cipher
            det = int(np.round(np.linalg.det(key_matrix))) % 256
            if self.cipher.gcd(det, 256) != 1:
                response = messagebox.askyesno(
                    "Invalid Matrix", 
                    f"This matrix is not invertible mod 256 (determinant: {det}).\n\n"
                    "Would you like to generate a random valid matrix instead?",
                    icon='warning'
                )
                if response:
                    self.random_fill_matrix()
                    return
                else:
                    return
            
            # Set the key
            if self.cipher.set_key_matrix(key_matrix):
                self.update_key_display()
                messagebox.showinfo("Success", 
                    f"Key matrix set successfully!\n"
                    f"Size: {size}x{size}\n"
                    f"Determinant: {det}")
            else:
                messagebox.showerror("Error", "Failed to set key matrix!")
                
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set key: {str(e)}")
    
    def update_key_display(self):
        """Update the key display in GUI."""
        if self.cipher.key_matrix is not None:
            key_matrix = self.cipher.key_matrix
            det = int(np.round(np.linalg.det(key_matrix)))
            size = f"{key_matrix.shape[0]}x{key_matrix.shape[1]}"
            key_text = (
                "Kunci Enkripsi (Key Matrix):\n"
                f"{key_matrix}\n\n"
                f"Ukuran Matriks: {size}\n"
                f"Determinan: {det}\n\n"
                "Penjelasan:\n"
                "- Matriks di atas digunakan untuk mengenkripsi gambar.\n"
                "- Ukuran matriks menentukan kekuatan enkripsi.\n"
                "- Determinan harus memiliki invers modulo 256 agar bisa digunakan untuk dekripsi.\n"
            )
            # Update all key displays
            self.key_display.delete('1.0', tk.END)
            self.key_display.insert('1.0', key_text)
            self.key_matrix_display.delete('1.0', tk.END)
            self.key_matrix_display.insert('1.0', key_text)
        else:
            no_key_text = "No key loaded. Generate or load a key first."
            self.key_display.delete('1.0', tk.END)
            self.key_display.insert('1.0', no_key_text)
            self.key_matrix_display.delete('1.0', tk.END)
            self.key_matrix_display.insert('1.0', no_key_text)
    
    def use_current_key(self):
        """Use the currently loaded key for decryption."""
        if self.cipher.key_matrix is not None:
            messagebox.showinfo("Info", "Using current key for decryption.")
        else:
            messagebox.showwarning("Warning", "No key loaded! Please generate or load a key first.")
    
    def encrypt_image(self):
        """Encrypt the selected image."""
        if not self.input_image_path.get():
            messagebox.showwarning("Warning", "Please select an input image!")
            return
        
        if not self.output_image_path.get():
            messagebox.showwarning("Warning", "Please specify output location!")
            return
        
        if self.cipher.key_matrix is None:
            messagebox.showwarning("Warning", "Please generate or load a key first!")
            return
        
        def encrypt_thread():
            try:
                self.encrypt_progress.start()
                self.status_var.set("Encrypting image...")
                
                success, message = self.cipher.encrypt_image(
                    self.input_image_path.get(),
                    self.output_image_path.get()
                )
                
                self.encrypt_progress.stop()
                
                if success:
                    self.status_var.set("Encryption completed successfully!")
                    messagebox.showinfo("Success", message)
                else:
                    self.status_var.set("Encryption failed!")
                    messagebox.showerror("Error", message)
                    
            except Exception as e:
                self.encrypt_progress.stop()
                self.status_var.set("Encryption failed!")
                messagebox.showerror("Error", f"Encryption failed: {str(e)}")
        
        # Run encryption in separate thread to prevent GUI freezing
        threading.Thread(target=encrypt_thread, daemon=True).start()
    
    def decrypt_image(self):
        """Decrypt the selected image."""
        if not self.decrypt_input_path.get():
            messagebox.showwarning("Warning", "Please select an encrypted image!")
            return
        
        if not self.decrypt_output_path.get():
            messagebox.showwarning("Warning", "Please specify output location!")
            return
        
        if self.cipher.key_matrix is None:
            messagebox.showwarning("Warning", "Please load or generate a key first!")
            return
        
        def decrypt_thread():
            try:
                self.decrypt_progress.start()
                self.status_var.set("Decrypting image...")
                
                success, message = self.cipher.decrypt_image(
                    self.decrypt_input_path.get(),
                    self.decrypt_output_path.get()
                )
                
                self.decrypt_progress.stop()
                
                if success:
                    self.status_var.set("Decryption completed successfully!")
                    messagebox.showinfo("Success", message)
                else:
                    self.status_var.set("Decryption failed!")
                    messagebox.showerror("Error", message)
                    
            except Exception as e:
                self.decrypt_progress.stop()
                self.status_var.set("Decryption failed!")
                messagebox.showerror("Error", f"Decryption failed: {str(e)}")
        
        # Run decryption in separate thread to prevent GUI freezing
        threading.Thread(target=decrypt_thread, daemon=True).start()
    
    def analyze_images(self):
        """Analyze original vs encrypted images."""
        if not self.input_image_path.get():
            messagebox.showwarning("Warning", "Please select an original image first!")
            return
        
        if not self.output_image_path.get() or not os.path.exists(self.output_image_path.get()):
            messagebox.showwarning("Warning", "Please encrypt an image first!")
            return
        
        try:
            # Load images
            original = Image.open(self.input_image_path.get())
            encrypted = Image.open(self.output_image_path.get())
            
            # Convert to numpy arrays
            orig_array = np.array(original)
            enc_array = np.array(encrypted)
            
            # Calculate statistics
            stats_text = "=== IMAGE ANALYSIS RESULTS ===\n\n"
            
            # Basic info
            stats_text += f"Original Image:\n"
            stats_text += f"  Size: {original.size}\n"
            stats_text += f"  Mode: {original.mode}\n"
            stats_text += f"  Min value: {orig_array.min()}\n"
            stats_text += f"  Max value: {orig_array.max()}\n"
            stats_text += f"  Mean: {orig_array.mean():.2f}\n"
            stats_text += f"  Std Dev: {orig_array.std():.2f}\n\n"
            
            stats_text += f"Encrypted Image:\n"
            stats_text += f"  Size: {encrypted.size}\n"
            stats_text += f"  Mode: {encrypted.mode}\n"
            stats_text += f"  Min value: {enc_array.min()}\n"
            stats_text += f"  Max value: {enc_array.max()}\n"
            stats_text += f"  Mean: {enc_array.mean():.2f}\n"
            stats_text += f"  Std Dev: {enc_array.std():.2f}\n\n"
            
            # Correlation coefficient
            if orig_array.shape == enc_array.shape:
                correlation = np.corrcoef(orig_array.flatten(), enc_array.flatten())[0, 1]
                stats_text += f"Correlation Coefficient: {correlation:.6f}\n"
                stats_text += f"Encryption Quality: {'Excellent' if abs(correlation) < 0.1 else 'Good' if abs(correlation) < 0.3 else 'Fair'}\n\n"
            
            # Update stats display
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', stats_text)
            
            # Switch to analysis tab
            self.notebook.select(self.analysis_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def show_histogram(self):
        """Show histogram comparison."""
        if not self.input_image_path.get():
            messagebox.showwarning("Warning", "Please select an original image first!")
            return
        
        if not self.output_image_path.get() or not os.path.exists(self.output_image_path.get()):
            messagebox.showwarning("Warning", "Please encrypt an image first!")
            return
        
        try:
            # Clear previous plots
            for widget in self.viz_content_frame.winfo_children():
                widget.destroy()
            
            # Load images
            original = Image.open(self.input_image_path.get())
            encrypted = Image.open(self.output_image_path.get())
            
            # Get available space for visualization
            self.viz_content_frame.update_idletasks()
            frame_width = max(self.viz_content_frame.winfo_width(), 800)
            frame_height = max(self.viz_content_frame.winfo_height(), 600)
            
            # Calculate figure size based on available space
            fig_width = min(frame_width / 80, 20)  # Convert pixels to inches (approx 80 DPI)
            fig_height = min(frame_height / 80, 15)
            
            # Create matplotlib figure
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(fig_width, fig_height))
            
            # Original image
            ax1.imshow(original)
            ax1.set_title("Original Image")
            ax1.axis('off')
            
            # Encrypted image
            ax2.imshow(encrypted)
            ax2.set_title("Encrypted Image")
            ax2.axis('off')
            
            # Original histogram
            orig_array = np.array(original)
            if len(orig_array.shape) == 3:  # Color image
                colors = ['red', 'green', 'blue']
                for i, color in enumerate(colors):
                    ax3.hist(orig_array[:,:,i].flatten(), bins=50, alpha=0.7, color=color, label=color.capitalize())
                ax3.legend()
            else:  # Grayscale
                ax3.hist(orig_array.flatten(), bins=50, alpha=0.7, color='gray')
            ax3.set_title("Original Histogram")
            ax3.set_xlabel("Pixel Value")
            ax3.set_ylabel("Frequency")
            
            # Encrypted histogram
            enc_array = np.array(encrypted)
            if len(enc_array.shape) == 3:  # Color image
                colors = ['red', 'green', 'blue']
                for i, color in enumerate(colors):
                    ax4.hist(enc_array[:,:,i].flatten(), bins=50, alpha=0.7, color=color, label=color.capitalize())
                ax4.legend()
            else:  # Grayscale
                ax4.hist(enc_array.flatten(), bins=50, alpha=0.7, color='gray')
            ax4.set_title("Encrypted Histogram")
            ax4.set_xlabel("Pixel Value")
            ax4.set_ylabel("Frequency")
            
            plt.tight_layout()
            
            # Embed plot in tkinter
            canvas = FigureCanvasTkAgg(fig, self.viz_content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            # Switch to analysis tab
            self.notebook.select(self.analysis_frame)
            self.analysis_notebook.select(self.viz_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Histogram generation failed: {str(e)}")
    
    def calculate_entropy(self):
        """Calculate and display image entropy."""
        if not self.input_image_path.get():
            messagebox.showwarning("Warning", "Please select an original image first!")
            return
        
        try:
            def entropy(image_array):
                """Calculate Shannon entropy of an image."""
                # Get histogram
                hist, _ = np.histogram(image_array.flatten(), bins=256, range=(0, 256))
                # Remove zeros
                hist = hist[hist > 0]
                # Calculate probabilities
                prob = hist / hist.sum()
                # Calculate entropy
                return -np.sum(prob * np.log2(prob))
            
            # Load original image
            original = Image.open(self.input_image_path.get())
            orig_array = np.array(original)
            orig_entropy = entropy(orig_array)
            
            result_text = f"=== ENTROPY ANALYSIS ===\n\n"
            result_text += f"Original Image Entropy: {orig_entropy:.4f} bits\n"
            
            # Check if encrypted image exists
            if self.output_image_path.get() and os.path.exists(self.output_image_path.get()):
                encrypted = Image.open(self.output_image_path.get())
                enc_array = np.array(encrypted)
                enc_entropy = entropy(enc_array)
                result_text += f"Encrypted Image Entropy: {enc_entropy:.4f} bits\n"
                result_text += f"Entropy Increase: {enc_entropy - orig_entropy:.4f} bits\n\n"
                
                result_text += "Interpretation:\n"
                result_text += f"- Higher entropy indicates more randomness\n"
                result_text += f"- Maximum possible entropy: 8.0 bits\n"
                result_text += f"- Encryption quality: {'Excellent' if enc_entropy > 7.5 else 'Good' if enc_entropy > 7.0 else 'Fair'}\n"
            
            # Update stats display
            current_text = self.stats_text.get('1.0', tk.END)
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', current_text + "\n" + result_text)
            
            # Switch to analysis tab
            self.notebook.select(self.analysis_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Entropy calculation failed: {str(e)}")
    
    def show_help(self):
        """Show help dialog."""
        help_text = """
        HILL CIPHER IMAGE ENCRYPTION TOOL - USER GUIDE
        
        1. ENCRYPTING AN IMAGE:
           - Go to 'Encrypt Image' tab
           - Select an image file using 'Browse' button
           - Generate a random key or load an existing key
           - Choose output location for encrypted image
           - Click 'Encrypt Image'
           - Save the key for later decryption!
        
        2. DECRYPTING AN IMAGE:
           - Go to 'Decrypt Image' tab
           - Select the encrypted image file
           - Load the correct key file
           - Choose output location for decrypted image
           - Click 'Decrypt Image'
        
        3. KEY MANAGEMENT:
           - Generate random keys for maximum security
           - Save keys to files for later use
           - Load keys from previously saved files
           - Enter keys manually if needed
        
        4. ANALYSIS:
           - Compare original and encrypted images
           - View histograms to verify encryption quality
           - Calculate entropy to measure randomness
        
        IMPORTANT NOTES:
        - Always save your encryption key!
        - Use the same key for encryption and decryption
        - Larger key matrices provide stronger encryption
        - Keep your keys secure and confidential
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("User Guide")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
        Hill Cipher Image Encryption Tool
        Version 1.0
        
        Implementation of Hill Cipher for Image Coding using Cryptography
        
        This tool provides a user-friendly interface for encrypting and 
        decrypting images using the Hill Cipher algorithm. It includes 
        analysis tools to evaluate encryption quality.
        
        Developed for educational and research purposes.
        
        Features:
        • Easy-to-use graphical interface
        • Secure image encryption/decryption
        • Key management system
        • Encryption quality analysis
        • Support for various image formats
        
        © 2025 - Educational Project
        """
        
        messagebox.showinfo("About", about_text)

    def on_encrypt_frame_resize(self, event):
        """Handle encrypt frame resize to update image preview."""
        if self.input_image_path.get() and hasattr(self, '_encrypt_resize_job'):
            # Cancel previous resize job if exists
            self.root.after_cancel(self._encrypt_resize_job)
        
        # Schedule preview update after short delay to avoid too frequent updates
        self._encrypt_resize_job = self.root.after(300, self.update_encrypt_preview)
    
    def on_decrypt_frame_resize(self, event):
        """Handle decrypt frame resize to update image preview."""
        if self.decrypt_input_path.get() and hasattr(self, '_decrypt_resize_job'):
            # Cancel previous resize job if exists
            self.root.after_cancel(self._decrypt_resize_job)
        
        # Schedule preview update after short delay to avoid too frequent updates
        self._decrypt_resize_job = self.root.after(300, self.update_decrypt_preview)
    
    def update_encrypt_preview(self):
        """Update encrypt image preview after frame resize."""
        if self.input_image_path.get():
            self.preview_input_image()
    
    def update_decrypt_preview(self):
        """Update decrypt image preview after frame resize."""
        if self.decrypt_input_path.get():
            self.preview_decrypt_image()
    
    def create_matrix_input_grid(self, size):
        """Create a grid of entry widgets for matrix input."""
        # Clear existing widgets
        for widget in self.matrix_input_frame.winfo_children():
            widget.destroy()
        
        self.matrix_entries = []
        
        # Create title
        title_label = ttk.Label(self.matrix_input_frame, 
                               text=f"{size}x{size} Matrix Input", 
                               font=('Arial', 12, 'bold'))
        title_label.grid(row=0, column=0, columnspan=size, pady=5)
        
        # Create entry grid
        for i in range(size):
            row_entries = []
            for j in range(size):
                # Create validation for numbers only
                vcmd = (self.root.register(self.validate_number), '%P')
                
                entry = ttk.Entry(self.matrix_input_frame, 
                                width=8, 
                                justify='center',
                                validate='key',
                                validatecommand=vcmd)
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                entry.insert(0, "0")  # Default value
                
                # Bind events for better UX
                entry.bind('<FocusIn>', lambda e: e.widget.select_range(0, 'end'))
                entry.bind('<Return>', self.focus_next_entry)
                
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
        
        # Add example values for demonstration
        if size == 2:
            self.matrix_entries[0][0].delete(0, 'end')
            self.matrix_entries[0][0].insert(0, "3")
            self.matrix_entries[0][1].delete(0, 'end')
            self.matrix_entries[0][1].insert(0, "2")
            self.matrix_entries[1][0].delete(0, 'end')
            self.matrix_entries[1][0].insert(0, "5")
            self.matrix_entries[1][1].delete(0, 'end')
            self.matrix_entries[1][1].insert(0, "7")
    
    def validate_number(self, value):
        """Validate that input is a number."""
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def focus_next_entry(self, event):
        """Move focus to next entry when Enter is pressed."""
        current_widget = event.widget
        
        # Find current position
        for i, row in enumerate(self.matrix_entries):
            for j, entry in enumerate(row):
                if entry == current_widget:
                    # Move to next entry
                    if j < len(row) - 1:
                        row[j + 1].focus_set()
                    elif i < len(self.matrix_entries) - 1:
                        self.matrix_entries[i + 1][0].focus_set()
                    return
    
    def on_matrix_size_change(self, event=None):
        """Handle matrix size change."""
        size = int(self.matrix_size_var.get())
        self.create_matrix_input_grid(size)
    
    def clear_matrix_inputs(self):
        """Clear all matrix input fields."""
        for row in self.matrix_entries:
            for entry in row:
                entry.delete(0, 'end')
                entry.insert(0, "0")
    
    def random_fill_matrix(self):
        """Fill matrix with random values."""
        import random
        size = int(self.matrix_size_var.get())
        
        # Generate a valid key matrix
        temp_cipher = HillCipher(block_size=size)
        random_key = temp_cipher.generate_random_key()
        
        # Fill the entries
        for i in range(size):
            for j in range(size):
                self.matrix_entries[i][j].delete(0, 'end')
                self.matrix_entries[i][j].insert(0, str(random_key[i][j]))
        
        messagebox.showinfo("Random Fill", "Matrix filled with random valid values!")
    
    # ...removed toggle_text_input (legacy text input feature)...
    
    def set_manual_key_from_text(self):
        """Set key from text area (legacy method)."""
        try:
            text = self.manual_key_text.get('1.0', 'end-1c')
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            matrix = []
            for line in lines:
                row = [int(x) for x in line.split()]
                matrix.append(row)
            
            key_matrix = np.array(matrix)
            
            if key_matrix.shape[0] != key_matrix.shape[1]:
                raise ValueError("Matrix must be square!")
            
            if self.cipher.set_key_matrix(key_matrix):
                self.update_key_display()
                messagebox.showinfo("Success", "Key set successfully!")
                
                # Update grid display to match
                size = key_matrix.shape[0]
                self.matrix_size_var.set(str(size))
                self.create_matrix_input_grid(size)
                
                # Fill grid with values
                for i in range(size):
                    for j in range(size):
                        self.matrix_entries[i][j].delete(0, 'end')
                        self.matrix_entries[i][j].insert(0, str(key_matrix[i][j]))
            else:
                messagebox.showerror("Error", "Invalid key matrix! Matrix must be invertible mod 256.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Invalid matrix format: {str(e)}")
