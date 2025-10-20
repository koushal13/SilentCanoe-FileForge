# 🔧 SilentCanoe FileForge

**Universal File Conversion and Manipulation Toolkit**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/silentcanoe/fileforge)

A comprehensive, open-source file processing suite that handles conversion between virtually any file format. Built by [SilentCanoe](https://silentcanoe.com) to make file conversion effortless and powerful.

## ✨ Features

### 🖼️ **Image Processing**
- **Universal Format Support**: HEIC, JPG, PNG, WebP, TIFF, BMP, GIF, ICO, PSD (read), RAW formats
- **Advanced Operations**: Resize, rotate, enhance (contrast/brightness/saturation), blur, watermark
- **Batch Processing**: Convert entire folders recursively
- **Contact Sheets**: Create photo contact sheets automatically
- **Thumbnail Generation**: Batch thumbnail creation with custom sizes

### 📄 **Document Conversion**
- **PDF Operations**: Merge, split, compress, encrypt, OCR, form filling
- **Office Formats**: Word (DOC/DOCX), Excel (XLS/XLSX), PowerPoint (PPT/PPTX)
- **Text Formats**: TXT, RTF, HTML, Markdown, CSV, JSON, XML, YAML
- **Advanced PDF**: Password protection, watermarking, annotations

### 🎵 **Audio Processing**
- **Format Support**: MP3, WAV, FLAC, AAC, OGG, WMA, M4A, OPUS, AIFF
- **Quality Control**: Lossless, high, medium, low quality presets
- **Audio Enhancement**: Volume normalization, fade in/out, channel manipulation
- **Batch Operations**: Convert entire music libraries

### 🎬 **Video Conversion**
- **Format Support**: MP4, AVI, MKV, MOV, WMV, FLV, WebM, 3GP
- **Quality Presets**: Ultra-low to ultra-high quality settings
- **Resolution Control**: 480p, 720p, 1080p, 1440p, 4K scaling
- **Advanced Features**: Compression, watermarking, GIF creation, trimming

### 📦 **Batch Processing Engine**
- **Parallel Processing**: Multi-threaded conversions for speed
- **Recursive Directory Scanning**: Process nested folder structures
- **Progress Tracking**: Real-time progress updates and logging
- **Resume Capability**: Continue interrupted operations
- **Smart Filtering**: Pattern-based file selection

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/silentcanoe/fileforge.git
cd fileforge

# Install dependencies
pip install -r requirements.txt

# Optional: Install external tools for full functionality
# - FFmpeg for audio/video conversion
# - LibreOffice for document conversion
# - Tesseract for OCR capabilities
```

### Usage

#### GUI (Recommended for Beginners)
```bash
python fileforge.py gui
```

#### Command Line Interface
```bash
# Convert single image
python fileforge.py convert image photo.heic photo.jpg --quality 90

# Convert PDF to Word
python fileforge.py convert document report.pdf report.docx

# Batch convert images
python fileforge.py batch images *.heic --to jpg --recursive

# PDF operations
python fileforge.py pdf merge file1.pdf file2.pdf merged.pdf

# Audio conversion
python fileforge.py convert audio song.flac song.mp3 --quality high
```

## 📖 Documentation

### Command Line Reference

#### Convert Commands
```bash
# Image conversion
fileforge convert image input.heic output.jpg --quality 90 --resize 1920x1080

# Document conversion
fileforge convert document doc.pdf doc.docx --password secret

# Audio conversion
fileforge convert audio song.wav song.mp3 --quality high --normalize

# Video conversion
fileforge convert video movie.avi movie.mp4 --resolution 720p --quality medium
```

#### Batch Operations
```bash
# Batch convert with options
fileforge batch /path/to/images --to jpg --recursive --quality 85

# Specific file patterns
fileforge batch /photos --pattern "*.heic" --to png --threads 8
```

#### PDF Operations
```bash
# Merge PDFs
fileforge pdf merge file1.pdf file2.pdf file3.pdf merged.pdf

# Split PDF
fileforge pdf split document.pdf --pages 1-10,15-20

# Compress PDF
fileforge pdf compress large.pdf compressed.pdf --level high

# Encrypt PDF
fileforge pdf encrypt document.pdf secure.pdf --password mypassword

# Add watermark
fileforge pdf watermark input.pdf output.pdf "CONFIDENTIAL" --opacity 0.3
```

### Python API

```python
from fileforge import ConversionEngine

# Initialize engine
engine = ConversionEngine()

# Convert single file
success = engine.convert_single(
    'input.heic', 
    'output.jpg', 
    quality=90,
    resize=(1920, 1080)
)

# Batch conversion
results = engine.convert_batch(
    input_folder='photos',
    output_folder='converted',
    file_pattern='*.heic',
    output_format='jpg',
    recursive=True,
    quality=85
)

print(f"Converted {results['successful']}/{results['total']} files")
```

## 🛠️ Installation & Setup

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 2GB RAM minimum, 4GB recommended
- **Storage**: 100MB for application + space for converted files

### Dependencies

#### Required (Auto-installed)
- `Pillow` - Image processing
- `pillow-heif` - HEIC/HEIF support
- `PyMuPDF` - PDF processing

#### Optional (Manual Installation)
- **FFmpeg** - Audio/video conversion ([Download](https://ffmpeg.org/download.html))
- **LibreOffice** - Office document conversion ([Download](https://www.libreoffice.org/download/))
- **Tesseract OCR** - Text recognition ([Download](https://github.com/tesseract-ocr/tesseract))
- **Pandoc** - Advanced document conversion ([Download](https://pandoc.org/installing.html))

### Platform-Specific Setup

#### Windows
```powershell
# Install using pip
pip install -r requirements.txt

# Optional: Install using Chocolatey
choco install ffmpeg libreoffice pandoc
```

#### macOS
```bash
# Install using Homebrew
brew install ffmpeg libreoffice pandoc tesseract

pip install -r requirements.txt
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt update
sudo apt install ffmpeg libreoffice pandoc tesseract-ocr

pip install -r requirements.txt
```

## 🎯 Use Cases

### 📱 **iPhone Photo Management**
- Convert HEIC photos to JPG for universal compatibility
- Batch process entire photo libraries
- Create thumbnails and contact sheets
- Resize images for web use

### 🏢 **Business Document Processing**
- Convert PDFs to editable Word documents
- Merge multiple documents into single PDFs
- Compress large files for email sharing
- Add watermarks and password protection

### 🎧 **Media Library Organization**
- Convert between audio formats for different devices
- Normalize audio levels across collections
- Extract audio from video files
- Compress media for storage optimization

### 🎬 **Content Creation**
- Convert videos for different platforms
- Create animated GIFs from videos
- Resize videos for social media
- Compress videos for faster uploads

## 🏗️ Architecture

### Project Structure
```
silentcanoe-fileforge/
├── fileforge/
│   ├── __init__.py
│   ├── core.py                 # Core processing engine
│   ├── converters/
│   │   ├── image_converter.py  # Image processing
│   │   ├── document_converter.py # PDF & documents
│   │   ├── audio_converter.py  # Audio processing
│   │   └── video_converter.py  # Video processing
│   ├── gui/
│   │   └── main.py            # GUI interface
│   └── cli/
│       └── main.py            # CLI interface
├── tests/                     # Test suite
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── fileforge.py              # Main entry point
└── requirements.txt          # Dependencies
```

### Key Components

#### **ConversionEngine**
Central orchestrator that handles file type detection and routes conversions to appropriate converters.

#### **BatchProcessor**
Manages parallel processing of multiple files with progress tracking and error handling.

#### **Converter Modules**
Specialized processors for each file type with format-specific optimizations.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/silentcanoe/fileforge.git
cd fileforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Areas for Contribution
- **New Format Support**: Add support for additional file formats
- **Performance Optimization**: Improve conversion speed and memory usage
- **UI/UX Improvements**: Enhance the GUI and user experience
- **Documentation**: Improve docs, examples, and tutorials
- **Testing**: Expand test coverage and add integration tests
- **Internationalization**: Add support for multiple languages

## 📊 Performance

### Benchmarks
- **Image Conversion**: ~5-50 files/second (depending on size and format)
- **Document Processing**: ~1-10 documents/second
- **Audio Conversion**: ~10-100x real-time (depending on quality)
- **Video Processing**: ~0.5-5x real-time (depending on resolution and codec)

### Optimization Tips
- Use SSD storage for better I/O performance
- Increase thread count for batch operations on multi-core systems
- Use appropriate quality settings to balance size and speed
- Enable hardware acceleration when available (GPU encoding)

## 🔧 Troubleshooting

### Common Issues

#### "FFmpeg not found"
- **Solution**: Install FFmpeg and ensure it's in your system PATH
- **Download**: https://ffmpeg.org/download.html

#### "LibreOffice conversion failed"
- **Solution**: Install LibreOffice headless support
- **Command**: `sudo apt install libreoffice --no-install-recommends` (Linux)

#### "Out of memory" errors
- **Solution**: Process files in smaller batches or increase system RAM
- **Alternative**: Use lower quality settings for large files

#### Slow conversion speeds
- **Solution**: 
  - Use faster storage (SSD vs HDD)
  - Increase number of processing threads
  - Use hardware acceleration when available
  - Choose appropriate quality settings

### Debug Mode
```bash
# Enable verbose logging
export FILEFORGE_DEBUG=1
python fileforge.py convert image input.heic output.jpg
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pillow** team for excellent image processing capabilities
- **FFmpeg** project for comprehensive media processing
- **PyMuPDF** for powerful PDF manipulation
- **LibreOffice** for document conversion support
- **Open Source Community** for inspiration and contributions

## 📞 Support

- **Documentation**: [Full Documentation](https://github.com/silentcanoe/fileforge/docs)
- **Issues**: [GitHub Issues](https://github.com/silentcanoe/fileforge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/silentcanoe/fileforge/discussions)
- **Website**: [SilentCanoe.com](https://silentcanoe.com)

---

<p align="center">
  <strong>Made with ❤️ by <a href="https://silentcanoe.com">SilentCanoe</a></strong><br>
  <em>Making file conversion effortless and powerful</em>
</p>