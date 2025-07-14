# Hill Cipher Image Encryption Tool

This application is used to encrypt and decrypt images using the Hill Cipher algorithm. It provides an easy-to-use graphical user interface (GUI) for everyone, as well as a command-line interface (CLI) for advanced users.

## Main Features
- Encrypt images using the Hill Cipher method
- Decrypt encrypted images
- Supports both color and grayscale images
- Generate your own encryption key
- Available as both GUI and CLI
- Windows .exe version available

## Who Is This App For?
This application is suitable for:
- Beginners who want to try encrypting images easily
- Non-IT users who want to protect their image privacy
- Anyone interested in learning about simple encryption

## How to Use (GUI)
1. Download and run the `HillCipherImageTool.exe` file (see the download link below).
2. Once the app opens, select the image you want to encrypt or decrypt.
3. Choose the operation (Encrypt/Decrypt).
4. Select or create a key file.
5. Click the process button, then save the result.

## How to Use (Python)
If you want to run it with Python:
1. Make sure Python is installed on your computer.
2. Install the dependencies with the command:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the GUI application:
   ```bash
   python main.py
   ```
4. For CLI (command-line) mode:
   ```bash
   python main.py --cli encrypt input.png output.png key.json
   python main.py --cli decrypt encrypted.png decrypted.png key.json
   ```

## Download Application (.exe)
Download the Windows version of the application here:
[Download HillCipherImageTool.exe](https://github.com/FarelGhozali/hill-cipher-image-encryption-tool/raw/main/HillCipherImageTool.exe)

## Contact & Contribution
If you have questions or want to contribute, please open an issue in this repository.

---

**Happy trying and hope it is useful!**
# Hill Cipher Image Encryption Tool

A user-friendly implementation of Hill Cipher for image encryption using Python and cryptography.

## Overview

This project implements the Hill Cipher algorithm for encrypting and decrypting digital images. It provides a comprehensive graphical user interface designed for both technical and non-technical users.

## Features

### Core Functionality
- **Image Encryption/Decryption**: Secure Hill Cipher implementation for various image formats
- **Key Management**: Generate, save, load, and manually enter encryption keys
- **User-Friendly GUI**: Intuitive interface designed for non-IT users
- **Multiple Image Formats**: Support for PNG, JPEG, BMP, TIFF, and GIF
- **Progress Tracking**: Real-time progress indicators for operations

### Analysis Tools
- **Statistical Analysis**: Compare original vs encrypted images
- **Histogram Visualization**: Visual comparison of pixel distributions
- **Entropy Calculation**: Measure encryption randomness and quality
- **Correlation Analysis**: Evaluate encryption effectiveness

### Security Features
- **Invertible Key Generation**: Ensures reliable decryption
- **Metadata Preservation**: Maintains encryption parameters
- **Key Validation**: Verifies key matrix validity
- **Secure Random Key Generation**: Uses cryptographically secure methods

## Installation

### Prerequisites
- Python 3.13 or higher
- Required packages listed in `requirements.txt`

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd path/to/hill-cipher-program
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage Guide

### Encrypting an Image

1. **Select Input Image**
   - Click "Browse" to select your image file
   - Use "Preview" to view the selected image
   - Supported formats: PNG, JPEG, BMP, TIFF, GIF

2. **Set Encryption Key**
   - **Generate Random Key**: Creates a secure random key matrix
   - **Load Key from File**: Use a previously saved key
   - **Enter Manually**: Input your own key matrix

3. **Choose Output Location**
   - Click "Browse" to select where to save the encrypted image
   - The tool automatically saves encryption metadata

4. **Encrypt**
   - Click "Encrypt Image" to start the process
   - Save the key file for later decryption!

### Decrypting an Image

1. **Select Encrypted Image**
   - Browse and select the encrypted image file

2. **Load Decryption Key**
   - Load the key file used for encryption
   - Or use the currently loaded key

3. **Choose Output Location**
   - Select where to save the decrypted image

4. **Decrypt**
   - Click "Decrypt Image" to restore the original

### Key Management

#### Generating Keys
- Navigate to "Key Management" tab
- Select key matrix size (2x2, 3x3, or 4x4)
- Click "Generate Random Key"
- Larger matrices provide stronger encryption

#### Manual Key Entry
- Enter matrix values in the text area
- Format: one row per line, space-separated values
- Example for 2x2 matrix:
  ```
  3 2
  5 7
  ```

#### Saving and Loading Keys
- Save keys to JSON files for future use
- Load previously saved keys
- Keys contain matrix data and metadata

### Image Analysis

#### Statistical Comparison
- Compare original and encrypted images
- View pixel value statistics
- Calculate correlation coefficients
- Assess encryption quality

#### Histogram Analysis
- Visual comparison of pixel distributions
- Side-by-side histogram display
- Supports both color and grayscale images

#### Entropy Calculation
- Measure image randomness
- Higher entropy indicates better encryption
- Maximum entropy: 8.0 bits per pixel

## Technical Details

### Hill Cipher Algorithm

The Hill Cipher is a polygraphic substitution cipher based on linear algebra. For images:

1. **Key Matrix**: An n×n invertible matrix (mod 256)
2. **Block Processing**: Image pixels are processed in blocks
3. **Encryption**: C = (K × P) mod 256
4. **Decryption**: P = (K⁻¹ × C) mod 256

Where:
- K = Key matrix
- P = Plaintext block
- C = Ciphertext block
- K⁻¹ = Inverse key matrix

### Implementation Features

#### Matrix Operations
- Modular arithmetic (mod 256 for 8-bit images)
- Matrix inversion using extended Euclidean algorithm
- Determinant calculation and GCD verification

#### Image Processing
- Multi-channel support (RGB, RGBA, Grayscale)
- Proper padding for block alignment
- Metadata preservation for reliable decryption

#### Security Considerations
- Key matrix invertibility verification
- Cryptographically secure random generation
- Correlation analysis for encryption validation

## File Structure

```
hill-cipher-program/
├── hill_cipher.py          # Core Hill Cipher implementation
├── gui_application.py      # GUI application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── sample_images/         # Test images (if any)
```

## Troubleshooting

### Common Issues

1. **"Matrix not invertible" error**
   - Generate a new random key
   - Ensure manual keys have non-zero determinant

2. **"Import error" messages**
   - Install required packages: `pip install -r requirements.txt`
   - Verify Python version (3.13+)

3. **Decryption produces noise**
   - Verify correct key is loaded
   - Check if metadata file exists
   - Ensure same key used for encryption

4. **Large file processing slow**
   - Normal for large images
   - Progress bars show operation status
   - Consider using smaller images for testing

### Performance Tips

- Use 2x2 keys for faster processing
- PNG format recommended for lossless encryption
- Close other applications for better performance

## Educational Value

This project demonstrates:
- **Linear Algebra**: Matrix operations and modular arithmetic
- **Cryptography**: Symmetric encryption principles
- **Image Processing**: Digital image manipulation
- **Software Engineering**: GUI design and user experience
- **Mathematical Analysis**: Statistical and entropy analysis

## Limitations

- **Block Cipher**: Patterns may be visible in uniform areas
- **Key Security**: Requires secure key distribution
- **Processing Time**: Large images take longer to process
- **Lossless Only**: Works best with lossless image formats

## Future Enhancements

Potential improvements:
- Batch processing capabilities
- Advanced key derivation functions
- Support for video encryption
- Network-based key sharing
- Enhanced statistical analysis

## License

This project is created for educational purposes. Use responsibly and in accordance with applicable laws and regulations.

## Contact

For questions or issues related to this implementation, please refer to the documentation or create an issue in the project repository.
