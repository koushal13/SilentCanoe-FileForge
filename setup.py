"""Setup configuration for SilentCanoe FileForge."""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="silentcanoe-fileforge",
    version="1.0.0",
    author="SilentCanoe",
    author_email="contact@silentcanoe.com",
    description="Universal File Conversion and Manipulation Toolkit",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/silentcanoe/fileforge",
    project_urls={
        "Bug Tracker": "https://github.com/silentcanoe/fileforge/issues",
        "Documentation": "https://github.com/silentcanoe/fileforge/docs",
        "Source Code": "https://github.com/silentcanoe/fileforge",
        "Website": "https://silentcanoe.com",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Office/Business",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "all": [
            "opencv-python>=4.5.0",
            "scikit-image>=0.19.0",
            "wand>=0.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fileforge=fileforge.cli.main:main",
            "silentcanoe-fileforge=fileforge.cli.main:main",
        ],
        "gui_scripts": [
            "fileforge-gui=fileforge.gui.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "fileforge": [
            "data/*",
            "templates/*",
            "configs/*",
        ],
    },
    keywords=[
        "file conversion",
        "image processing",
        "pdf manipulation", 
        "audio conversion",
        "video conversion",
        "batch processing",
        "heic",
        "jpg",
        "png",
        "mp3",
        "mp4",
        "document converter",
        "silentcanoe",
        "multimedia",
        "utility",
    ],
    zip_safe=False,
)