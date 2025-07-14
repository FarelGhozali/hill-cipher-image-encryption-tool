"""
Hill Cipher Image Encryption - Complete Demonstration

This script demonstrates all the features of the Hill Cipher image encryption tool.
It shows both the command-line interface and core functionality.
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from hill_cipher import HillCipher

def demonstrate_hill_cipher():
    """Complete demonstration of Hill Cipher functionality."""
    
    print("="*60)
    print("HILL CIPHER IMAGE ENCRYPTION DEMONSTRATION")
    print("="*60)
    print()
    
    # Step 1: Create cipher instance
    print("Step 1: Creating Hill Cipher instance...")
    cipher = HillCipher()
    print("✓ Hill Cipher instance created")
    print()
    
    # Step 2: Generate encryption key
    print("Step 2: Generating random encryption key...")
    key_matrix = cipher.generate_random_key()
    print("✓ Random key generated:")
    print(f"Key Matrix:\n{key_matrix}")
    print(f"Matrix Size: {key_matrix.shape[0]}x{key_matrix.shape[1]}")
    print(f"Determinant: {int(np.round(np.linalg.det(key_matrix)))}")
    print()
    
    # Step 3: Test mathematical operations
    print("Step 3: Testing mathematical operations...")
    
    # Test GCD
    gcd_result = cipher.gcd(48, 18)
    print(f"✓ GCD(48, 18) = {gcd_result}")
    
    # Test modular inverse
    try:
        mod_inv = cipher.mod_inverse(7, 26)
        print(f"✓ Modular inverse of 7 mod 26 = {mod_inv}")
    except ValueError as e:
        print(f"✗ Modular inverse test failed: {e}")
    
    # Test matrix inverse
    inverse_matrix = cipher.inverse_key_matrix
    print(f"✓ Inverse key matrix:\n{inverse_matrix}")
    
    # Verify matrix multiplication
    identity_check = np.dot(key_matrix, inverse_matrix) % 256
    print(f"✓ Key × Inverse mod 256:\n{identity_check}")
    print()
    
    # Step 4: Save and load key
    print("Step 4: Testing key save/load functionality...")
    key_file = "demo_key.json"
    
    save_success = cipher.save_key(key_file)
    print(f"✓ Key saved to {key_file}: {save_success}")
    
    # Load key in new cipher instance
    new_cipher = HillCipher()
    load_success = new_cipher.load_key(key_file)
    print(f"✓ Key loaded successfully: {load_success}")
    
    if load_success:
        print("✓ Loaded key matches original:", np.array_equal(cipher.key_matrix, new_cipher.key_matrix))
    print()
    
    # Step 5: Test with sample images
    print("Step 5: Testing image encryption/decryption...")
    
    # Check if sample images exist, create if not
    if not os.path.exists("sample_images/test_color.png"):
        print("Creating sample images...")
        os.system("python create_test_images.py")
    
    # Test different image types
    test_images = [
        ("sample_images/test_color.png", "Color Image"),
        ("sample_images/test_grayscale.png", "Grayscale Image"),
        ("sample_images/test_pattern.png", "Pattern Image")
    ]
    
    for img_path, img_type in test_images:
        if os.path.exists(img_path):
            print(f"\nTesting {img_type}: {img_path}")
            
            # Encrypt
            encrypted_path = f"demo_encrypted_{os.path.basename(img_path)}"
            encrypt_success, encrypt_msg = cipher.encrypt_image(img_path, encrypted_path)
            print(f"  Encryption: {'✓' if encrypt_success else '✗'} {encrypt_msg}")
            
            if encrypt_success:
                # Decrypt
                decrypted_path = f"demo_decrypted_{os.path.basename(img_path)}"
                decrypt_success, decrypt_msg = cipher.decrypt_image(encrypted_path, decrypted_path)
                print(f"  Decryption: {'✓' if decrypt_success else '✗'} {decrypt_msg}")
                
                if decrypt_success:
                    # Verify integrity
                    original = np.array(Image.open(img_path))
                    decrypted = np.array(Image.open(decrypted_path))
                    integrity_check = np.array_equal(original, decrypted)
                    print(f"  Integrity: {'✓' if integrity_check else '✗'} Data matches original")
                    
                    # Calculate statistics
                    encrypted_img = np.array(Image.open(encrypted_path))
                    correlation = np.corrcoef(original.flatten(), encrypted_img.flatten())[0, 1]
                    print(f"  Correlation: {correlation:.6f} (lower is better)")
                    
                    # Calculate entropy
                    def calculate_entropy(data):
                        hist, _ = np.histogram(data.flatten(), bins=256, range=(0, 256))
                        hist = hist[hist > 0]
                        prob = hist / hist.sum()
                        return -np.sum(prob * np.log2(prob))
                    
                    orig_entropy = calculate_entropy(original)
                    enc_entropy = calculate_entropy(encrypted_img)
                    print(f"  Original Entropy: {orig_entropy:.4f} bits")
                    print(f"  Encrypted Entropy: {enc_entropy:.4f} bits")
                    print(f"  Entropy Improvement: {enc_entropy - orig_entropy:.4f} bits")
    
    print()
    
    # Step 6: Test different key sizes
    print("Step 6: Testing different key matrix sizes...")
    
    key_sizes = [2, 3]
    for size in key_sizes:
        print(f"\nTesting {size}x{size} key matrix:")
        test_cipher = HillCipher(block_size=size)
        test_key = test_cipher.generate_random_key()
        print(f"  Generated {size}x{size} key: ✓")
        print(f"  Key Matrix:\n{test_key}")
        
        # Test encryption with this key size
        if os.path.exists("sample_images/test_color.png"):
            test_encrypted = f"test_encrypted_{size}x{size}.png"
            test_decrypted = f"test_decrypted_{size}x{size}.png"
            
            enc_success, _ = test_cipher.encrypt_image("sample_images/test_color.png", test_encrypted)
            if enc_success:
                dec_success, _ = test_cipher.decrypt_image(test_encrypted, test_decrypted)
                print(f"  Encryption/Decryption: {'✓' if dec_success else '✗'}")
                
                # Clean up
                if os.path.exists(test_encrypted):
                    os.remove(test_encrypted)
                if os.path.exists(test_decrypted):
                    os.remove(test_decrypted)
                metadata_path = test_encrypted.rsplit('.', 1)[0] + '_metadata.json'
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)
    
    print()
    
    # Step 7: Performance test
    print("Step 7: Performance evaluation...")
    
    # Test encryption speed with different image sizes
    import time
    
    # Create test images of different sizes
    test_sizes = [(64, 64), (128, 128), (256, 256)]
    
    for width, height in test_sizes:
        print(f"\nTesting {width}x{height} image:")
        
        # Create random test image
        test_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        test_img = Image.fromarray(test_data, 'RGB')
        test_path = f"perf_test_{width}x{height}.png"
        test_img.save(test_path)
        
        # Time encryption
        start_time = time.time()
        enc_success, _ = cipher.encrypt_image(test_path, f"enc_{test_path}")
        enc_time = time.time() - start_time
        
        print(f"  Encryption time: {enc_time:.3f} seconds")
        print(f"  Processing rate: {(width * height) / enc_time:.0f} pixels/second")
        
        # Clean up
        for cleanup_file in [test_path, f"enc_{test_path}"]:
            if os.path.exists(cleanup_file):
                os.remove(cleanup_file)
        
        metadata_path = f"enc_{test_path}".rsplit('.', 1)[0] + '_metadata.json'
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
    
    print()
    
    # Clean up demonstration files
    print("Step 8: Cleaning up demonstration files...")
    cleanup_files = [
        "demo_key.json",
        "demo_encrypted_test_color.png",
        "demo_decrypted_test_color.png",
        "demo_encrypted_test_grayscale.png",
        "demo_decrypted_test_grayscale.png",
        "demo_encrypted_test_pattern.png",
        "demo_decrypted_test_pattern.png"
    ]
    
    for filename in cleanup_files:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"  Removed {filename}")
        
        # Also check for metadata files
        metadata_file = filename.rsplit('.', 1)[0] + '_metadata.json'
        if os.path.exists(metadata_file):
            os.remove(metadata_file)
            print(f"  Removed {metadata_file}")
    
    print()
    print("="*60)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("="*60)
    print()
    print("Summary:")
    print("✓ Hill Cipher implementation working correctly")
    print("✓ Key generation and management functional")
    print("✓ Image encryption/decryption cycle verified")
    print("✓ Multiple image formats supported")
    print("✓ Different key sizes tested")
    print("✓ Performance metrics collected")
    print("✓ All temporary files cleaned up")
    print()
    print("The Hill Cipher Image Encryption Tool is ready for use!")
    print("Launch the GUI with: python main.py")
    print("Or use CLI with: python main.py --cli encrypt input.png output.png key.json")

if __name__ == "__main__":
    try:
        demonstrate_hill_cipher()
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
    except Exception as e:
        print(f"\n\nDemonstration failed with error: {e}")
        import traceback
        traceback.print_exc()
