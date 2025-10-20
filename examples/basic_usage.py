#!/usr/bin/env python3
"""
SilentCanoe FileForge - Basic Usage Examples
===========================================

This script demonstrates the basic usage of FileForge for common file conversion tasks.
Perfect for getting started with the toolkit!
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path so we can import fileforge
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fileforge import ConversionEngine, BatchProcessor
    print("✅ FileForge modules imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import FileForge: {e}")
    print("💡 Make sure you've installed the requirements: pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Run basic FileForge examples."""
    print("🔧 SilentCanoe FileForge - Basic Examples")
    print("=" * 50)
    
    # Initialize the conversion engine
    engine = ConversionEngine()
    
    # Example 1: Convert a single image (if you have test files)
    print("\n📸 Example 1: Single Image Conversion")
    print("-" * 40)
    
    # Check if we have sample images
    sample_dir = Path(__file__).parent / "sample_files"
    if sample_dir.exists():
        print(f"✅ Sample files directory found: {sample_dir}")
        
        # Look for any image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.heic']
        sample_images = []
        for ext in image_extensions:
            sample_images.extend(sample_dir.glob(f"*{ext}"))
            sample_images.extend(sample_dir.glob(f"*{ext.upper()}"))
        
        if sample_images:
            print(f"📁 Found {len(sample_images)} sample image(s)")
            for img in sample_images[:3]:  # Show first 3
                print(f"   • {img.name}")
        else:
            print("📁 No sample images found")
    else:
        print("📁 No sample files directory found")
        print("💡 You can add sample files to examples/sample_files/ to test conversions")
    
    # Example 2: Demonstrate available formats
    print("\n🎨 Example 2: Supported Formats")
    print("-" * 40)
    
    # Show some supported formats (these would come from the actual converters)
    formats_info = {
        "Images": ["HEIC", "JPG", "PNG", "WebP", "TIFF", "BMP", "GIF", "ICO"],
        "Documents": ["PDF", "DOCX", "XLSX", "PPTX", "TXT", "RTF", "HTML"],
        "Audio": ["MP3", "WAV", "FLAC", "AAC", "OGG", "M4A", "WMA"],
        "Video": ["MP4", "AVI", "MKV", "MOV", "WMV", "FLV", "WebM"]
    }
    
    for category, formats in formats_info.items():
        print(f"📋 {category:12}: {', '.join(formats)}")
    
    # Example 3: CLI Usage Examples
    print("\n💻 Example 3: Command Line Usage")
    print("-" * 40)
    
    cli_examples = [
        ("Convert HEIC to JPG", "python fileforge.py convert image photo.heic photo.jpg --quality 90"),
        ("Batch convert images", "python fileforge.py batch images *.heic --to jpg --recursive"),
        ("Merge PDFs", "python fileforge.py pdf merge file1.pdf file2.pdf merged.pdf"),
        ("Convert audio", "python fileforge.py convert audio song.wav song.mp3 --quality high"),
        ("Launch GUI", "python fileforge.py gui"),
    ]
    
    for description, command in cli_examples:
        print(f"📌 {description}:")
        print(f"   {command}")
        print()
    
    # Example 4: Python API Usage
    print("🐍 Example 4: Python API Usage")
    print("-" * 40)
    
    api_example = '''
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
'''
    print(api_example)
    
    # Example 5: Configuration Tips
    print("⚙️ Example 5: Pro Tips")
    print("-" * 40)
    
    tips = [
        "🚀 Use --threads 8 for faster batch processing on multi-core systems",
        "💾 Add --preserve-metadata to keep EXIF data when converting images",
        "🔒 Use --encrypt password for adding password protection to PDFs",
        "⚡ Set --quality medium for smaller file sizes with good quality",
        "📁 Use --recursive to process subdirectories automatically",
        "🎯 Try --dry-run first to see what would be converted",
        "📊 Use --progress to see detailed conversion progress",
        "🔧 Install FFmpeg for audio/video conversion support"
    ]
    
    for tip in tips:
        print(f"   {tip}")
    
    print("\n" + "=" * 50)
    print("🎉 Ready to start converting! Try the GUI: python fileforge.py gui")
    print("📚 For more help: python fileforge.py --help")
    print("🌐 Visit: https://github.com/koushal13/SilentCanoe-FileForge")

if __name__ == "__main__":
    main()