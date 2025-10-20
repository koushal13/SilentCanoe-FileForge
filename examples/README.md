# 📚 SilentCanoe FileForge Examples

This directory contains example scripts and sample files to help you get started with SilentCanoe FileForge quickly and effectively.

## 📁 Directory Structure

```
examples/
├── README.md                 # This file
├── basic_usage.py           # Getting started examples
├── advanced_usage.py        # Advanced workflows and automation
├── sample_files/            # Sample files for testing (create this folder)
├── scripts/                 # Utility and automation scripts
└── workflows/               # Pre-configured workflow examples
```

## 🚀 Quick Start

### 1. Basic Examples
```bash
# Run basic examples to understand core functionality
cd examples
python basic_usage.py
```

### 2. Advanced Examples  
```bash
# Explore advanced workflows and automation
python advanced_usage.py
```

### 3. Test with Sample Files
```bash
# Create sample files directory
mkdir sample_files

# Add some test files (HEIC, PDF, etc.) to sample_files/
# Then run the examples to see FileForge in action
```

## 🎯 Example Categories

### 📸 **Image Processing Examples**
- HEIC to JPG conversion with quality settings
- Batch image resizing and optimization
- Adding watermarks and enhancements
- Creating contact sheets and thumbnails
- RAW image processing workflows

### 📄 **Document Processing Examples**
- PDF merging and splitting workflows
- Document format conversions (Word, Excel, PowerPoint)
- PDF compression and optimization
- Adding security and watermarks
- OCR text extraction

### 🎵 **Audio Processing Examples**
- Audio format conversions with quality presets
- Audio enhancement (normalize, fade, effects)
- Batch music library conversions
- Extracting audio from video files
- Podcast processing workflows

### 🎬 **Video Processing Examples**
- Video format conversions for different platforms
- Resolution scaling and compression
- Creating animated GIFs from videos
- Video merging and splitting
- Social media optimization workflows

### 🔄 **Batch Processing Examples**
- Recursive directory processing
- Pattern-based file selection
- Parallel processing optimization
- Progress tracking and logging
- Resume interrupted operations

### 🤖 **Automation Examples**
- Watch folder automation scripts
- Scheduled conversion tasks
- Custom workflow creation
- Integration with other tools
- Error handling and notifications

## 💻 Code Examples

### Simple Conversion
```python
from fileforge import ConversionEngine

engine = ConversionEngine()

# Convert HEIC to JPG
success = engine.convert_single(
    'photo.heic', 
    'photo.jpg', 
    quality=90
)
```

### Batch Processing
```python
from fileforge import BatchProcessor

processor = BatchProcessor()

# Convert all HEIC files in a folder
results = processor.process_folder(
    input_folder='photos',
    output_folder='converted',
    pattern='*.heic',
    output_format='jpg',
    quality=85,
    recursive=True
)

print(f"Converted {results.successful}/{results.total} files")
```

### PDF Operations
```python
from fileforge.converters import DocumentConverter

converter = DocumentConverter()

# Merge PDFs
converter.merge_pdfs(
    ['file1.pdf', 'file2.pdf', 'file3.pdf'],
    'merged.pdf'
)

# Compress PDF
converter.compress_pdf('large.pdf', 'small.pdf', level='high')
```

## 🛠️ CLI Examples

### Image Conversion
```bash
# Convert single image with quality setting
python fileforge.py convert image photo.heic photo.jpg --quality 90

# Batch convert with resizing
python fileforge.py batch images photos/ --to jpg --resize 1920x1080 --quality 85
```

### PDF Processing
```bash
# Merge multiple PDFs
python fileforge.py pdf merge file1.pdf file2.pdf file3.pdf merged.pdf

# Split PDF by page ranges
python fileforge.py pdf split document.pdf --pages 1-10,15-20
```

### Audio/Video Conversion
```bash
# Convert audio with high quality
python fileforge.py convert audio song.flac song.mp3 --quality high

# Convert video for YouTube
python fileforge.py convert video raw.mov youtube.mp4 --resolution 1080p
```

## 🎨 Workflow Templates

### Content Creator Workflow
```bash
#!/bin/bash
# Process raw footage for multiple platforms

# YouTube (1080p, high quality)
python fileforge.py convert video raw_footage.mov youtube.mp4 \
    --resolution 1080p --quality high --watermark "Creator Name"

# Instagram (720p, optimized)
python fileforge.py convert video raw_footage.mov instagram.mp4 \
    --resolution 720p --quality medium --aspect-ratio 1:1

# Extract audio for podcast
python fileforge.py convert audio raw_footage.mov podcast.mp3 \
    --quality high --normalize --fade-in 0.5 --fade-out 1.0
```

