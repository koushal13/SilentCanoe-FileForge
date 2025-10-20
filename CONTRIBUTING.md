# Contributing to SilentCanoe FileForge

Thank you for your interest in contributing to SilentCanoe FileForge! We welcome contributions from developers of all skill levels.

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git for version control
- Basic understanding of file processing concepts

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/fileforge.git
   cd fileforge
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Verify Installation**
   ```bash
   python fileforge.py --help
   pytest tests/
   ```

## 🎯 Areas for Contribution

### High Priority
- **New Format Support**: Add converters for additional file types
- **Performance Optimization**: Improve conversion speed and memory usage
- **Cross-Platform Testing**: Ensure compatibility across Windows, macOS, Linux
- **Error Handling**: Improve error messages and recovery mechanisms

### Medium Priority
- **GUI Improvements**: Enhance user interface and user experience
- **Documentation**: Improve examples, tutorials, and API documentation
- **Internationalization**: Add support for multiple languages
- **Plugin System**: Create extensible architecture for third-party converters

### Ongoing
- **Bug Fixes**: Fix reported issues and edge cases
- **Code Quality**: Improve code organization and maintainability
- **Test Coverage**: Expand automated testing
- **Security**: Address security considerations

## 📝 Contribution Types

### 🐛 Bug Reports
- Use the issue template
- Include system information (OS, Python version)
- Provide minimal reproduction steps
- Include error messages and logs

### ✨ Feature Requests
- Check existing issues first
- Explain the use case and benefits
- Provide implementation suggestions if possible
- Consider backwards compatibility

### 🔧 Code Contributions
- Fork the repository
- Create feature branch: `git checkout -b feature/your-feature`
- Follow coding standards (see below)
- Write tests for new functionality
- Update documentation
- Submit pull request

### 📚 Documentation
- Fix typos and improve clarity
- Add code examples
- Create tutorials and guides
- Update API documentation

## 💻 Development Guidelines

### Code Standards

#### Python Style
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter)
- Use descriptive variable and function names

#### Code Organization
```python
# Standard library imports first
import os
import sys
from pathlib import Path

# Third-party imports
import PIL
from PIL import Image

# Local imports
from fileforge.core import ConversionEngine
from fileforge.utils import validate_file
```

#### Error Handling
```python
def convert_image(input_path: str, output_path: str) -> bool:
    """Convert image file with proper error handling."""
    try:
        # Conversion logic here
        return True
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_path}")
        return False
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return False
```

#### Logging
```python
import logging

logger = logging.getLogger(__name__)

def process_file(file_path: str) -> None:
    logger.info(f"Processing file: {file_path}")
    # Processing logic
    logger.debug(f"File processed successfully")
```

### Testing Requirements

#### Test Structure
- Use pytest for all tests
- Place tests in `tests/` directory
- Mirror source structure: `tests/test_converters/test_image_converter.py`
- Use descriptive test names: `test_convert_heic_to_jpg_with_quality_setting`

#### Test Coverage
```python
import pytest
from unittest.mock import Mock, patch
from fileforge.converters.image_converter import ImageConverter

class TestImageConverter:
    def setup_method(self):
        self.converter = ImageConverter()
    
    def test_convert_heic_to_jpg_success(self):
        # Test successful conversion
        result = self.converter.convert("test.heic", "test.jpg")
        assert result is True
    
    def test_convert_invalid_format_fails(self):
        # Test error handling
        with pytest.raises(ValueError):
            self.converter.convert("test.txt", "test.jpg")
```

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fileforge

# Run specific test file
pytest tests/test_converters/test_image_converter.py

# Run specific test
pytest tests/test_converters/test_image_converter.py::TestImageConverter::test_convert_heic_to_jpg_success
```

### Documentation Standards

#### Docstrings
```python
def convert_image(
    input_path: str, 
    output_path: str, 
    quality: int = 90,
    resize: tuple = None
) -> bool:
    """Convert image file to different format.
    
    Args:
        input_path: Path to input image file
        output_path: Path for output image file
        quality: JPEG quality (1-100, default: 90)
        resize: Optional (width, height) tuple for resizing
        
    Returns:
        True if conversion successful, False otherwise
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If invalid format or parameters
        
    Example:
        >>> converter = ImageConverter()
        >>> success = converter.convert("photo.heic", "photo.jpg", quality=85)
    """
```

#### README Updates
- Update feature lists when adding new functionality
- Add usage examples for new features
- Update installation instructions if needed
- Keep performance benchmarks current

## 🏗️ Adding New Converters

### Converter Template
```python
"""Template for new file format converter."""

from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class NewFormatConverter:
    """Converter for new file format."""
    
    def __init__(self):
        self.supported_formats = {
            'input': ['.ext1', '.ext2'],
            'output': ['.ext3', '.ext4']
        }
    
    def can_convert(self, input_format: str, output_format: str) -> bool:
        """Check if conversion is supported."""
        return (
            input_format in self.supported_formats['input'] and
            output_format in self.supported_formats['output']
        )
    
    def convert(
        self, 
        input_path: str, 
        output_path: str, 
        **options
    ) -> bool:
        """Convert file from input to output format."""
        try:
            logger.info(f"Converting {input_path} to {output_path}")
            
            # Conversion logic here
            
            logger.info("Conversion completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return False
    
    def get_info(self, file_path: str) -> Dict[str, Any]:
        """Get file information."""
        # Return file metadata
        pass
```

### Integration Steps
1. Create converter class following template
2. Add to `fileforge/converters/__init__.py`
3. Register in `core.py` ConversionEngine
4. Add CLI support in `cli/main.py`
5. Add GUI support in `gui/main.py`
6. Write comprehensive tests
7. Update documentation

## 🔍 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] Commit messages are clear

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process
1. **Automated Checks**: CI/CD pipeline runs tests and checks
2. **Code Review**: Maintainers review code quality and design
3. **Testing**: Manual testing for complex changes
4. **Merge**: Approved PRs are merged to main branch

## 🐛 Issue Guidelines

### Bug Reports
**Template:**
```markdown
**Describe the bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. With file '...'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g. 3.9.2]
- FileForge version: [e.g. 1.0.0]

**Additional context**
- Error messages
- Log files
- Sample files (if relevant)
```

### Feature Requests
**Template:**
```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution**
Clear description of what you want to happen.

**Describe alternatives**
Alternative solutions you've considered.

**Additional context**
Mockups, examples, or other context.
```

## 🎖️ Recognition

### Contributors
All contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes for significant contributions
- GitHub contributors section

### Types of Recognition
- **Code Contributors**: New features, bug fixes, optimizations
- **Documentation Contributors**: Guides, examples, translations
- **Community Contributors**: Issue triage, user support, feedback
- **Testing Contributors**: Bug reports, testing, quality assurance

## 📞 Getting Help

### Development Questions
- **GitHub Discussions**: Design and architecture questions
- **Issues**: Bug reports and feature requests
- **Discord/Slack**: Real-time development chat (link in README)

### Communication Guidelines
- Be respectful and constructive
- Search existing issues before creating new ones
- Provide sufficient context and details
- Follow up on your contributions

## 📋 Release Process

### Versioning
We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Steps
1. Update version in `fileforge/__init__.py`
2. Update `CHANGELOG.md`
3. Create release branch
4. Final testing and documentation review
5. Merge to main and tag release
6. Automated deployment to PyPI

---

Thank you for contributing to SilentCanoe FileForge! Your contributions help make file conversion better for everyone. 🚀