#!/usr/bin/env python3
"""
SilentCanoe FileForge - Main Entry Point

Universal file conversion and manipulation toolkit.
Run with --help to see all available commands.

Usage:
    fileforge <command> [options]
    fileforge gui
    fileforge convert --help
    fileforge pdf --help
    fileforge batch --help

Examples:
    fileforge convert image input.heic output.jpg
    fileforge convert pdf document.pdf document.docx
    fileforge pdf merge file1.pdf file2.pdf merged.pdf
    fileforge batch convert *.heic --to jpg --quality 90
    fileforge gui
"""

import sys
import argparse
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fileforge.cli.main import main as cli_main
from fileforge.gui.main import main as gui_main

def main():
    """Main entry point for SilentCanoe FileForge"""
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(0)
    
    # If first argument is 'gui', launch GUI
    if len(sys.argv) >= 2 and sys.argv[1] == 'gui':
        gui_main()
        return
    
    # Otherwise, use CLI
    cli_main()

if __name__ == "__main__":
    main()