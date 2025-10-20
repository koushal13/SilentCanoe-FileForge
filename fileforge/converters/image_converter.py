"""
Universal Image Converter for SilentCanoe FileForge

Supports conversion between all major image formats including:
- HEIC/HEIF (iPhone photos)
- JPG/JPEG (standard photos)
- PNG (lossless, transparency)
- WebP (modern web format)
- TIFF (high quality)
- BMP (Windows bitmap)
- GIF (animations)
- ICO (icons)
- PSD (Photoshop - read only)
- RAW formats (camera files)
- SVG (vector graphics)
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pillow_heif

# Register HEIF support
pillow_heif.register_heif_opener()

logger = logging.getLogger(__name__)

class ImageConverter:
    """Comprehensive image format converter"""
    
    # Supported input formats
    SUPPORTED_INPUT = {
        '.heic', '.heif', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif',
        '.webp', '.gif', '.ico', '.psd', '.svg'
    }
    
    # Supported output formats
    SUPPORTED_OUTPUT = {
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
    
    # Format-specific default options
    DEFAULT_OPTIONS = {
        'JPEG': {'quality': 90, 'optimize': True, 'progressive': True},
        'PNG': {'optimize': True, 'compress_level': 6},
        'WebP': {'quality': 85, 'method': 6, 'lossless': False},
        'TIFF': {'compression': 'lzw'},
        'GIF': {'optimize': True, 'save_all': True},
        'ICO': {'sizes': [(16, 16), (32, 32), (48, 48), (64, 64)]},
        'BMP': {}
    }
    
    def __init__(self):
        self.setup_pillow_options()
    
    def setup_pillow_options(self):
        """Configure PIL/Pillow for optimal performance"""
        # Increase maximum image pixels for large images
        Image.MAX_IMAGE_PIXELS = 933120000  # ~30k x 30k pixels
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats"""
        return list(self.SUPPORTED_OUTPUT.keys())
    
    def get_image_info(self, image_path: Path) -> Dict[str, Any]:
        """Get detailed information about an image"""
        try:
            with Image.open(image_path) as img:
                info = {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info,
                    'animated': getattr(img, 'is_animated', False),
                    'frames': getattr(img, 'n_frames', 1)
                }
                
                # Add EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    info['has_exif'] = True
                else:
                    info['has_exif'] = False
                
                return info
        except Exception as e:
            logger.error(f"Failed to get image info for {image_path}: {e}")
            return {}
    
    def convert(self, input_path: Path, output_path: Path, **options) -> bool:
        """
        Convert an image to another format
        
        Args:
            input_path: Source image file
            output_path: Destination image file
            **options: Conversion options
        
        Options:
            quality: JPEG/WebP quality (1-100)
            resize: Tuple (width, height) or 'auto'
            rotate: Rotation angle in degrees
            enhance_contrast: Contrast factor (1.0 = no change)
            enhance_brightness: Brightness factor (1.0 = no change)
            enhance_saturation: Saturation factor (1.0 = no change)
            enhance_sharpness: Sharpness factor (1.0 = no change)
            blur: Blur radius
            preserve_metadata: Keep EXIF data (default: True)
            progressive: Progressive JPEG (default: True)
            lossless: Lossless WebP (default: False)
            optimize: Optimize file size (default: True)
        """
        try:
            # Determine output format
            output_ext = output_path.suffix.lower().lstrip('.')
            if output_ext not in self.SUPPORTED_OUTPUT:
                raise ValueError(f"Unsupported output format: {output_ext}")
            
            pil_format = self.SUPPORTED_OUTPUT[output_ext]
            
            # Open and process image
            with Image.open(input_path) as img:
                # Convert mode if necessary
                processed_img = self._prepare_image(img, pil_format, options)
                
                # Apply transformations
                processed_img = self._apply_transformations(processed_img, options)
                
                # Prepare save options
                save_options = self._prepare_save_options(pil_format, options)
                
                # Handle special cases
                if pil_format == 'ICO':
                    self._save_ico(processed_img, output_path, save_options)
                elif pil_format == 'GIF' and getattr(img, 'is_animated', False):
                    self._save_animated_gif(img, output_path, save_options)
                else:
                    # Standard save
                    processed_img.save(output_path, pil_format, **save_options)
                
                logger.info(f"Converted {input_path.name} to {output_path.name}")
                return True
                
        except Exception as e:
            logger.error(f"Conversion failed for {input_path}: {e}")
            return False
    
    def _prepare_image(self, img: Image.Image, target_format: str, options: Dict[str, Any]) -> Image.Image:
        """Prepare image for conversion (handle color modes, etc.)"""
        
        # Handle transparency based on target format
        if target_format in ('JPEG', 'BMP'):
            # These formats don't support transparency
            if img.mode in ('RGBA', 'LA'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                else:
                    background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode == 'P' and 'transparency' in img.info:
                # Convert palette mode with transparency
                img = img.convert('RGBA')
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                img = img.convert('RGB')
        
        elif target_format in ('PNG', 'WebP', 'TIFF'):
            # These formats support transparency
            if img.mode not in ('RGBA', 'RGB', 'L', 'LA'):
                if img.mode == 'P':
                    img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')
                else:
                    img = img.convert('RGBA')
        
        elif target_format == 'GIF':
            # GIF has limited color palette
            if img.mode not in ('P', 'L'):
                img = img.convert('P', palette=Image.ADAPTIVE)
        
        return img
    
    def _apply_transformations(self, img: Image.Image, options: Dict[str, Any]) -> Image.Image:
        """Apply image transformations"""
        
        # Resize
        if 'resize' in options:
            resize_option = options['resize']
            if isinstance(resize_option, (list, tuple)) and len(resize_option) == 2:
                img = img.resize(resize_option, Image.Resampling.LANCZOS)
            elif resize_option == 'auto':
                # Auto-resize large images
                max_size = options.get('max_size', 1920)
                if max(img.size) > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Rotate
        if 'rotate' in options:
            angle = options['rotate']
            img = img.rotate(angle, expand=True)
        
        # Auto-orient based on EXIF
        if options.get('auto_orient', True):
            img = ImageOps.exif_transpose(img)
        
        # Enhance contrast
        if 'enhance_contrast' in options:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(options['enhance_contrast'])
        
        # Enhance brightness
        if 'enhance_brightness' in options:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(options['enhance_brightness'])
        
        # Enhance saturation
        if 'enhance_saturation' in options:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(options['enhance_saturation'])
        
        # Enhance sharpness
        if 'enhance_sharpness' in options:
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(options['enhance_sharpness'])
        
        # Apply blur
        if 'blur' in options:
            blur_radius = options['blur']
            img = img.filter(ImageFilter.GaussianBlur(blur_radius))
        
        return img
    
    def _prepare_save_options(self, pil_format: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare format-specific save options"""
        
        # Start with defaults
        save_options = self.DEFAULT_OPTIONS.get(pil_format, {}).copy()
        
        # Override with user options
        if pil_format == 'JPEG':
            if 'quality' in options:
                save_options['quality'] = max(1, min(100, int(options['quality'])))
            if 'progressive' in options:
                save_options['progressive'] = options['progressive']
            if 'optimize' in options:
                save_options['optimize'] = options['optimize']
        
        elif pil_format == 'PNG':
            if 'optimize' in options:
                save_options['optimize'] = options['optimize']
            if 'compress_level' in options:
                save_options['compress_level'] = max(0, min(9, int(options['compress_level'])))
        
        elif pil_format == 'WebP':
            if 'quality' in options:
                save_options['quality'] = max(1, min(100, int(options['quality'])))
            if 'lossless' in options:
                save_options['lossless'] = options['lossless']
            if 'method' in options:
                save_options['method'] = max(0, min(6, int(options['method'])))
        
        elif pil_format == 'TIFF':
            if 'compression' in options:
                save_options['compression'] = options['compression']
        
        elif pil_format == 'GIF':
            if 'optimize' in options:
                save_options['optimize'] = options['optimize']
        
        # Handle metadata preservation
        if options.get('preserve_metadata', True) and pil_format in ('JPEG', 'TIFF'):
            save_options['exif'] = options.get('exif_data', b'')
        
        return save_options
    
    def _save_ico(self, img: Image.Image, output_path: Path, save_options: Dict[str, Any]):
        """Save image as ICO with multiple sizes"""
        sizes = save_options.get('sizes', [(16, 16), (32, 32), (48, 48)])
        
        # Create images at different sizes
        images = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            if resized.mode != 'RGBA':
                resized = resized.convert('RGBA')
            images.append(resized)
        
        # Save as ICO
        images[0].save(output_path, 'ICO', sizes=[img.size for img in images])
    
    def _save_animated_gif(self, img: Image.Image, output_path: Path, save_options: Dict[str, Any]):
        """Save animated GIF preserving animation"""
        frames = []
        
        try:
            for frame_num in range(img.n_frames):
                img.seek(frame_num)
                frame = img.copy()
                if frame.mode != 'P':
                    frame = frame.convert('P', palette=Image.ADAPTIVE)
                frames.append(frame)
            
            # Save animated GIF
            frames[0].save(
                output_path,
                'GIF',
                save_all=True,
                append_images=frames[1:],
                duration=img.info.get('duration', 100),
                loop=img.info.get('loop', 0),
                optimize=save_options.get('optimize', True)
            )
        except Exception as e:
            logger.warning(f"Failed to save as animated GIF, saving first frame: {e}")
            img.seek(0)
            img.save(output_path, 'GIF', **save_options)
    
    def batch_convert(self, input_folder: Path, output_folder: Path, 
                     output_format: str, recursive: bool = True, **options) -> List[Dict[str, Any]]:
        """Convert multiple images in a folder"""
        results = []
        
        # Find all supported image files
        pattern = "**/*" if recursive else "*"
        for input_file in input_folder.glob(pattern):
            if input_file.is_file() and input_file.suffix.lower() in self.SUPPORTED_INPUT:
                
                # Generate output path
                relative_path = input_file.relative_to(input_folder)
                output_file = output_folder / relative_path.with_suffix(f'.{output_format}')
                
                # Ensure output directory exists
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Convert
                success = self.convert(input_file, output_file, **options)
                
                results.append({
                    'input': str(input_file),
                    'output': str(output_file),
                    'success': success
                })
        
        return results
    
    def create_thumbnail(self, input_path: Path, output_path: Path, 
                        size: Tuple[int, int] = (256, 256), **options) -> bool:
        """Create a thumbnail of an image"""
        options['resize'] = size
        options['quality'] = options.get('quality', 85)
        return self.convert(input_path, output_path, **options)
    
    def create_contact_sheet(self, image_paths: List[Path], output_path: Path,
                           grid_size: Tuple[int, int] = None, 
                           thumbnail_size: Tuple[int, int] = (200, 200)) -> bool:
        """Create a contact sheet from multiple images"""
        try:
            if not image_paths:
                return False
            
            # Determine grid size
            if grid_size is None:
                import math
                count = len(image_paths)
                cols = math.ceil(math.sqrt(count))
                rows = math.ceil(count / cols)
                grid_size = (cols, rows)
            
            cols, rows = grid_size
            thumb_w, thumb_h = thumbnail_size
            
            # Create contact sheet
            sheet_width = cols * thumb_w
            sheet_height = rows * thumb_h
            sheet = Image.new('RGB', (sheet_width, sheet_height), 'white')
            
            for i, img_path in enumerate(image_paths[:cols * rows]):
                if not img_path.exists():
                    continue
                
                try:
                    with Image.open(img_path) as img:
                        # Create thumbnail
                        img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                        
                        # Calculate position
                        col = i % cols
                        row = i // cols
                        x = col * thumb_w + (thumb_w - img.width) // 2
                        y = row * thumb_h + (thumb_h - img.height) // 2
                        
                        # Paste thumbnail
                        sheet.paste(img, (x, y))
                
                except Exception as e:
                    logger.warning(f"Failed to add {img_path} to contact sheet: {e}")
            
            # Save contact sheet
            sheet.save(output_path, 'JPEG', quality=90, optimize=True)
            return True
            
        except Exception as e:
            logger.error(f"Failed to create contact sheet: {e}")
            return False