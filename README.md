# Image Converter Pro

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Image Converter Pro** is a desktop application built with Python that allows users to convert, edit, and batch process images with a user-friendly graphical interface. It supports various image formats and provides advanced editing features like resizing, rotating, applying filters, adding watermarks, and more.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Batch Processing**: Process multiple images simultaneously with the same settings.
- **Format Conversion**: Convert images between popular formats (JPEG, PNG, BMP, GIF, TIFF, WEBP).
- **Image Editing**:
  - Resize images with optional aspect ratio preservation.
  - Rotate images (90°, 180°, 270°, or custom angles).
  - Adjust brightness, contrast, saturation, and sharpness.
  - Apply filters (Blur, Sharpen, Edge Enhance, Emboss, Contour, Grayscale).
- **Watermarking**: Add custom text watermarks with adjustable position and opacity.
- **Presets**: Save and load processing settings as presets for quick reuse.
- **Rename Options**: Rename output files using customizable patterns during batch processing.
- **Preview**: Preview images before processing.
- **Logging**: Keep track of operations with a detailed log, which can be saved to a file.
- **Modern UI**: Tab-based interface with a clean and intuitive design.

## Screenshots  
![Main Tab](https://github.com/user-attachments/assets/9876c184-580e-4c7e-b56f-e4efd84a1dce)  
![Advanced Effects](https://github.com/user-attachments/assets/4fe20137-e90f-4b3c-b38d-80f55c9ecda0)  
![Batch Processing](https://github.com/user-attachments/assets/8a07b4cd-c71a-438f-aee0-89bce5a32758)  


## Installation

### Prerequisites
- Python 3.7 or higher
- `Pillow` library for image processing
- `tkinter` (usually included with Python)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mpython77/image-converter-pro.git
   cd image-converter-pro
   ```

2. **Install Dependencies**:
   Install the required Python libraries using pip:
   ```bash
   pip install Pillow
   ```

3. **Run the Application**:
   Execute the main script to launch the application:
   ```bash
   python image_converter_pro.py
   ```

## Usage

1. **Launch the Application**:
   Run the script as shown above to open the GUI.

2. **Select Images**:
   - Navigate to the "Main" tab.
   - Click "Select Image(s)" to choose one or more images.
   - Use the listbox to view selected files and click "Preview" to see details of a selected image.

3. **Configure Conversion Settings**:
   - **Format**: Choose the output format (e.g., JPEG, PNG).
   - **Size**: Set the width and height for resizing. Check "Maintain Aspect Ratio" to preserve proportions.
   - **Rotate**: Select a rotation angle or specify a custom angle.
   - **Quality**: Adjust the quality for JPEG/WEBP formats (1-100).

4. **Apply Effects**:
   - In the "Main" tab, adjust basic effects like brightness and contrast.
   - In the "Advanced Effects" tab, apply filters (Blur, Sharpen, etc.), adjust saturation and sharpness, and add a watermark.

5. **Batch Processing** (Optional):
   - Go to the "Batch Processing" tab.
   - Enable renaming and specify a pattern (e.g., `image_{num}`).
   - Save settings as a preset for future use or load a previously saved preset.

6. **Process and Save**:
   - Click "Process and Save" in the "Main" tab.
   - Choose a save directory.
   - Monitor progress via the progress bar and status label.
   - View logs in the "Log" tab to track operations.

7. **Post-Processing**:
   - Click "Open Folder" to view the output directory.
   - Save or clear the log as needed.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.




