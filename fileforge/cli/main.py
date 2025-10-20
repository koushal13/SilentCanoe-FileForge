"""
Command Line Interface for SilentCanoe FileForge

Provides comprehensive CLI for all file conversion and processing operations.
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fileforge.core import ConversionEngine, FileType

logger = logging.getLogger(__name__)

class FileForgeConsole:
    """Console interface for SilentCanoe FileForge"""
    
    def __init__(self):
        self.engine = ConversionEngine()
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging for console output"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser"""
        parser = argparse.ArgumentParser(
            description='SilentCanoe FileForge - Universal File Conversion Toolkit',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Convert single image
  fileforge convert image photo.heic photo.jpg --quality 90
  
  # Convert PDF to Word
  fileforge convert document report.pdf report.docx
  
  # Batch convert images
  fileforge batch images *.heic --to jpg --recursive
  
  # PDF operations
  fileforge pdf merge file1.pdf file2.pdf merged.pdf
  fileforge pdf split document.pdf --pages 1-5,10-15
  
  # Media conversions
  fileforge convert audio song.flac song.mp3 --quality high
  fileforge convert video movie.avi movie.mp4 --resolution 720p
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Convert command
        self._add_convert_parser(subparsers)
        
        # Batch command
        self._add_batch_parser(subparsers)
        
        # PDF operations
        self._add_pdf_parser(subparsers)
        
        # Info command
        self._add_info_parser(subparsers)
        
        # List formats command
        self._add_formats_parser(subparsers)
        
        return parser
    
    def _add_convert_parser(self, subparsers):
        """Add convert command parser"""
        convert_parser = subparsers.add_parser('convert', help='Convert single file')
        convert_subparsers = convert_parser.add_subparsers(dest='convert_type')
        
        # Image conversion
        img_parser = convert_subparsers.add_parser('image', help='Convert image files')
        img_parser.add_argument('input', help='Input image file')
        img_parser.add_argument('output', help='Output image file')
        img_parser.add_argument('--quality', type=int, default=90, help='Quality (1-100)')
        img_parser.add_argument('--resize', help='Resize to WIDTHxHEIGHT or preset (720p, 1080p)')
        img_parser.add_argument('--rotate', type=float, help='Rotation angle in degrees')
        img_parser.add_argument('--enhance-contrast', type=float, help='Contrast enhancement (1.0=no change)')
        img_parser.add_argument('--enhance-brightness', type=float, help='Brightness enhancement (1.0=no change)')
        img_parser.add_argument('--blur', type=float, help='Blur radius')
        
        # Document conversion
        doc_parser = convert_subparsers.add_parser('document', help='Convert document files')
        doc_parser.add_argument('input', help='Input document file')
        doc_parser.add_argument('output', help='Output document file')
        doc_parser.add_argument('--password', help='PDF password if encrypted')
        doc_parser.add_argument('--pages', help='Page range (e.g., 1-5,10)')
        doc_parser.add_argument('--ocr', action='store_true', help='Enable OCR for scanned PDFs')
        
        # Audio conversion
        audio_parser = convert_subparsers.add_parser('audio', help='Convert audio files')
        audio_parser.add_argument('input', help='Input audio file')
        audio_parser.add_argument('output', help='Output audio file')
        audio_parser.add_argument('--quality', choices=['low', 'medium', 'high', 'lossless'], 
                                default='medium', help='Audio quality')
        audio_parser.add_argument('--sample-rate', type=int, help='Sample rate (e.g., 44100)')
        audio_parser.add_argument('--channels', type=int, choices=[1, 2], help='Channels (1=mono, 2=stereo)')
        audio_parser.add_argument('--volume', type=float, help='Volume adjustment (e.g., 0.5, 2.0)')
        audio_parser.add_argument('--normalize', action='store_true', help='Normalize audio volume')
        
        # Video conversion
        video_parser = convert_subparsers.add_parser('video', help='Convert video files')
        video_parser.add_argument('input', help='Input video file')
        video_parser.add_argument('output', help='Output video file')
        video_parser.add_argument('--quality', choices=['ultra_low', 'low', 'medium', 'high', 'ultra_high'],
                                default='medium', help='Video quality')
        video_parser.add_argument('--resolution', help='Resolution (480p, 720p, 1080p, 1440p, 4k)')
        video_parser.add_argument('--fps', type=int, help='Frame rate')
        video_parser.add_argument('--start-time', type=float, help='Start time in seconds')
        video_parser.add_argument('--duration', type=float, help='Duration in seconds')
        video_parser.add_argument('--remove-audio', action='store_true', help='Remove audio track')
    
    def _add_batch_parser(self, subparsers):
        """Add batch command parser"""
        batch_parser = subparsers.add_parser('batch', help='Batch convert multiple files')
        batch_parser.add_argument('input_folder', help='Input folder')
        batch_parser.add_argument('--output-folder', help='Output folder (default: input_folder_converted)')
        batch_parser.add_argument('--pattern', default='*', help='File pattern to match')
        batch_parser.add_argument('--to', required=True, help='Output format')
        batch_parser.add_argument('--recursive', action='store_true', help='Search subdirectories')
        batch_parser.add_argument('--quality', type=int, default=90, help='Quality for lossy formats')
        batch_parser.add_argument('--threads', type=int, default=4, help='Number of parallel threads')
    
    def _add_pdf_parser(self, subparsers):
        """Add PDF operations parser"""
        pdf_parser = subparsers.add_parser('pdf', help='PDF operations')
        pdf_subparsers = pdf_parser.add_subparsers(dest='pdf_operation')
        
        # Merge PDFs
        merge_parser = pdf_subparsers.add_parser('merge', help='Merge PDF files')
        merge_parser.add_argument('inputs', nargs='+', help='Input PDF files')
        merge_parser.add_argument('output', help='Output PDF file')
        
        # Split PDF
        split_parser = pdf_subparsers.add_parser('split', help='Split PDF file')
        split_parser.add_argument('input', help='Input PDF file')
        split_parser.add_argument('--output-folder', help='Output folder for split files')
        split_parser.add_argument('--pages', help='Page ranges to extract (e.g., 1-5,10-15)')
        
        # Compress PDF
        compress_parser = pdf_subparsers.add_parser('compress', help='Compress PDF file')
        compress_parser.add_argument('input', help='Input PDF file')
        compress_parser.add_argument('output', help='Output PDF file')
        compress_parser.add_argument('--level', choices=['low', 'medium', 'high'], 
                                   default='medium', help='Compression level')
        
        # Encrypt PDF
        encrypt_parser = pdf_subparsers.add_parser('encrypt', help='Encrypt PDF file')
        encrypt_parser.add_argument('input', help='Input PDF file')
        encrypt_parser.add_argument('output', help='Output PDF file')
        encrypt_parser.add_argument('--password', required=True, help='User password')
        encrypt_parser.add_argument('--owner-password', help='Owner password (for permissions)')
        
        # Add watermark
        watermark_parser = pdf_subparsers.add_parser('watermark', help='Add watermark to PDF')
        watermark_parser.add_argument('input', help='Input PDF file')
        watermark_parser.add_argument('output', help='Output PDF file')
        watermark_parser.add_argument('text', help='Watermark text')
        watermark_parser.add_argument('--font-size', type=int, default=40, help='Font size')
        watermark_parser.add_argument('--opacity', type=float, default=0.3, help='Opacity (0-1)')
    
    def _add_info_parser(self, subparsers):
        """Add info command parser"""
        info_parser = subparsers.add_parser('info', help='Get file information')
        info_parser.add_argument('file', help='File to analyze')
    
    def _add_formats_parser(self, subparsers):
        """Add formats command parser"""
        formats_parser = subparsers.add_parser('formats', help='List supported formats')
        formats_parser.add_argument('--type', choices=['image', 'document', 'audio', 'video'],
                                  help='Show formats for specific type')
    
    def handle_convert(self, args):
        """Handle convert command"""
        input_path = Path(args.input)
        output_path = Path(args.output)
        
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist")
            return False
        
        # Prepare options based on conversion type
        options = {}
        
        if args.convert_type == 'image':
            if args.quality:
                options['quality'] = args.quality
            if args.resize:
                if 'x' in args.resize:
                    w, h = map(int, args.resize.split('x'))
                    options['resize'] = (w, h)
                else:
                    options['resize'] = args.resize
            if args.rotate:
                options['rotate'] = args.rotate
            if args.enhance_contrast:
                options['enhance_contrast'] = args.enhance_contrast
            if args.enhance_brightness:
                options['enhance_brightness'] = args.enhance_brightness
            if args.blur:
                options['blur'] = args.blur
                
        elif args.convert_type == 'document':
            if args.password:
                options['password'] = args.password
            if args.pages:
                options['pages'] = args.pages
            if args.ocr:
                options['ocr'] = True
                
        elif args.convert_type == 'audio':
            options['quality'] = args.quality
            if args.sample_rate:
                options['sample_rate'] = args.sample_rate
            if args.channels:
                options['channels'] = args.channels
            if args.volume:
                options['volume'] = args.volume
            if args.normalize:
                options['normalize'] = True
                
        elif args.convert_type == 'video':
            options['quality'] = args.quality
            if args.resolution:
                options['resolution'] = args.resolution
            if args.fps:
                options['fps'] = args.fps
            if args.start_time:
                options['start_time'] = args.start_time
            if args.duration:
                options['duration'] = args.duration
            if args.remove_audio:
                options['remove_audio'] = True
        
        # Perform conversion
        print(f"Converting {input_path.name} to {output_path.name}...")
        success = self.engine.convert_single(str(input_path), str(output_path), **options)
        
        if success:
            print("✅ Conversion completed successfully!")
            return True
        else:
            print("❌ Conversion failed!")
            return False
    
    def handle_batch(self, args):
        """Handle batch command"""
        input_folder = Path(args.input_folder)
        
        if not input_folder.exists():
            print(f"Error: Input folder '{input_folder}' does not exist")
            return False
        
        output_folder = Path(args.output_folder) if args.output_folder else input_folder.parent / f"{input_folder.name}_converted"
        
        options = {'quality': args.quality}
        
        print(f"Batch converting files from {input_folder} to {output_folder}")
        print(f"Pattern: {args.pattern}, Format: {args.to}, Recursive: {args.recursive}")
        
        results = self.engine.convert_batch(
            str(input_folder),
            str(output_folder),
            args.pattern,
            args.to,
            args.recursive,
            **options
        )
        
        print(f"\n📊 Batch conversion results:")
        print(f"Total files: {results['total']}")
        print(f"Successful: {results['successful']} ✅")
        print(f"Failed: {results['failed']} ❌")
        
        return results['failed'] == 0
    
    def handle_pdf(self, args):
        """Handle PDF operations"""
        from fileforge.converters.document_converter import DocumentConverter
        converter = DocumentConverter()
        
        if args.pdf_operation == 'merge':
            input_paths = [Path(p) for p in args.inputs]
            output_path = Path(args.output)
            
            print(f"Merging {len(input_paths)} PDF files...")
            success = converter.merge_pdfs(input_paths, output_path)
            
        elif args.pdf_operation == 'split':
            input_path = Path(args.input)
            output_folder = Path(args.output_folder) if args.output_folder else input_path.parent / f"{input_path.stem}_split"
            
            print(f"Splitting PDF: {input_path.name}")
            options = {}
            if args.pages:
                options['pages'] = args.pages
            success = converter.split_pdf(input_path, output_folder, **options)
            
        elif args.pdf_operation == 'compress':
            input_path = Path(args.input)
            output_path = Path(args.output)
            
            print(f"Compressing PDF: {input_path.name}")
            success = converter.compress_pdf(input_path, output_path, compress_level=args.level)
            
        elif args.pdf_operation == 'encrypt':
            input_path = Path(args.input)
            output_path = Path(args.output)
            
            print(f"Encrypting PDF: {input_path.name}")
            success = converter.encrypt_pdf(input_path, output_path, args.password, args.owner_password)
            
        elif args.pdf_operation == 'watermark':
            input_path = Path(args.input)
            output_path = Path(args.output)
            
            print(f"Adding watermark to PDF: {input_path.name}")
            options = {
                'font_size': args.font_size,
                'opacity': args.opacity
            }
            success = converter.add_watermark(input_path, output_path, args.text, **options)
        
        else:
            print("Unknown PDF operation")
            return False
        
        if success:
            print("✅ PDF operation completed successfully!")
        else:
            print("❌ PDF operation failed!")
        
        return success
    
    def handle_info(self, args):
        """Handle info command"""
        file_path = Path(args.file)
        
        if not file_path.exists():
            print(f"Error: File '{file_path}' does not exist")
            return False
        
        file_type = self.engine.processor.detect_file_type(file_path)
        
        print(f"📄 File Information: {file_path.name}")
        print(f"Type: {file_type.value}")
        print(f"Size: {file_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Get detailed info based on file type
        if file_type == FileType.IMAGE:
            from fileforge.converters.image_converter import ImageConverter
            converter = ImageConverter()
            info = converter.get_image_info(file_path)
            
            if info:
                print(f"Format: {info.get('format', 'Unknown')}")
                print(f"Dimensions: {info.get('width', 0)}x{info.get('height', 0)}")
                print(f"Mode: {info.get('mode', 'Unknown')}")
                print(f"Has transparency: {info.get('has_transparency', False)}")
                print(f"Animated: {info.get('animated', False)}")
        
        elif file_type == FileType.AUDIO:
            from fileforge.converters.audio_converter import AudioConverter
            converter = AudioConverter()
            info = converter.get_audio_info(file_path)
            
            if info:
                print(f"Format: {info.get('format', 'Unknown')}")
                print(f"Duration: {info.get('duration', 0):.2f} seconds")
                print(f"Bitrate: {info.get('bitrate', 0)} bps")
                print(f"Sample rate: {info.get('sample_rate', 0)} Hz")
                print(f"Channels: {info.get('channels', 0)}")
        
        elif file_type == FileType.VIDEO:
            from fileforge.converters.video_converter import VideoConverter
            converter = VideoConverter()
            info = converter.get_video_info(file_path)
            
            if info:
                print(f"Format: {info.get('format', 'Unknown')}")
                print(f"Duration: {info.get('duration', 0):.2f} seconds")
                print(f"Resolution: {info.get('width', 0)}x{info.get('height', 0)}")
                print(f"Video codec: {info.get('video_codec', 'Unknown')}")
                print(f"Audio codec: {info.get('audio_codec', 'Unknown')}")
                print(f"FPS: {info.get('fps', 0):.2f}")
        
        return True
    
    def handle_formats(self, args):
        """Handle formats command"""
        conversions = self.engine.get_supported_conversions()
        
        if args.type:
            if args.type in conversions:
                print(f"📋 Supported {args.type} formats:")
                for fmt in conversions[args.type]:
                    print(f"  • {fmt}")
            else:
                print(f"No formats available for type: {args.type}")
        else:
            print("📋 All supported formats:")
            for file_type, formats in conversions.items():
                print(f"\n{file_type.upper()}:")
                for fmt in formats:
                    print(f"  • {fmt}")
        
        return True
    
    def run(self, args=None):
        """Run the CLI with given arguments"""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return False
        
        try:
            if parsed_args.command == 'convert':
                return self.handle_convert(parsed_args)
            elif parsed_args.command == 'batch':
                return self.handle_batch(parsed_args)
            elif parsed_args.command == 'pdf':
                return self.handle_pdf(parsed_args)
            elif parsed_args.command == 'info':
                return self.handle_info(parsed_args)
            elif parsed_args.command == 'formats':
                return self.handle_formats(parsed_args)
            else:
                print(f"Unknown command: {parsed_args.command}")
                return False
                
        except KeyboardInterrupt:
            print("\n⚠️ Operation cancelled by user")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"❌ Error: {e}")
            return False

def main():
    """Main entry point for CLI"""
    console = FileForgeConsole()
    success = console.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()