#!/usr/bin/env python3
"""
SilentCanoe FileForge CLI - Demo Version
Command-line interface for file analysis and information
"""

import os
import sys
import argparse
from pathlib import Path
import time
import json

class FileForgeCliDemo:
    """CLI Demo version of SilentCanoe FileForge."""
    
    def __init__(self):
        self.supported_formats = {
            'image': ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'heic', 'webp'],
            'document': ['pdf', 'docx', 'txt', 'md', 'rtf', 'csv', 'html'],
            'audio': ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'],
            'video': ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm'],
            'archive': ['zip', 'rar', '7z', 'tar', 'gz', 'bz2'],
            'code': ['py', 'js', 'html', 'css', 'cpp', 'java', 'c', 'h', 'php']
        }
        
    def analyze_file(self, file_path: str, output_format: str = 'text') -> dict:
        """Analyze a file and return information."""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {'error': f"File not found: {file_path}"}
                
            if not path.is_file():
                return {'error': f"Path is not a file: {file_path}"}
                
            stat = path.stat()
            ext = path.suffix.lower().lstrip('.')
            file_type = self.detect_file_type(ext)
            
            # Build file information
            file_info = {
                'name': path.name,
                'path': str(path.absolute()),
                'extension': ext,
                'type': file_type,
                'size_bytes': stat.st_size,
                'size_formatted': self.format_file_size(stat.st_size),
                'created': time.ctime(stat.st_ctime),
                'modified': time.ctime(stat.st_mtime),
                'accessed': time.ctime(stat.st_atime),
                'permissions': {
                    'readable': os.access(path, os.R_OK),
                    'writable': os.access(path, os.W_OK),
                    'executable': os.access(path, os.X_OK)
                },
                'supported': self.is_supported_format(ext),
                'conversion_options': self.get_conversion_options(file_type)
            }
            
            return file_info
            
        except Exception as e:
            return {'error': f"Failed to analyze file: {str(e)}"}
            
    def list_directory(self, dir_path: str, recursive: bool = False) -> dict:
        """List directory contents with file information."""
        try:
            path = Path(dir_path)
            
            if not path.exists():
                return {'error': f"Directory not found: {dir_path}"}
                
            if not path.is_dir():
                return {'error': f"Path is not a directory: {dir_path}"}
                
            files = []
            directories = []
            
            # Get items
            if recursive:
                items = path.rglob('*')
            else:
                items = path.iterdir()
                
            for item in sorted(items, key=lambda x: x.name.lower()):
                try:
                    stat = item.stat()
                    
                    item_info = {
                        'name': item.name,
                        'path': str(item.absolute()),
                        'size_bytes': stat.st_size if item.is_file() else 0,
                        'size_formatted': self.format_file_size(stat.st_size) if item.is_file() else '-',
                        'modified': time.ctime(stat.st_mtime),
                        'type': self.detect_file_type(item.suffix.lower().lstrip('.')) if item.is_file() else 'directory'
                    }
                    
                    if item.is_file():
                        files.append(item_info)
                    else:
                        directories.append(item_info)
                        
                except (PermissionError, OSError):
                    # Skip files we can't access
                    continue
                    
            return {
                'directory': str(path.absolute()),
                'directories': directories,
                'files': files,
                'total_directories': len(directories),
                'total_files': len(files)
            }
            
        except Exception as e:
            return {'error': f"Failed to list directory: {str(e)}"}
            
    def detect_file_type(self, extension: str) -> str:
        """Detect file type from extension."""
        for file_type, extensions in self.supported_formats.items():
            if extension in extensions:
                return file_type
        return 'unknown'
        
    def is_supported_format(self, extension: str) -> bool:
        """Check if format is supported."""
        for extensions in self.supported_formats.values():
            if extension in extensions:
                return True
        return False
        
    def get_conversion_options(self, file_type: str) -> list:
        """Get available conversion options for file type."""
        options = {
            'image': ['JPG', 'PNG', 'WebP', 'BMP', 'TIFF', 'GIF'],
            'document': ['PDF', 'DOCX', 'TXT', 'HTML', 'MD'],
            'audio': ['MP3', 'WAV', 'FLAC', 'AAC', 'OGG'],
            'video': ['MP4', 'AVI', 'MKV', 'WebM', 'MOV'],
            'archive': ['ZIP', 'TAR.GZ', '7Z'],
            'code': ['Format code', 'Minify', 'Beautify']
        }
        return options.get(file_type, ['No conversions available in demo'])
        
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
            
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
        
    def print_file_info(self, file_info: dict):
        """Print formatted file information."""
        if 'error' in file_info:
            print(f"❌ Error: {file_info['error']}")
            return
            
        print("🔧 SilentCanoe FileForge - File Analysis")
        print("=" * 50)
        print(f"📄 Name: {file_info['name']}")
        print(f"📁 Path: {file_info['path']}")
        print(f"🏷️  Type: {file_info['type'].title()}")
        print(f"📊 Size: {file_info['size_formatted']} ({file_info['size_bytes']:,} bytes)")
        print(f"📅 Created: {file_info['created']}")
        print(f"📅 Modified: {file_info['modified']}")
        print(f"🔧 Extension: .{file_info['extension']}" if file_info['extension'] else "🔧 Extension: None")
        print(f"✅ Supported: {'Yes' if file_info['supported'] else 'No'}")
        
        print("\n🔑 Permissions:")
        perms = file_info['permissions']
        print(f"  📖 Readable: {'Yes' if perms['readable'] else 'No'}")
        print(f"  ✏️  Writable: {'Yes' if perms['writable'] else 'No'}")
        print(f"  🚀 Executable: {'Yes' if perms['executable'] else 'No'}")
        
        print("\n🛠️  Conversion Options:")
        for option in file_info['conversion_options']:
            print(f"  • {option}")
            
        print("\n💡 Demo Version - Actual conversion requires full implementation")
        print("🌐 GitHub: https://github.com/koushal13/SilentCanoe-FileForge")
        
    def print_directory_listing(self, dir_info: dict, show_files: bool = True, show_dirs: bool = True):
        """Print formatted directory listing."""
        if 'error' in dir_info:
            print(f"❌ Error: {dir_info['error']}")
            return
            
        print("🔧 SilentCanoe FileForge - Directory Browser")
        print("=" * 50)
        print(f"📁 Directory: {dir_info['directory']}")
        print(f"📊 Summary: {dir_info['total_directories']} directories, {dir_info['total_files']} files")
        
        if show_dirs and dir_info['directories']:
            print(f"\n📂 Directories ({dir_info['total_directories']}):")
            print("-" * 30)
            for directory in dir_info['directories'][:20]:  # Limit to first 20
                print(f"📁 {directory['name']}")
            
            if len(dir_info['directories']) > 20:
                print(f"... and {len(dir_info['directories']) - 20} more directories")
                
        if show_files and dir_info['files']:
            print(f"\n📄 Files ({dir_info['total_files']}):")
            print("-" * 60)
            print(f"{'Name':<30} {'Type':<12} {'Size':<10} {'Modified':<20}")
            print("-" * 60)
            
            for file_item in dir_info['files'][:20]:  # Limit to first 20
                name = file_item['name'][:28] + "..." if len(file_item['name']) > 30 else file_item['name']
                file_type = file_item['type'][:10]
                size = file_item['size_formatted']
                modified = file_item['modified'].split()[1:3]  # Get date and time only
                modified_str = " ".join(modified)[:18]
                
                print(f"{name:<30} {file_type:<12} {size:<10} {modified_str:<20}")
                
            if len(dir_info['files']) > 20:
                print(f"... and {len(dir_info['files']) - 20} more files")
                
        print("\n💡 Use 'analyze <filename>' to get detailed file information")
        print("🌐 GitHub: https://github.com/koushal13/SilentCanoe-FileForge")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="🔧 SilentCanoe FileForge - Universal File Toolkit (Demo)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fileforge_cli.py analyze photo.jpg
  python fileforge_cli.py analyze document.pdf --json
  python fileforge_cli.py list /path/to/directory
  python fileforge_cli.py list . --recursive
  python fileforge_cli.py info
  
