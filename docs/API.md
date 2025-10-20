# 📖 SilentCanoe FileForge API Documentation

Welcome to the comprehensive API documentation for SilentCanoe FileForge - the universal file conversion toolkit.

## 📚 Table of Contents

- [Quick Start](#quick-start)
- [Core API](#core-api)
- [Converters](#converters)
- [CLI Reference](#cli-reference)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Basic Usage
```python
from fileforge import ConversionEngine

# Initialize the engine
engine = ConversionEngine()

# Convert a single file
success = engine.convert_single('input.heic', 'output.jpg')

# Batch convert files
results = engine.convert_batch(
    input_folder='photos',
    output_folder='converted',
    pattern='*.heic',
    output_format='jpg'
)
```

## 🔧 Core API

### ConversionEngine

The main class that orchestrates all file conversions.

```python
class ConversionEngine:
    """Main conversion engine for SilentCanoe FileForge."""
    
    def __init__(self):
        """Initialize the conversion engine."""
        
    def convert_single(
        self, 
        input_path: str, 
        output_path: str, 
        **options
    ) -> bool:
        """
        Convert a single file.
        
        Args:
            input_path: Path to input file
            output_path: Path for output file
            **options: Format-specific options
            
        Returns:
            True if conversion successful, False otherwise
            
        Example:
            >>> engine = ConversionEngine()
            >>> success = engine.convert_single(
            ...     'photo.heic', 
            ...     'photo.jpg',
            ...     quality=90,
            ...     resize=(1920, 1080)
            ... )
        """
        
    def convert_batch(
        self,
        input_folder: str,
        output_folder: str = None,
        pattern: str = "*",
        output_format: str = None,
        recursive: bool = False,
        **options
    ) -> Dict[str, Any]:
        """
        Convert multiple files in batch.
        
        Args:
            input_folder: Input directory path
            output_folder: Output directory path
            pattern: File pattern to match (e.g., "*.heic")
            output_format: Target format (e.g., "jpg")
            recursive: Process subdirectories
            **options: Format-specific options
            
        Returns:
            Dictionary with conversion results
            
        Example:
            >>> results = engine.convert_batch(
            ...     input_folder='photos',
            ...     output_folder='converted',
            ...     pattern='*.heic',
            ...     output_format='jpg',
            ...     quality=85,
            ...     recursive=True
            ... )
            >>> print(f"Converted {results['successful']}/{results['total']} files")
        """
        
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get all supported file formats.
        
        Returns:
            Dictionary mapping format categories to supported extensions
            
        Example:
            >>> formats = engine.get_supported_formats()
            >>> print(formats['image'])  # ['jpg', 'png', 'heic', ...]
        """
        
    def detect_file_type(self, file_path: str) -> str:
        """
        Detect the type of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type ('image', 'document', 'audio', 'video', 'unknown')
            
        Example:
            >>> file_type = engine.detect_file_type('photo.heic')
            >>> print(file_type)  # 'image'
        """
```

### BatchProcessor

Handles batch processing operations with parallel execution.

```python
class BatchProcessor:
    """Batch processor for handling multiple file conversions."""
    
    def __init__(self, max_workers: int = None):
        """
        Initialize batch processor.
        
        Args:
            max_workers: Maximum number of parallel workers
        """
        
    def process_folder(
        self,
        input_folder: str,
        output_folder: str,
        converter_func: callable,
        pattern: str = "*",
        recursive: bool = False,
        progress_callback: callable = None
    ) -> BatchResult:
        """
        Process all files in a folder.
        
        Args:
            input_folder: Source directory
            output_folder: Destination directory
            converter_func: Function to convert each file
            pattern: File pattern to match
            recursive: Process subdirectories
            progress_callback: Callback for progress updates
            
        Returns:
            BatchResult object with processing statistics
            
        Example:
            >>> processor = BatchProcessor(max_workers=4)
            >>> result = processor.process_folder(
            ...     'photos',
            ...     'converted',
            ...     lambda src, dst: engine.convert_single(src, dst, quality=90),
            ...     pattern='*.heic',
            ...     recursive=True
            ... )
        """
```

### FileProcessor

Low-level file processing utilities.

```python
class FileProcessor:
    """Low-level file processing utilities."""
    
    @staticmethod
    def validate_file(file_path: str) -> bool:
        """
        Validate if file exists and is readable.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is valid, False otherwise
        """
        
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """
        Get detailed file information.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file metadata
            
        Example:
            >>> info = FileProcessor.get_file_info('photo.jpg')
            >>> print(info)
            {
                'size': 1024000,
                'format': 'JPEG',
                'dimensions': (1920, 1080),
                'created': '2024-01-15 10:30:00',
                'modified': '2024-01-15 10:30:00'
            }
        """
        
    @staticmethod
    def ensure_directory(dir_path: str) -> bool:
        """
        Ensure directory exists, create if necessary.
        
        Args:
            dir_path: Directory path
            
        Returns:
            True if directory exists/created, False otherwise
        """
```

## 🎨 Converters

### ImageConverter

Handles all image format conversions and processing.

```python
class ImageConverter:
    """Image format converter with advanced processing capabilities."""
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        quality: int = 90,
        resize: tuple = None,
        enhance: dict = None,
        watermark: str = None,
        preserve_metadata: bool = True
    ) -> bool:
        """
        Convert image with optional processing.
        
        Args:
            input_path: Source image path
            output_path: Destination image path
            quality: Output quality (1-100)
            resize: Target size as (width, height)
            enhance: Enhancement settings
            watermark: Watermark text
            preserve_metadata: Keep EXIF data
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> converter = ImageConverter()
            >>> success = converter.convert(
            ...     'photo.heic',
            ...     'photo.jpg',
            ...     quality=90,
            ...     resize=(1920, 1080),
            ...     enhance={'brightness': 1.1, 'contrast': 1.05},
            ...     watermark='© 2024 SilentCanoe'
            ... )
        """
        
    def create_thumbnail(
        self,
        input_path: str,
        output_path: str,
        size: tuple = (300, 300),
        maintain_aspect: bool = True
    ) -> bool:
        """
        Create thumbnail image.
        
        Args:
            input_path: Source image path
            output_path: Thumbnail path
            size: Thumbnail size as (width, height)
            maintain_aspect: Preserve aspect ratio
            
        Returns:
            True if successful, False otherwise
        """
        
    def create_contact_sheet(
        self,
        image_paths: List[str],
        output_path: str,
        grid_size: tuple = None,
        thumbnail_size: tuple = (200, 200)
    ) -> bool:
        """
        Create contact sheet from multiple images.
        
        Args:
            image_paths: List of source image paths
            output_path: Contact sheet output path
            grid_size: Grid layout as (cols, rows)
            thumbnail_size: Size of each thumbnail
            
        Returns:
            True if successful, False otherwise
        """
        
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get supported image formats.
        
        Returns:
            Dictionary with input and output format lists
            
        Example:
            >>> formats = converter.get_supported_formats()
            >>> print(formats['input'])   # ['heic', 'jpg', 'png', ...]
            >>> print(formats['output'])  # ['jpg', 'png', 'webp', ...]
        """
```

### DocumentConverter

Handles document conversions and PDF operations.

```python
class DocumentConverter:
    """Document format converter with PDF manipulation."""
    
    def convert_document(
        self,
        input_path: str,
        output_path: str,
        preserve_formatting: bool = True
    ) -> bool:
        """
        Convert between document formats.
        
        Args:
            input_path: Source document path
            output_path: Destination document path
            preserve_formatting: Maintain original formatting
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> converter = DocumentConverter()
            >>> success = converter.convert_document('report.pdf', 'report.docx')
        """
        
    def merge_pdfs(
        self,
        pdf_paths: List[str],
        output_path: str,
        bookmarks: bool = True
    ) -> bool:
        """
        Merge multiple PDF files.
        
        Args:
            pdf_paths: List of PDF file paths
            output_path: Output merged PDF path
            bookmarks: Include bookmarks in merged file
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> success = converter.merge_pdfs(
            ...     ['file1.pdf', 'file2.pdf', 'file3.pdf'],
            ...     'merged.pdf'
            ... )
        """
        
    def split_pdf(
        self,
        input_path: str,
        output_folder: str,
        page_ranges: List[str] = None
    ) -> bool:
        """
        Split PDF into separate files.
        
        Args:
            input_path: Source PDF path
            output_folder: Destination folder
            page_ranges: List of page ranges (e.g., ['1-5', '10-15'])
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> success = converter.split_pdf(
            ...     'document.pdf',
            ...     'pages/',
            ...     page_ranges=['1-10', '15-20']
            ... )
        """
        
    def compress_pdf(
        self,
        input_path: str,
        output_path: str,
        compression_level: str = 'medium'
    ) -> bool:
        """
        Compress PDF file.
        
        Args:
            input_path: Source PDF path
            output_path: Compressed PDF path
            compression_level: 'low', 'medium', 'high', 'extreme'
            
        Returns:
            True if successful, False otherwise
        """
        
    def encrypt_pdf(
        self,
        input_path: str,
        output_path: str,
        password: str,
        permissions: Dict[str, bool] = None
    ) -> bool:
        """
        Add password protection to PDF.
        
        Args:
            input_path: Source PDF path
            output_path: Encrypted PDF path
            password: Protection password
            permissions: User permissions dictionary
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> success = converter.encrypt_pdf(
            ...     'document.pdf',
            ...     'secure.pdf',
            ...     'mypassword',
            ...     permissions={'print': True, 'modify': False}
            ... )
        """
```

### AudioConverter

Handles audio format conversions and processing.

```python
class AudioConverter:
    """Audio format converter with enhancement capabilities."""
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        quality: str = 'high',
        sample_rate: int = None,
        bitrate: str = None,
        channels: int = None
    ) -> bool:
        """
        Convert audio format.
        
        Args:
            input_path: Source audio path
            output_path: Destination audio path
            quality: Quality preset ('low', 'medium', 'high', 'lossless')
            sample_rate: Target sample rate in Hz
            bitrate: Target bitrate (e.g., '320k', '128k')
            channels: Number of audio channels
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> converter = AudioConverter()
            >>> success = converter.convert(
            ...     'song.flac',
            ...     'song.mp3',
            ...     quality='high',
            ...     bitrate='320k'
            ... )
        """
        
    def normalize_audio(
        self,
        input_path: str,
        output_path: str,
        target_level: float = -23.0
    ) -> bool:
        """
        Normalize audio levels.
        
        Args:
            input_path: Source audio path
            output_path: Normalized audio path
            target_level: Target LUFS level
            
        Returns:
            True if successful, False otherwise
        """
        
    def add_fade(
        self,
        input_path: str,
        output_path: str,
        fade_in: float = 0.0,
        fade_out: float = 0.0
    ) -> bool:
        """
        Add fade in/out effects.
        
        Args:
            input_path: Source audio path
            output_path: Processed audio path
            fade_in: Fade in duration in seconds
            fade_out: Fade out duration in seconds
            
        Returns:
            True if successful, False otherwise
        """
```

### VideoConverter

Handles video format conversions and processing.

```python
class VideoConverter:
    """Video format converter with processing capabilities."""
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        resolution: str = None,
        quality: str = 'medium',
        fps: int = None,
        codec: str = None
    ) -> bool:
        """
        Convert video format.
        
        Args:
            input_path: Source video path
            output_path: Destination video path
            resolution: Target resolution ('480p', '720p', '1080p', '4K')
            quality: Quality preset ('low', 'medium', 'high', 'ultra')
            fps: Target frame rate
            codec: Video codec ('h264', 'h265', 'vp9')
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> converter = VideoConverter()
            >>> success = converter.convert(
            ...     'movie.avi',
            ...     'movie.mp4',
            ...     resolution='1080p',
            ...     quality='high'
            ... )
        """
        
    def create_gif(
        self,
        input_path: str,
        output_path: str,
        start_time: float = 0,
        duration: float = 5,
        fps: int = 10,
        scale: int = 320
    ) -> bool:
        """
        Create animated GIF from video.
        
        Args:
            input_path: Source video path
            output_path: GIF output path
            start_time: Start time in seconds
            duration: Duration in seconds
            fps: Frame rate for GIF
            scale: Width scaling
            
        Returns:
            True if successful, False otherwise
        """
        
    def extract_audio(
        self,
        input_path: str,
        output_path: str,
        audio_format: str = 'mp3'
    ) -> bool:
        """
        Extract audio track from video.
        
        Args:
            input_path: Source video path
            output_path: Audio output path
            audio_format: Output audio format
            
        Returns:
            True if successful, False otherwise
        """
```

## 💻 CLI Reference

### Main Commands

```bash
# Get help
fileforge --help
fileforge <command> --help

# Convert single file
fileforge convert <type> <input> <output> [options]

# Batch convert files
fileforge batch <type> <pattern> [options]

# PDF operations
fileforge pdf <operation> [arguments] [options]

# Get file information
fileforge info <file>

# List supported formats
fileforge formats [type]

# Launch GUI
fileforge gui
```

### Conversion Examples

```bash
# Image conversions
fileforge convert image photo.heic photo.jpg --quality 90
fileforge convert image picture.png picture.webp --quality 85 --resize 1920x1080

# Document conversions
fileforge convert document report.pdf report.docx
fileforge convert document presentation.pptx presentation.pdf

# Audio conversions
fileforge convert audio song.flac song.mp3 --quality high
fileforge convert audio track.wav track.aac --bitrate 256k

# Video conversions
fileforge convert video movie.avi movie.mp4 --resolution 1080p
fileforge convert video clip.mov clip.webm --quality medium
```

### Batch Operations

```bash
# Batch convert images
fileforge batch images *.heic --to jpg --quality 90 --recursive

# Batch convert documents
fileforge batch documents *.docx --to pdf --output converted/

# Batch convert audio files
fileforge batch audio *.flac --to mp3 --quality high --normalize

# Batch convert videos
fileforge batch videos *.mov --to mp4 --resolution 720p --threads 4
```

### PDF Operations

```bash
# Merge PDFs
fileforge pdf merge file1.pdf file2.pdf file3.pdf merged.pdf

# Split PDF
fileforge pdf split document.pdf --pages 1-10,15-20 --output pages/

# Compress PDF
fileforge pdf compress large.pdf small.pdf --level high

# Encrypt PDF
fileforge pdf encrypt document.pdf secure.pdf --password mypassword

# Add watermark
fileforge pdf watermark input.pdf output.pdf "CONFIDENTIAL" --opacity 0.3
```

## 🔧 Configuration

### Quality Presets

```python
QUALITY_PRESETS = {
    'low': {'quality': 60, 'optimize': True},
    'medium': {'quality': 80, 'optimize': True},
    'high': {'quality': 90, 'optimize': False},
    'ultra': {'quality': 95, 'optimize': False},
    'lossless': {'quality': 100, 'lossless': True}
}
```

### Resolution Presets

```python
RESOLUTION_PRESETS = {
    '480p': (854, 480),
    '720p': (1280, 720),
    '1080p': (1920, 1080),
    '1440p': (2560, 1440),
    '4K': (3840, 2160),
    '8K': (7680, 4320)
}
```

## ⚠️ Error Handling

### Exception Classes

```python
class FileForgeError(Exception):
    """Base exception for FileForge operations."""
    pass

class ConversionError(FileForgeError):
    """Raised when file conversion fails."""
    pass

class UnsupportedFormatError(FileForgeError):
    """Raised when file format is not supported."""
    pass

class FileNotFoundError(FileForgeError):
    """Raised when input file doesn't exist."""
    pass

class PermissionError(FileForgeError):
    """Raised when file permissions are insufficient."""
    pass
```

### Error Handling Example

```python
from fileforge import ConversionEngine, ConversionError, UnsupportedFormatError

engine = ConversionEngine()

try:
    success = engine.convert_single('input.heic', 'output.jpg')
except FileNotFoundError:
    print("Input file not found")
except UnsupportedFormatError as e:
    print(f"Unsupported format: {e}")
except ConversionError as e:
    print(f"Conversion failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🏆 Best Practices

### Performance Optimization

```python
# Use appropriate thread count for batch processing
processor = BatchProcessor(max_workers=cpu_count() - 1)

# Process files by size (small files first)
files = sorted(files, key=lambda f: f.stat().st_size)

# Use quality presets for consistent results
engine.convert_single('input.jpg', 'output.webp', quality_preset='web')

# Enable progress callbacks for long operations
def progress_callback(current, total, filename):
    print(f"Processing {current}/{total}: {filename}")

engine.convert_batch(
    'photos/', 
    'converted/', 
    progress_callback=progress_callback
)
```

### Memory Management

```python
# Process large files sequentially
if file_size > 100_000_000:  # 100MB
    processor = BatchProcessor(max_workers=1)

# Clear cache between operations
engine.clear_cache()

# Use streaming for video conversions
converter.convert_video(input_path, output_path, streaming=True)
```

### Error Recovery

```python
# Implement retry logic for network issues
import time
from functools import wraps

def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (2 ** attempt))
            return wrapper
    return decorator

@retry(max_attempts=3)
def convert_with_retry(input_path, output_path):
    return engine.convert_single(input_path, output_path)
```

### Logging Configuration

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fileforge.log'),
        logging.StreamHandler()
    ]
)

# Enable debug logging for troubleshooting
logger = logging.getLogger('fileforge')
logger.setLevel(logging.DEBUG)
```

## 📞 Support

- **GitHub**: [Issues & Discussions](https://github.com/koushal13/SilentCanoe-FileForge)
- **Documentation**: [Full Docs](https://github.com/koushal13/SilentCanoe-FileForge/blob/main/README.md)
- **Website**: [SilentCanoe.com](https://silentcanoe.com)

---

<div align="center">

**Happy Converting! 🚀**

*API Documentation for SilentCanoe FileForge v1.0.0*

</div>