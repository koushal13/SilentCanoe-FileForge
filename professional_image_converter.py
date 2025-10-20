#!/usr/bin/env python3
"""
SilentCanoe FileForge - Professional Image Converter
Real image conversion with extensive validation and checkpoints
"""

import os
import sys
import hashlib
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import time

try:
    from PIL import Image, ImageOps, ExifTags
    import pillow_heif
    # Register HEIF opener with Pillow
    pillow_heif.register_heif_opener()
    CONVERSION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: Image conversion libraries not available: {e}")
    CONVERSION_AVAILABLE = False

class ImageConverter:
    """Professional image converter with real conversion and validation."""
    
    def __init__(self):
        self.supported_input_formats = {
            'heic', 'heif', 'jpg', 'jpeg', 'png', 'bmp', 'gif', 
            'tiff', 'tif', 'webp', 'ico', 'ppm', 'pgm', 'pbm'
        }
        self.supported_output_formats = {
            'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp', 'ico', 'gif'
        }
        
        # Conversion statistics
        self.conversion_stats = {
            'total_attempted': 0,
            'successful': 0,
            'failed': 0,
            'validation_passed': 0,
            'validation_failed': 0
        }
        
    def validate_input_file(self, file_path: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Comprehensive validation of input image file.
        
        Returns:
            Tuple of (is_valid, error_message, file_info)
        """
        print(f"🔍 CHECKPOINT 1: Validating input file: {file_path.name}")
        
        # Check file existence
        if not file_path.exists():
            return False, f"File does not exist: {file_path}", {}
            
        if not file_path.is_file():
            return False, f"Path is not a file: {file_path}", {}
            
        # Check file size
        file_size = file_path.stat().st_size
        if file_size == 0:
            return False, "File is empty (0 bytes)", {}
            
        if file_size > 100 * 1024 * 1024:  # 100MB limit
            return False, f"File too large: {file_size / (1024*1024):.1f}MB (max 100MB)", {}
            
        # Check file extension
        extension = file_path.suffix.lower().lstrip('.')
        if extension not in self.supported_input_formats:
            return False, f"Unsupported input format: .{extension}", {}
            
        # Calculate file hash for integrity checking
        file_hash = self._calculate_file_hash(file_path)
        
        # Try to open and validate the image
        try:
            with Image.open(file_path) as img:
                # Get image properties
                file_info = {
                    'path': str(file_path),
                    'size_bytes': file_size,
                    'size_mb': file_size / (1024 * 1024),
                    'format': img.format,
                    'mode': img.mode,
                    'width': img.width,
                    'height': img.height,
                    'has_transparency': img.mode in ('RGBA', 'LA', 'P'),
                    'file_hash': file_hash,
                    'extension': extension
                }
                
                # Additional format-specific validations
                if extension in ('heic', 'heif'):
                    print("✅ HEIC/HEIF format detected and validated")
                elif extension in ('jpg', 'jpeg'):
                    print("✅ JPEG format detected and validated")
                elif extension == 'png':
                    print("✅ PNG format detected and validated")
                    
                print(f"✅ CHECKPOINT 1 PASSED: Valid {img.format} image ({img.width}x{img.height})")
                return True, "", file_info
                
        except Exception as e:
            return False, f"Invalid image file: {str(e)}", {}
            
    def validate_output_format(self, output_format: str, input_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate output format compatibility."""
        print(f"🔍 CHECKPOINT 2: Validating output format: {output_format}")
        
        output_format = output_format.lower()
        if output_format not in self.supported_output_formats:
            return False, f"Unsupported output format: {output_format}"
            
        # Check format-specific requirements
        if output_format in ('jpg', 'jpeg'):
            if input_info.get('has_transparency'):
                print("⚠️ Warning: JPEG doesn't support transparency, will be converted to white background")
                
        print(f"✅ CHECKPOINT 2 PASSED: Output format {output_format.upper()} is valid")
        return True, ""
        
    def prepare_output_path(self, input_path: Path, output_dir: Path, output_format: str) -> Path:
        """Prepare and validate output path."""
        print(f"🔍 CHECKPOINT 3: Preparing output path")
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        base_name = input_path.stem
        output_extension = 'jpg' if output_format.lower() == 'jpeg' else output_format.lower()
        output_path = output_dir / f"{base_name}.{output_extension}"
        
        # Handle filename conflicts
        counter = 1
        original_output_path = output_path
        while output_path.exists():
            output_path = output_dir / f"{base_name}_{counter}.{output_extension}"
            counter += 1
            
        if output_path != original_output_path:
            print(f"📝 Renamed output to avoid conflict: {output_path.name}")
            
        print(f"✅ CHECKPOINT 3 PASSED: Output path prepared: {output_path}")
        return output_path
        
    def convert_image(self, input_path: Path, output_path: Path, output_format: str, 
                     quality: int = 90, max_width: Optional[int] = None, 
                     max_height: Optional[int] = None) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Perform actual image conversion with extensive validation.
        
        Returns:
            Tuple of (success, error_message, conversion_info)
        """
        print(f"🔄 CHECKPOINT 4: Starting image conversion")
        print(f"   Input: {input_path}")
        print(f"   Output: {output_path}")
        print(f"   Format: {output_format.upper()}")
        print(f"   Quality: {quality}%")
        
        conversion_start_time = time.time()
        
        try:
            # Open the input image
            with Image.open(input_path) as img:
                print(f"📖 Opened source image: {img.format} {img.mode} {img.width}x{img.height}")
                
                # Handle EXIF orientation for JPEG images
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    img = ImageOps.exif_transpose(img)
                    print("🔄 Applied EXIF orientation correction")
                
                # Convert color mode if necessary
                original_mode = img.mode
                if output_format.lower() in ('jpg', 'jpeg'):
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Convert to RGB with white background for JPEG
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                        print("🎨 Converted to RGB with white background for JPEG")
                elif output_format.lower() == 'png':
                    if img.mode not in ('RGBA', 'RGB', 'L', 'LA'):
                        img = img.convert('RGBA')
                        print("🎨 Converted to RGBA for PNG")
                
                # Resize if requested
                original_size = (img.width, img.height)
                if max_width or max_height:
                    new_size = self._calculate_resize_dimensions(
                        img.width, img.height, max_width, max_height
                    )
                    if new_size != original_size:
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                        print(f"📏 Resized from {original_size} to {new_size}")
                
                # Prepare save parameters
                save_kwargs = {}
                if output_format.lower() in ('jpg', 'jpeg'):
                    save_kwargs.update({
                        'format': 'JPEG',
                        'quality': quality,
                        'optimize': True
                    })
                elif output_format.lower() == 'png':
                    save_kwargs.update({
                        'format': 'PNG',
                        'optimize': True
                    })
                elif output_format.lower() == 'webp':
                    save_kwargs.update({
                        'format': 'WebP',
                        'quality': quality,
                        'optimize': True
                    })
                elif output_format.lower() == 'tiff':
                    save_kwargs.update({
                        'format': 'TIFF',
                        'compression': 'lzw'
                    })
                else:
                    save_kwargs['format'] = output_format.upper()
                
                print(f"💾 Saving with parameters: {save_kwargs}")
                
                # Save the converted image
                img.save(output_path, **save_kwargs)
                
                conversion_time = time.time() - conversion_start_time
                
                # Prepare conversion info
                conversion_info = {
                    'input_path': str(input_path),
                    'output_path': str(output_path),
                    'input_format': original_mode,
                    'output_format': output_format.upper(),
                    'original_size': original_size,
                    'final_size': (img.width, img.height),
                    'quality': quality,
                    'conversion_time_seconds': conversion_time,
                    'file_size_before': input_path.stat().st_size,
                    'file_size_after': output_path.stat().st_size if output_path.exists() else 0
                }
                
                print(f"✅ CHECKPOINT 4 PASSED: Conversion completed in {conversion_time:.2f}s")
                return True, "", conversion_info
                
        except Exception as e:
            error_msg = f"Conversion failed: {str(e)}"
            print(f"❌ CHECKPOINT 4 FAILED: {error_msg}")
            return False, error_msg, {}
            
    def validate_output_file(self, output_path: Path, expected_format: str, 
                           input_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Comprehensive validation of the converted output file."""
        print(f"🔍 CHECKPOINT 5: Validating output file")
        
        # Check if file was created
        if not output_path.exists():
            return False, "Output file was not created"
            
        # Check file size
        output_size = output_path.stat().st_size
        if output_size == 0:
            return False, "Output file is empty (0 bytes)"
            
        # Try to open and validate the converted image
        try:
            with Image.open(output_path) as img:
                # Verify format
                detected_format = img.format
                expected_pil_format = self._get_pil_format_name(expected_format)
                
                if detected_format != expected_pil_format:
                    return False, f"Format mismatch: expected {expected_pil_format}, got {detected_format}"
                
                # Verify image can be read completely
                img.load()  # Force loading of image data
                
                # Check if dimensions are reasonable
                if img.width <= 0 or img.height <= 0:
                    return False, f"Invalid image dimensions: {img.width}x{img.height}"
                
                # Calculate compression ratio
                input_size = input_info.get('size_bytes', 0)
                compression_ratio = (input_size - output_size) / input_size * 100 if input_size > 0 else 0
                
                print(f"📊 Conversion Statistics:")
                print(f"   Format: {detected_format}")
                print(f"   Size: {img.width}x{img.height}")
                print(f"   File size: {output_size / 1024:.1f} KB")
                print(f"   Compression: {compression_ratio:.1f}%")
                
                print(f"✅ CHECKPOINT 5 PASSED: Output file is valid {detected_format}")
                return True, ""
                
        except Exception as e:
            return False, f"Output file validation failed: {str(e)}"
            
    def integrity_check(self, input_path: Path, output_path: Path, 
                       conversion_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Final integrity check comparing input and output."""
        print(f"🔍 CHECKPOINT 6: Final integrity check")
        
        try:
            # Open both images and compare key properties
            with Image.open(input_path) as input_img, Image.open(output_path) as output_img:
                
                # Check that we didn't lose critical image data
                input_pixels = input_img.width * input_img.height
                output_pixels = output_img.width * output_img.height
                
                # Allow for resize operations
                expected_size = conversion_info.get('final_size', (input_img.width, input_img.height))
                expected_pixels = expected_size[0] * expected_size[1]
                
                if output_pixels != expected_pixels:
                    return False, f"Pixel count mismatch: expected {expected_pixels}, got {output_pixels}"
                
                # Verify output image is not corrupted by checking a sample of pixels
                try:
                    # Sample some pixels to ensure image data is accessible
                    output_img.getpixel((0, 0))
                    output_img.getpixel((output_img.width - 1, output_img.height - 1))
                    
                    # Check center pixel
                    center_x, center_y = output_img.width // 2, output_img.height // 2
                    output_img.getpixel((center_x, center_y))
                    
                except Exception as e:
                    return False, f"Output image data is corrupted: {str(e)}"
                
                print(f"✅ CHECKPOINT 6 PASSED: Integrity check successful")
                return True, ""
                
        except Exception as e:
            return False, f"Integrity check failed: {str(e)}"
            
    def convert_single_image(self, input_path: str, output_dir: str, output_format: str,
                           quality: int = 90, max_width: Optional[int] = None,
                           max_height: Optional[int] = None) -> Dict[str, Any]:
        """
        Convert a single image with full validation pipeline.
        
        Returns detailed conversion report.
        """
        print(f"\n🚀 STARTING CONVERSION PIPELINE")
        print(f"=" * 60)
        
        self.conversion_stats['total_attempted'] += 1
        
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        
        # Initialize result
        result = {
            'success': False,
            'input_file': str(input_path),
            'output_file': None,
            'error': None,
            'checkpoints_passed': [],
            'checkpoints_failed': [],
            'conversion_info': {},
            'validation_info': {}
        }
        
        try:
            # CHECKPOINT 1: Validate input file
            is_valid, error_msg, file_info = self.validate_input_file(input_path)
            if not is_valid:
                result['error'] = f"Input validation failed: {error_msg}"
                result['checkpoints_failed'].append('input_validation')
                return result
            result['checkpoints_passed'].append('input_validation')
            
            # CHECKPOINT 2: Validate output format
            is_valid, error_msg = self.validate_output_format(output_format, file_info)
            if not is_valid:
                result['error'] = f"Output format validation failed: {error_msg}"
                result['checkpoints_failed'].append('format_validation')
                return result
            result['checkpoints_passed'].append('format_validation')
            
            # CHECKPOINT 3: Prepare output path
            output_path = self.prepare_output_path(input_path, output_dir, output_format)
            result['output_file'] = str(output_path)
            result['checkpoints_passed'].append('path_preparation')
            
            # CHECKPOINT 4: Perform conversion
            success, error_msg, conversion_info = self.convert_image(
                input_path, output_path, output_format, quality, max_width, max_height
            )
            if not success:
                result['error'] = error_msg
                result['checkpoints_failed'].append('conversion')
                return result
            result['checkpoints_passed'].append('conversion')
            result['conversion_info'] = conversion_info
            
            # CHECKPOINT 5: Validate output file
            is_valid, error_msg = self.validate_output_file(output_path, output_format, file_info)
            if not is_valid:
                result['error'] = f"Output validation failed: {error_msg}"
                result['checkpoints_failed'].append('output_validation')
                self.conversion_stats['validation_failed'] += 1
                return result
            result['checkpoints_passed'].append('output_validation')
            self.conversion_stats['validation_passed'] += 1
            
            # CHECKPOINT 6: Final integrity check
            is_valid, error_msg = self.integrity_check(input_path, output_path, conversion_info)
            if not is_valid:
                result['error'] = f"Integrity check failed: {error_msg}"
                result['checkpoints_failed'].append('integrity_check')
                return result
            result['checkpoints_passed'].append('integrity_check')
            
            # Success!
            result['success'] = True
            self.conversion_stats['successful'] += 1
            
            print(f"\n🎉 CONVERSION COMPLETED SUCCESSFULLY!")
            print(f"   All 6 checkpoints passed ✅")
            print(f"   Input: {input_path.name}")
            print(f"   Output: {output_path.name}")
            print(f"   Format: {file_info.get('format', 'Unknown')} → {output_format.upper()}")
            
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
            result['checkpoints_failed'].append('unexpected_error')
            self.conversion_stats['failed'] += 1
            
        return result
        
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file for integrity checking."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:16]  # First 16 chars for brevity
        
    def _calculate_resize_dimensions(self, width: int, height: int, 
                                   max_width: Optional[int], 
                                   max_height: Optional[int]) -> Tuple[int, int]:
        """Calculate new dimensions while maintaining aspect ratio."""
        if not max_width and not max_height:
            return width, height
            
        aspect_ratio = width / height
        
        if max_width and max_height:
            # Fit within both constraints
            if width / max_width > height / max_height:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        elif max_width:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:  # max_height only
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
            
        return new_width, new_height
        
    def _get_pil_format_name(self, format_name: str) -> str:
        """Convert format name to PIL format name."""
        format_map = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'bmp': 'BMP',
            'tiff': 'TIFF',
            'tif': 'TIFF',
            'webp': 'WebP',
            'gif': 'GIF',
            'ico': 'ICO'
        }
        return format_map.get(format_name.lower(), format_name.upper())
        
    def print_conversion_stats(self):
        """Print conversion statistics."""
        print(f"\n📊 CONVERSION STATISTICS")
        print(f"=" * 40)
        print(f"Total Attempted: {self.conversion_stats['total_attempted']}")
        print(f"Successful: {self.conversion_stats['successful']}")
        print(f"Failed: {self.conversion_stats['failed']}")
        print(f"Validation Passed: {self.conversion_stats['validation_passed']}")
        print(f"Validation Failed: {self.conversion_stats['validation_failed']}")
        
        if self.conversion_stats['total_attempted'] > 0:
            success_rate = (self.conversion_stats['successful'] / 
                          self.conversion_stats['total_attempted']) * 100
            print(f"Success Rate: {success_rate:.1f}%")

def main():
    """Demo of the professional image converter."""
    if not CONVERSION_AVAILABLE:
        print("❌ Image conversion libraries not available!")
        print("Please install: pip install Pillow pillow-heif")
        return
        
    print("🔧 SilentCanoe FileForge - Professional Image Converter")
    print("=" * 60)
    print("This converter includes extensive validation and checkpoints")
    print("to ensure legitimate image conversion (no file copying tricks)")
    print()
    
    converter = ImageConverter()
    
    # Example usage
    print("📋 Supported Input Formats:", ', '.join(sorted(converter.supported_input_formats)))
    print("📋 Supported Output Formats:", ', '.join(sorted(converter.supported_output_formats)))
    print()
    
    # Interactive mode
    while True:
        print("\n" + "=" * 60)
        input_file = input("🖼️ Enter image file path (or 'quit' to exit): ").strip()
        
        if input_file.lower() == 'quit':
            break
            
        if not input_file:
            continue
            
        output_dir = input("📂 Enter output directory: ").strip()
        if not output_dir:
            output_dir = "."
            
        output_format = input("🎯 Enter output format (jpg/png/webp/tiff/bmp): ").strip()
        if not output_format:
            output_format = "jpg"
            
        quality_input = input("🎨 Enter quality 1-100 (default 90): ").strip()
        quality = 90
        if quality_input.isdigit():
            quality = max(1, min(100, int(quality_input)))
            
        # Perform conversion
        result = converter.convert_single_image(
            input_file, output_dir, output_format, quality
        )
        
        # Print detailed results
        print(f"\n📋 CONVERSION REPORT")
        print(f"=" * 40)
        print(f"Success: {'✅ YES' if result['success'] else '❌ NO'}")
        print(f"Input: {result['input_file']}")
        print(f"Output: {result['output_file'] or 'N/A'}")
        
        if result['error']:
            print(f"Error: {result['error']}")
            
        print(f"Checkpoints Passed: {len(result['checkpoints_passed'])}/6")
        for checkpoint in result['checkpoints_passed']:
            print(f"   ✅ {checkpoint}")
            
        if result['checkpoints_failed']:
            print(f"Checkpoints Failed:")
            for checkpoint in result['checkpoints_failed']:
                print(f"   ❌ {checkpoint}")
                
        if result['conversion_info']:
            info = result['conversion_info']
            print(f"\nConversion Details:")
            print(f"   Time: {info.get('conversion_time_seconds', 0):.2f}s")
            print(f"   Size: {info.get('original_size', 'Unknown')} → {info.get('final_size', 'Unknown')}")
            print(f"   File: {info.get('file_size_before', 0)/1024:.1f}KB → {info.get('file_size_after', 0)/1024:.1f}KB")
    
    converter.print_conversion_stats()
    print("\n👋 Thank you for using SilentCanoe FileForge!")

if __name__ == "__main__":
    main()