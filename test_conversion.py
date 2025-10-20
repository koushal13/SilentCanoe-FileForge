#!/usr/bin/env python3
"""
Test script to verify image conversion capabilities
Creates test images and converts them to verify everything works
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
    import pillow_heif
    pillow_heif.register_heif_opener()
    LIBS_AVAILABLE = True
except ImportError:
    LIBS_AVAILABLE = False

def create_test_image(path: Path, format_type: str = "PNG"):
    """Create a test image for conversion testing."""
    if not LIBS_AVAILABLE:
        print("❌ PIL not available for test image creation")
        return False
        
    try:
        # Create a 400x300 test image with some content
        img = Image.new('RGB', (400, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Draw some shapes to make it interesting
        draw.rectangle([50, 50, 150, 150], fill='red', outline='darkred', width=3)
        draw.ellipse([200, 50, 350, 200], fill='green', outline='darkgreen', width=3)
        draw.polygon([(200, 250), (250, 200), (300, 250)], fill='yellow', outline='orange', width=3)
        
        # Add text
        draw.text((10, 10), f"Test Image - {format_type}", fill='black')
        draw.text((10, 270), f"Size: {img.width}x{img.height}", fill='black')
        
        # Save the test image
        if format_type.upper() == 'JPEG':
            img.save(path, 'JPEG', quality=90)
        else:
            img.save(path, format_type.upper())
            
        print(f"✅ Created test image: {path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return False

def test_conversion():
    """Test the image conversion system."""
    print("🧪 Testing SilentCanoe FileForge Image Conversion")
    print("=" * 50)
    
    if not LIBS_AVAILABLE:
        print("❌ Required libraries not available!")
        print("Please install: pip install Pillow pillow-heif")
        return
    
    # Create test directory
    test_dir = Path("conversion_test")
    test_dir.mkdir(exist_ok=True)
    
    output_dir = test_dir / "converted"
    output_dir.mkdir(exist_ok=True)
    
    # Create test images in different formats
    test_images = []
    
    # PNG test image
    png_path = test_dir / "test_image.png"
    if create_test_image(png_path, "PNG"):
        test_images.append((png_path, "PNG"))
    
    # JPEG test image  
    jpg_path = test_dir / "test_image.jpg"
    if create_test_image(jpg_path, "JPEG"):
        test_images.append((jpg_path, "JPEG"))
    
    print(f"\n📋 Created {len(test_images)} test images")
    
    # Import our professional converter
    try:
        from professional_image_converter import ImageConverter
        converter = ImageConverter()
        
        print(f"\n🔄 Testing conversions...")
        
        # Test conversions
        test_cases = [
            (png_path, "jpg", "PNG to JPEG"),
            (png_path, "webp", "PNG to WebP"), 
            (jpg_path, "png", "JPEG to PNG"),
            (jpg_path, "tiff", "JPEG to TIFF")
        ]
        
        successful_conversions = 0
        
        for input_path, output_format, description in test_cases:
            if not input_path.exists():
                print(f"⏭️ Skipping {description}: input not available")
                continue
                
            print(f"\n🧪 Testing: {description}")
            print("-" * 30)
            
            result = converter.convert_single_image(
                str(input_path), 
                str(output_dir), 
                output_format,
                quality=85
            )
            
            if result['success']:
                successful_conversions += 1
                print(f"✅ {description} - SUCCESS")
                
                # Verify output file
                output_file = Path(result['output_file'])
                if output_file.exists():
                    file_size = output_file.stat().st_size
                    print(f"   📁 Output: {output_file.name} ({file_size/1024:.1f} KB)")
                else:
                    print(f"   ⚠️ Output file missing: {result['output_file']}")
            else:
                print(f"❌ {description} - FAILED")
                print(f"   Error: {result['error']}")
        
        print(f"\n📊 CONVERSION TEST RESULTS")
        print("=" * 40)
        print(f"Tests attempted: {len(test_cases)}")
        print(f"Successful: {successful_conversions}")
        print(f"Failed: {len(test_cases) - successful_conversions}")
        print(f"Success rate: {(successful_conversions/len(test_cases)*100):.1f}%")
        
        # Show converter statistics
        converter.print_conversion_stats()
        
        # List all output files
        print(f"\n📁 Generated Files:")
        for file in output_dir.glob("*"):
            if file.is_file():
                size = file.stat().st_size
                print(f"   {file.name} ({size/1024:.1f} KB)")
        
        print(f"\n💡 To test HEIC conversion, place a .heic file in the test directory")
        print(f"   and run the professional_image_converter.py interactively")
        
    except ImportError:
        print("❌ Could not import professional_image_converter")
        print("Make sure professional_image_converter.py is in the same directory")

def main():
    """Run the conversion test."""
    print("🔧 SilentCanoe FileForge - Conversion Test Suite")
    print("This will verify that image conversion is working properly")
    print("(No file copying tricks - real conversion with validation)")
    print()
    
    test_conversion()
    
    print(f"\n🎯 To test with your own files:")
    print(f"   python professional_image_converter.py")
    print(f"   python fileforge_converter.py")

if __name__ == "__main__":
    main()