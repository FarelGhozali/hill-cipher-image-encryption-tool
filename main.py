#!/usr/bin/env python3
"""
Hill Cipher Image Encryption Tool - Main Entry Point

This script provides a simple way to run the Hill Cipher GUI application.
It also includes command-line interface options for batch processing.

Usage:
    python main.py                  # Launch GUI
    python main.py --cli            # Command-line interface
    python main.py --test           # Run tests
    python main.py --help           # Show help
"""

import sys
import argparse
import os

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='Hill Cipher Image Encryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                     Launch GUI application
  python main.py --cli encrypt input.png output.png key.json
  python main.py --cli decrypt encrypted.png decrypted.png key.json
  python main.py --test              Run unit tests
  python main.py --generate-key key.json --size 3
        """
    )
    
    parser.add_argument('--cli', action='store_true',
                       help='Use command-line interface instead of GUI')
    parser.add_argument('--test', action='store_true',
                       help='Run unit tests')
    parser.add_argument('--generate-key', metavar='KEY_FILE',
                       help='Generate a new key and save to file')
    parser.add_argument('--size', type=int, default=2, choices=[2, 3, 4],
                       help='Key matrix size (default: 2)')
    
    # CLI-specific arguments
    parser.add_argument('operation', nargs='?', choices=['encrypt', 'decrypt'],
                       help='Operation to perform (CLI mode only)')
    parser.add_argument('input_file', nargs='?',
                       help='Input image file (CLI mode only)')
    parser.add_argument('output_file', nargs='?',
                       help='Output image file (CLI mode only)')
    parser.add_argument('key_file', nargs='?',
                       help='Key file (CLI mode only)')
    
    args = parser.parse_args()
    
    # Handle test mode
    if args.test:
        print("Running unit tests...")
        import unittest
        from test_hill_cipher import TestHillCipher
        
        suite = unittest.TestLoader().loadTestsFromTestCase(TestHillCipher)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("\nAll tests passed!")
            return 0
        else:
            print("\nSome tests failed!")
            return 1
    
    # Handle key generation
    if args.generate_key:
        from hill_cipher import HillCipher
        
        print(f"Generating {args.size}x{args.size} key matrix...")
        cipher = HillCipher(block_size=args.size)
        key_matrix = cipher.generate_random_key()
        
        if cipher.save_key(args.generate_key):
            print(f"Key saved to: {args.generate_key}")
            print("Key matrix:")
            print(key_matrix)
            return 0
        else:
            print("Failed to save key!")
            return 1
    
    # Handle CLI mode
    if args.cli:
        if not all([args.operation, args.input_file, args.output_file, args.key_file]):
            print("Error: CLI mode requires operation, input_file, output_file, and key_file")
            parser.print_help()
            return 1
        
        return run_cli(args.operation, args.input_file, args.output_file, args.key_file)
    
    # Default: Launch GUI
    try:
        import tkinter as tk
        from gui_application import HillCipherGUI
        
        print("Launching Hill Cipher GUI...")
        root = tk.Tk()
        app = HillCipherGUI(root)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        root.mainloop()
        return 0
        
    except ImportError as e:
        print(f"Error: Failed to import required modules: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"Error launching GUI: {e}")
        return 1

def run_cli(operation, input_file, output_file, key_file):
    """Run command-line interface operations."""
    try:
        from hill_cipher import HillCipher
        
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found!")
            return 1
        
        # Initialize cipher and load key
        cipher = HillCipher()
        
        if operation == "encrypt":
            # For encryption, check if key file exists
            if os.path.exists(key_file):
                if not cipher.load_key(key_file):
                    print(f"Error: Failed to load key from '{key_file}'!")
                    return 1
                print(f"Loaded key from: {key_file}")
            else:
                # Generate new key if file doesn't exist
                print("Key file not found. Generating new key...")
                cipher.generate_random_key()
                if cipher.save_key(key_file):
                    print(f"New key saved to: {key_file}")
                else:
                    print("Warning: Failed to save new key!")
            
            # Encrypt image
            print(f"Encrypting '{input_file}' to '{output_file}'...")
            success, message = cipher.encrypt_image(input_file, output_file)
            
        elif operation == "decrypt":
            # For decryption, key file must exist
            if not os.path.exists(key_file):
                print(f"Error: Key file '{key_file}' not found!")
                return 1
            
            if not cipher.load_key(key_file):
                print(f"Error: Failed to load key from '{key_file}'!")
                return 1
            
            print(f"Loaded key from: {key_file}")
            
            # Decrypt image
            print(f"Decrypting '{input_file}' to '{output_file}'...")
            success, message = cipher.decrypt_image(input_file, output_file)
        
        # Report results
        if success:
            print(f"Success: {message}")
            return 0
        else:
            print(f"Error: {message}")
            return 1
            
    except ImportError as e:
        print(f"Error: Failed to import required modules: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def check_dependencies():
    """Check if all required dependencies are available."""
    required_modules = [
        'numpy', 'PIL', 'tkinter', 'matplotlib', 'json'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print("Missing required modules:", ', '.join(missing))
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

if __name__ == "__main__":
    # Check dependencies before running
    if not check_dependencies():
        sys.exit(1)
    
    # Run main function
    exit_code = main()
    sys.exit(exit_code)
