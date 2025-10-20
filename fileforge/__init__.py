"""
SilentCanoe FileForge - Universal File Conversion and Manipulation Toolkit

A comprehensive, open-source file processing suite supporting:
- Image conversions (HEIC, JPG, PNG, WebP, TIFF, BMP, GIF, ICO, etc.)
- Document processing (PDF, Word, Excel, PowerPoint, TXT, RTF, etc.)
- Audio/Video conversions (MP3, WAV, FLAC, MP4, AVI, MKV, etc.)
- Batch processing with parallel execution
- Advanced PDF operations (merge, split, compress, encrypt, OCR)
- Archive management (ZIP, RAR, 7Z, TAR)

Created by SilentCanoe - Making file conversion effortless and powerful.
"""

__version__ = "1.0.0"
__author__ = "SilentCanoe"
__license__ = "MIT"
__description__ = "Universal File Conversion and Manipulation Toolkit"

# Core modules
from .core import FileProcessor, BatchProcessor, ConversionEngine
from .utils import *
# from .converters import *

__all__ = [
    'FileProcessor',
    'BatchProcessor', 
    'ConversionEngine',
    '__version__',
    '__author__',
    '__license__'
]