🌐 GitHub: https://github.com/koushal13/SilentCanoe-FileForge
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a file')
    analyze_parser.add_argument('file', help='Path to file to analyze')
    analyze_parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List directory contents')
    list_parser.add_argument('directory', nargs='?', default='.', help='Directory to list (default: current)')
    list_parser.add_argument('--recursive', '-r', action='store_true', help='List recursively')
    list_parser.add_argument('--files-only', action='store_true', help='Show only files')
    list_parser.add_argument('--dirs-only', action='store_true', help='Show only directories')
    list_parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show application information')
    
    # GUI command
    gui_parser = subparsers.add_parser('gui', help='Launch GUI version')
    
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return
        
    cli = FileForgeCliDemo()
    
    if args.command == 'analyze':
        file_info = cli.analyze_file(args.file)
        if args.json:
            print(json.dumps(file_info, indent=2))
        else:
            cli.print_file_info(file_info)
            
    elif args.command == 'list':
        dir_info = cli.list_directory(args.directory, args.recursive)
        if args.json:
            print(json.dumps(dir_info, indent=2))
        else:
            show_files = not args.dirs_only
            show_dirs = not args.files_only
            cli.print_directory_listing(dir_info, show_files, show_dirs)
            
    elif args.command == 'info':
        print("🔧 SilentCanoe FileForge - Demo Version")
        print("=" * 50)
        print("Universal File Conversion and Manipulation Toolkit")
        print()
        print("🌟 Demo Features:")
        print("  • File information analysis")
        print("  • Directory browsing and listing")
        print("  • Format detection and categorization")
        print("  • Command-line interface")
        print("  • JSON output support")
        print()
        print("🚀 Full Version Features:")
        print("  • Universal image converter (HEIC, JPG, PNG, WebP, etc.)")
        print("  • PDF manipulation suite (merge, split, compress, encrypt)")
        print("  • Audio/Video conversion with FFmpeg integration")
        print("  • Batch processing with parallel execution")
        print("  • GUI interface with drag-and-drop")
        print("  • Professional API documentation")
        print()
        print("📊 Supported Formats (Detection Only):")
        for category, formats in cli.supported_formats.items():
            print(f"  {category.title()}: {', '.join(formats[:10])}")
            if len(formats) > 10:
                print(f"    ... and {len(formats) - 10} more")
        print()
        print("💻 Technical Details:")
        import sys as system_info
        print(f"  • Python {system_info.version.split()[0]}")
        print(f"  • Platform: {system_info.platform}")
        print("  • License: MIT")
        print("  • Version: 1.0.0 Demo")
        print()
        print("🌐 Links:")
        print("  • GitHub: https://github.com/koushal13/SilentCanoe-FileForge")
        print("  • SilentCanoe: https://silentcanoe.com")
        print("  • Documentation: See repository README")
        
    elif args.command == 'gui':
        print("🚀 Launching GUI version...")
        try:
            # Try to launch the GUI demo
            import subprocess
            import sys
            
            demo_path = Path(__file__).parent / 'demo.py'
            if demo_path.exists():
                subprocess.run([sys.executable, str(demo_path)])
            else:
                print("❌ GUI demo not found. Please run:")
                print("   python demo.py")
        except Exception as e:
            print(f"❌ Failed to launch GUI: {e}")
            print("💡 Try running: python demo.py")

if __name__ == "__main__":
    main()