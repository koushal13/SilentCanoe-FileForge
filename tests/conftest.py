"""Test configuration and fixtures for SilentCanoe FileForge."""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator
from unittest.mock import Mock, MagicMock

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def sample_image_files(temp_dir: Path) -> dict:
    """Create sample image files for testing."""
    try:
        from PIL import Image
    except ImportError:
        pytest.skip("PIL not available for image tests")
    
    files = {}
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    
    # Save in different formats
    jpg_path = temp_dir / "test.jpg"
    png_path = temp_dir / "test.png"
    
    img.save(jpg_path, 'JPEG')
    img.save(png_path, 'PNG')
    
    files['jpg'] = jpg_path
    files['png'] = png_path
    
    return files

@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create a sample text file."""
    text_file = temp_dir / "sample.txt"
    text_file.write_text("This is a sample text file for testing.")
    return text_file

@pytest.fixture
def mock_file_processor():
    """Mock FileProcessor for unit tests."""
    mock = Mock()
    mock.detect_file_type.return_value = 'image'
    mock.convert_single.return_value = True
    mock.get_supported_formats.return_value = {
        'image': ['jpg', 'png', 'heic', 'webp'],
        'document': ['pdf', 'docx', 'txt'],
        'audio': ['mp3', 'wav', 'flac'],
        'video': ['mp4', 'avi', 'mkv']
    }
    return mock

@pytest.fixture
def mock_converter():
    """Mock converter for testing."""
    mock = Mock()
    mock.can_convert.return_value = True
    mock.convert.return_value = True
    mock.get_info.return_value = {
        'format': 'jpg',
        'size': (1920, 1080),
        'file_size': 1024000
    }
    return mock

@pytest.fixture 
def sample_files_structure(temp_dir: Path) -> dict:
    """Create a complete sample file structure for testing."""
    structure = {
        'root': temp_dir,
        'images': temp_dir / 'images',
        'documents': temp_dir / 'documents', 
        'audio': temp_dir / 'audio',
        'video': temp_dir / 'video',
        'output': temp_dir / 'output'
    }
    
    # Create directories
    for folder in structure.values():
        if isinstance(folder, Path):
            folder.mkdir(exist_ok=True)
    
    # Create sample files
    sample_files = {}
    
    # Text files
    (structure['documents'] / 'sample.txt').write_text("Sample text content")
    (structure['documents'] / 'readme.md').write_text("# Sample Markdown")
    
    # Mock image files (just empty files with correct extensions)
    image_files = ['photo.jpg', 'image.png', 'picture.heic', 'graphic.webp']
    for filename in image_files:
        (structure['images'] / filename).write_bytes(b'fake_image_data')
        sample_files[filename] = structure['images'] / filename
    
    # Mock audio files
    audio_files = ['song.mp3', 'track.wav', 'music.flac']
    for filename in audio_files:
        (structure['audio'] / filename).write_bytes(b'fake_audio_data')
        sample_files[filename] = structure['audio'] / filename
    
    # Mock video files  
    video_files = ['movie.mp4', 'clip.avi', 'video.mkv']
    for filename in video_files:
        (structure['video'] / filename).write_bytes(b'fake_video_data')
        sample_files[filename] = structure['video'] / filename
    
    structure['files'] = sample_files
    return structure