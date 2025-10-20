"""Utility functions for SilentCanoe FileForge."""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

def get_file_extension(file_path: str) -> str:
    """Get file extension from path."""
    return Path(file_path).suffix.lower().lstrip('.')

def ensure_directory(dir_path: str) -> bool:
    """Ensure directory exists, create if necessary."""
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

def validate_file(file_path: str) -> bool:
    """Validate if file exists and is readable."""
    try:
        path = Path(file_path)
        return path.exists() and path.is_file() and os.access(path, os.R_OK)
    except Exception:
        return False

def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    try:
        return Path(file_path).stat().st_size
    except Exception:
        return 0

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def get_supported_formats() -> Dict[str, List[str]]:
    """Get all supported file formats."""
    return {
        'image': ['heic', 'jpg', 'jpeg', 'png', 'webp', 'tiff', 'bmp', 'gif', 'ico'],
        'document': ['pdf', 'docx', 'xlsx', 'pptx', 'txt', 'rtf', 'html', 'md'],
        'audio': ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'wma'],
        'video': ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', '3gp']
    }

def detect_file_type(file_path: str) -> str:
    """Detect file type based on extension."""
    ext = get_file_extension(file_path)
    formats = get_supported_formats()
    
    for file_type, extensions in formats.items():
        if ext in extensions:
            return file_type
    
    return 'unknown'