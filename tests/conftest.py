"""Test configuration and fixtures for SilentCanoe FileForge."""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator

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
    from PIL import Image
    
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