import numpy as np
from PIL import Image
import os
from typing import Tuple, Optional
import json

class HillCipher:
    """
    Hill Cipher implementation for image encryption/decryption.
    Uses matrix operations to encrypt and decrypt image data.
    """
    
    def __init__(self, key_matrix: np.ndarray = None, block_size: int = 2):
        """
        Initialize Hill Cipher with key matrix and block size.
        
        Args:
            key_matrix: Square matrix for encryption (must be invertible mod 256)
            block_size: Size of the square key matrix (default: 2x2)
        """
        self.block_size = block_size
        self.key_matrix = key_matrix
        self.inverse_key_matrix = None
        
        if key_matrix is not None:
            self.set_key_matrix(key_matrix)
    
    def generate_random_key(self) -> np.ndarray:
        """
        Generate a random invertible key matrix.
        
        Returns:
            Random invertible key matrix
        """
        while True:
            # Generate random matrix with values 0-255
            key = np.random.randint(0, 256, (self.block_size, self.block_size))
            try:
                # Check if matrix is invertible mod 256
                det = int(np.round(np.linalg.det(key))) % 256
                if self.gcd(det, 256) == 1:
                    self.set_key_matrix(key)
                    return key
            except:
                continue
    
    def set_key_matrix(self, key_matrix: np.ndarray) -> bool:
        """
        Set the key matrix and calculate its inverse.
        
        Args:
            key_matrix: Square matrix for encryption
            
        Returns:
            True if key is valid, False otherwise
        """
        try:
            self.key_matrix = key_matrix.astype(int)
            self.inverse_key_matrix = self.matrix_inverse_mod(key_matrix, 256)
            return True
        except Exception as e:
            print(f"Invalid key matrix: {e}")
            return False
    
    def gcd(self, a: int, b: int) -> int:
        """Calculate Greatest Common Divisor."""
        while b:
            a, b = b, a % b
        return a
    
    def mod_inverse(self, a: int, m: int) -> int:
        """Calculate modular inverse of a mod m."""
        if self.gcd(a, m) != 1:
            raise ValueError("Modular inverse does not exist")
        
        # Extended Euclidean Algorithm
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    def matrix_inverse_mod(self, matrix: np.ndarray, mod: int) -> np.ndarray:
        """
        Calculate matrix inverse modulo m.
        
        Args:
            matrix: Input matrix
            mod: Modulus value
            
        Returns:
            Inverse matrix modulo m
        """
        det = int(np.round(np.linalg.det(matrix))) % mod
        det_inv = self.mod_inverse(det, mod)
        
        # Calculate adjugate matrix
        if matrix.shape[0] == 2:
            adjugate = np.array([[matrix[1, 1], -matrix[0, 1]],
                               [-matrix[1, 0], matrix[0, 0]]])
        else:
            # For larger matrices, use cofactor method
            adjugate = np.zeros_like(matrix)
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                    cofactor = ((-1) ** (i + j)) * np.round(np.linalg.det(minor))
                    adjugate[j, i] = cofactor % mod
        
        inverse = (det_inv * adjugate) % mod
        return inverse.astype(int)
    
    def pad_data(self, data: np.ndarray) -> np.ndarray:
        """
        Pad data to make it divisible by block size.
        
        Args:
            data: Input data array
            
        Returns:
            Padded data array
        """
        remainder = len(data) % self.block_size
        if remainder != 0:
            padding = self.block_size - remainder
            data = np.append(data, np.zeros(padding, dtype=data.dtype))
        return data
    
    def encrypt_block(self, block: np.ndarray) -> np.ndarray:
        """
        Encrypt a single block using Hill cipher.
        
        Args:
            block: Input block to encrypt
            
        Returns:
            Encrypted block
        """
        if self.key_matrix is None:
            raise ValueError("Key matrix not set")
        
        encrypted = np.dot(self.key_matrix, block) % 256
        return encrypted.astype(np.uint8)
    
    def decrypt_block(self, block: np.ndarray) -> np.ndarray:
        """
        Decrypt a single block using Hill cipher.
        
        Args:
            block: Input block to decrypt
            
        Returns:
            Decrypted block
        """
        if self.inverse_key_matrix is None:
            raise ValueError("Inverse key matrix not calculated")
        
        decrypted = np.dot(self.inverse_key_matrix, block) % 256
        return decrypted.astype(np.uint8)
    
    def encrypt_image(self, image_path: str, output_path: str) -> Tuple[bool, str]:
        """
        Encrypt an image file.
        
        Args:
            image_path: Path to input image
            output_path: Path to save encrypted image
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Load image
            image = Image.open(image_path)
            image_array = np.array(image)
            original_shape = image_array.shape
            
            # Handle different image modes
            if len(original_shape) == 3:  # Color image
                # Process each channel separately
                encrypted_channels = []
                for channel in range(original_shape[2]):
                    channel_data = image_array[:, :, channel].flatten()
                    channel_data = self.pad_data(channel_data)
                    
                    encrypted_channel = []
                    for i in range(0, len(channel_data), self.block_size):
                        block = channel_data[i:i+self.block_size]
                        encrypted_block = self.encrypt_block(block)
                        encrypted_channel.extend(encrypted_block)
                    
                    encrypted_channels.append(encrypted_channel)
                
                # Reconstruct image
                encrypted_array = np.array(encrypted_channels).T
                encrypted_array = encrypted_array[:np.prod(original_shape[:2])].reshape(original_shape)
                
            else:  # Grayscale image
                flat_data = image_array.flatten()
                flat_data = self.pad_data(flat_data)
                
                encrypted_data = []
                for i in range(0, len(flat_data), self.block_size):
                    block = flat_data[i:i+self.block_size]
                    encrypted_block = self.encrypt_block(block)
                    encrypted_data.extend(encrypted_block)
                
                encrypted_array = np.array(encrypted_data)[:np.prod(original_shape)].reshape(original_shape)
            
            # Save encrypted image
            encrypted_image = Image.fromarray(encrypted_array.astype(np.uint8), mode=image.mode)
            encrypted_image.save(output_path)
            
            # Save metadata
            metadata = {
                'original_shape': original_shape,
                'image_mode': image.mode,
                'block_size': self.block_size,
                'key_matrix': self.key_matrix.tolist()
            }
            
            metadata_path = output_path.rsplit('.', 1)[0] + '_metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f)
            
            return True, "Image encrypted successfully!"
            
        except Exception as e:
            return False, f"Encryption failed: {str(e)}"
    
    def decrypt_image(self, image_path: str, output_path: str, metadata_path: str = None) -> Tuple[bool, str]:
        """
        Decrypt an image file.
        
        Args:
            image_path: Path to encrypted image
            output_path: Path to save decrypted image
            metadata_path: Path to metadata file (optional)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Load metadata
            if metadata_path is None:
                metadata_path = image_path.rsplit('.', 1)[0] + '_metadata.json'
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                original_shape = tuple(metadata['original_shape'])
                image_mode = metadata['image_mode']
            else:
                # Try to decrypt without metadata
                image = Image.open(image_path)
                original_shape = np.array(image).shape
                image_mode = image.mode
            
            # Load encrypted image
            image = Image.open(image_path)
            image_array = np.array(image)
            
            # Decrypt based on image type
            if len(original_shape) == 3:  # Color image
                decrypted_channels = []
                for channel in range(original_shape[2]):
                    channel_data = image_array[:, :, channel].flatten()
                    channel_data = self.pad_data(channel_data)
                    
                    decrypted_channel = []
                    for i in range(0, len(channel_data), self.block_size):
                        block = channel_data[i:i+self.block_size]
                        decrypted_block = self.decrypt_block(block)
                        decrypted_channel.extend(decrypted_block)
                    
                    decrypted_channels.append(decrypted_channel)
                
                # Reconstruct image
                decrypted_array = np.array(decrypted_channels).T
                decrypted_array = decrypted_array[:np.prod(original_shape[:2])].reshape(original_shape)
                
            else:  # Grayscale image
                flat_data = image_array.flatten()
                flat_data = self.pad_data(flat_data)
                
                decrypted_data = []
                for i in range(0, len(flat_data), self.block_size):
                    block = flat_data[i:i+self.block_size]
                    decrypted_block = self.decrypt_block(block)
                    decrypted_data.extend(decrypted_block)
                
                decrypted_array = np.array(decrypted_data)[:np.prod(original_shape)].reshape(original_shape)
            
            # Save decrypted image
            decrypted_image = Image.fromarray(decrypted_array.astype(np.uint8), mode=image_mode)
            decrypted_image.save(output_path)
            
            return True, "Image decrypted successfully!"
            
        except Exception as e:
            return False, f"Decryption failed: {str(e)}"
    
    def save_key(self, filepath: str) -> bool:
        """
        Save the current key matrix to a file.
        
        Args:
            filepath: Path to save the key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.key_matrix is None:
                return False
            
            key_data = {
                'key_matrix': self.key_matrix.tolist(),
                'block_size': self.block_size
            }
            
            with open(filepath, 'w') as f:
                json.dump(key_data, f)
            return True
        except:
            return False
    
    def load_key(self, filepath: str) -> bool:
        """
        Load a key matrix from a file.
        
        Args:
            filepath: Path to the key file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'r') as f:
                key_data = json.load(f)
            
            key_matrix = np.array(key_data['key_matrix'])
            self.block_size = key_data.get('block_size', 2)
            
            return self.set_key_matrix(key_matrix)
        except:
            return False