### Photographer Workflow
```bash
#!/bin/bash
# Process RAW photos from shoot

# Convert HEIC to JPG with enhancement
python fileforge.py batch images raw_photos/ \
    --to jpg --quality 95 --resize 3840x2160 \
    --enhance brightness=1.1,contrast=1.05 \
    --watermark "© Photographer 2024" --preserve-metadata

# Create web-optimized versions
python fileforge.py batch images converted/ \
    --to jpg --quality 75 --resize 1920x1080 \
    --output web_gallery/ --create-thumbnails
```

### Office Document Workflow
```bash
#!/bin/bash
# Process business documents

# Convert Word docs to PDF
python fileforge.py batch documents contracts/ \
    --from docx --to pdf --preserve-formatting

# Merge all contracts into one PDF
python fileforge.py pdf merge contracts/*.pdf all_contracts.pdf

# Add password protection
python fileforge.py pdf encrypt all_contracts.pdf secure_contracts.pdf \
    --password "SecurePassword123"
```

## 🔧 Custom Scripts

### Daily Automation Script
```python
#!/usr/bin/env python3
"""Daily file processing automation."""

import schedule
import time
from pathlib import Path
from fileforge import ConversionEngine

def process_daily_files():
    """Process files in watch folders."""
    engine = ConversionEngine()
    
    # Process incoming photos
    photos_folder = Path("~/Desktop/Photos_Inbox").expanduser()
    if photos_folder.exists():
        engine.batch_convert(
            photos_folder,
            output_folder="~/Pictures/Processed",
            pattern="*.heic",
            output_format="jpg",
            quality=90
        )
    
    # Process incoming documents
    docs_folder = Path("~/Desktop/Docs_Inbox").expanduser()
    if docs_folder.exists():
        engine.batch_convert(
            docs_folder,
            output_folder="~/Documents/Processed", 
            pattern="*.docx",
            output_format="pdf"
        )

# Schedule daily processing
schedule.every().day.at("09:00").do(process_daily_files)
schedule.every().day.at("17:00").do(process_daily_files)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
```

## 📊 Performance Benchmarks

### Typical Processing Speeds
- **Image Conversion**: 5-50 files/second (depending on size and format)
- **PDF Operations**: 1-10 documents/second
- **Audio Conversion**: 10-100x real-time
- **Video Processing**: 0.5-5x real-time

### Optimization Tips
```python
# Optimal settings for different scenarios

# Fast preview generation
engine.convert_single(
    'input.heic', 'preview.jpg',
    quality=60,  # Lower quality for speed
    resize=(800, 600)  # Smaller size
)

# High-quality archival
engine.convert_single(
    'input.heic', 'archive.jpg', 
    quality=95,  # Maximum quality
    preserve_metadata=True
)

# Balanced web optimization  
engine.convert_single(
    'input.heic', 'web.jpg',
    quality=85,  # Good quality/size balance
    resize=(1920, 1080),
    progressive=True  # Progressive JPEG
)
```

## 🤝 Contributing Examples

Have a useful workflow or script? Contribute it!

1. **Fork the repository**
2. **Add your example** to the appropriate category
3. **Include documentation** and comments
4. **Test thoroughly** on different platforms
5. **Submit a pull request**

### Example Template
```python
#!/usr/bin/env python3
"""
Your Example Name
================

Brief description of what this example demonstrates.

Requirements:
- List any special requirements
- External dependencies
- Sample files needed

Usage:
    python your_example.py [options]
"""

def your_example_function():
    """
    Detailed description of the function.
    
    Returns:
        Description of return value
    """
    # Your code here
    pass

if __name__ == "__main__":
    your_example_function()
```

## 🆘 Need Help?

- **Issues**: [GitHub Issues](https://github.com/koushal13/SilentCanoe-FileForge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/koushal13/SilentCanoe-FileForge/discussions)
- **Documentation**: [Full Documentation](https://github.com/koushal13/SilentCanoe-FileForge/blob/main/README.md)
- **Website**: [SilentCanoe.com](https://silentcanoe.com)

---

<div align="center">

**Happy Converting! 🚀**

*Made with ❤️ by [SilentCanoe](https://silentcanoe.com)*

</div>