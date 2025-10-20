"""
Core processing engine for SilentCanoe FileForge

Handles file detection, conversion routing, and batch processing.
"""

import os
import logging
import threading
import queue
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileType(Enum):
    """Supported file types"""
    IMAGE = "image"
    DOCUMENT = "document" 
    AUDIO = "audio"
    VIDEO = "video"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"

@dataclass
class ConversionJob:
    """Represents a single file conversion job"""
    input_path: Path
    output_path: Path
    converter_type: str
    options: Dict[str, Any]
    priority: int = 0
    
class ConversionResult:
    """Result of a conversion operation"""
    def __init__(self, success: bool, input_path: Path, output_path: Path, 
                 message: str = "", error: Optional[Exception] = None):
        self.success = success
        self.input_path = input_path
        self.output_path = output_path
        self.message = message
        self.error = error
        self.timestamp = None

class FileProcessor:
    """Core file processing engine"""
    
    # File type mappings
    IMAGE_EXTENSIONS = {
        '.heic', '.heif', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif',
        '.webp', '.gif', '.ico', '.psd', '.raw', '.cr2', '.nef', '.arw',
        '.dng', '.orf', '.rw2', '.pef', '.srw', '.svg'
    }
    
    DOCUMENT_EXTENSIONS = {
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.txt', '.rtf', '.odt', '.ods', '.odp', '.csv', '.json',
        '.xml', '.yaml', '.yml', '.md', '.html', '.htm'
    }
    
    AUDIO_EXTENSIONS = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
        '.opus', '.amr', '.aiff', '.au', '.ra'
    }
    
    VIDEO_EXTENSIONS = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
        '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts'
    }
    
    ARCHIVE_EXTENSIONS = {
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
        '.tar.gz', '.tar.bz2', '.tar.xz'
    }
    
    def __init__(self):
        self.converters = {}
        self._register_converters()
    
    def _register_converters(self):
        """Register all available converters"""
        try:
            from .converters.image_converter import ImageConverter
            self.converters['image'] = ImageConverter()
        except ImportError:
            logger.warning("Image converter not available")
        
        try:
            from .converters.document_converter import DocumentConverter
            self.converters['document'] = DocumentConverter()
        except ImportError:
            logger.warning("Document converter not available")
        
        try:
            from .converters.audio_converter import AudioConverter
            self.converters['audio'] = AudioConverter()
        except ImportError:
            logger.warning("Audio converter not available")
        
        try:
            from .converters.video_converter import VideoConverter
            self.converters['video'] = VideoConverter()
        except ImportError:
            logger.warning("Video converter not available")
    
    def detect_file_type(self, file_path: Path) -> FileType:
        """Detect the type of a file based on its extension"""
        ext = file_path.suffix.lower()
        
        if ext in self.IMAGE_EXTENSIONS:
            return FileType.IMAGE
        elif ext in self.DOCUMENT_EXTENSIONS:
            return FileType.DOCUMENT
        elif ext in self.AUDIO_EXTENSIONS:
            return FileType.AUDIO
        elif ext in self.VIDEO_EXTENSIONS:
            return FileType.VIDEO
        elif ext in self.ARCHIVE_EXTENSIONS:
            return FileType.ARCHIVE
        else:
            return FileType.UNKNOWN
    
    def get_supported_formats(self, file_type: FileType) -> List[str]:
        """Get list of supported output formats for a file type"""
        converter_name = file_type.value
        if converter_name in self.converters:
            return self.converters[converter_name].get_supported_formats()
        return []
    
    def convert_file(self, input_path: Path, output_path: Path, 
                    options: Dict[str, Any] = None) -> ConversionResult:
        """Convert a single file"""
        options = options or {}
        
        if not input_path.exists():
            return ConversionResult(
                False, input_path, output_path,
                f"Input file does not exist: {input_path}"
            )
        
        file_type = self.detect_file_type(input_path)
        
        if file_type == FileType.UNKNOWN:
            return ConversionResult(
                False, input_path, output_path,
                f"Unsupported file type: {input_path.suffix}"
            )
        
        converter_name = file_type.value
        if converter_name not in self.converters:
            return ConversionResult(
                False, input_path, output_path,
                f"No converter available for {file_type.value} files"
            )
        
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Perform conversion
            converter = self.converters[converter_name]
            success = converter.convert(input_path, output_path, **options)
            
            if success:
                return ConversionResult(
                    True, input_path, output_path,
                    f"Successfully converted {input_path.name} to {output_path.name}"
                )
            else:
                return ConversionResult(
                    False, input_path, output_path,
                    "Conversion failed"
                )
                
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            return ConversionResult(
                False, input_path, output_path,
                f"Conversion error: {str(e)}", e
            )

class BatchProcessor:
    """Handles batch file processing with parallel execution"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.file_processor = FileProcessor()
        self.job_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.progress_callback: Optional[Callable] = None
        self.cancel_event = threading.Event()
    
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """Set callback for progress updates: callback(completed, total, current_file)"""
        self.progress_callback = callback
    
    def add_files(self, input_folder: Path, output_folder: Path, 
                  recursive: bool = True, file_pattern: str = "*",
                  output_format: str = None, options: Dict[str, Any] = None):
        """Add files to the conversion queue"""
        options = options or {}
        
        if recursive:
            pattern_files = input_folder.rglob(file_pattern)
        else:
            pattern_files = input_folder.glob(file_pattern)
        
        for input_file in pattern_files:
            if input_file.is_file():
                # Generate output path
                relative_path = input_file.relative_to(input_folder)
                
                if output_format:
                    output_file = output_folder / relative_path.with_suffix(f'.{output_format}')
                else:
                    output_file = output_folder / relative_path
                
                job = ConversionJob(
                    input_path=input_file,
                    output_path=output_file,
                    converter_type=self.file_processor.detect_file_type(input_file).value,
                    options=options
                )
                self.job_queue.put(job)
    
    def process_all(self) -> List[ConversionResult]:
        """Process all jobs in the queue"""
        jobs = []
        while not self.job_queue.empty():
            jobs.append(self.job_queue.get())
        
        if not jobs:
            return []
        
        results = []
        completed = 0
        total = len(jobs)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self._process_job, job): job 
                for job in jobs
            }
            
            # Process completed jobs
            for future in as_completed(future_to_job):
                if self.cancel_event.is_set():
                    break
                
                job = future_to_job[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1
                    
                    if self.progress_callback:
                        self.progress_callback(completed, total, str(job.input_path.name))
                        
                except Exception as e:
                    logger.error(f"Job failed: {e}")
                    results.append(ConversionResult(
                        False, job.input_path, job.output_path,
                        f"Processing error: {str(e)}", e
                    ))
        
        return results
    
    def _process_job(self, job: ConversionJob) -> ConversionResult:
        """Process a single conversion job"""
        return self.file_processor.convert_file(
            job.input_path, job.output_path, job.options
        )
    
    def cancel(self):
        """Cancel the current batch operation"""
        self.cancel_event.set()

class ConversionEngine:
    """High-level interface for file conversions"""
    
    def __init__(self):
        self.processor = FileProcessor()
        self.batch_processor = BatchProcessor()
    
    def convert_single(self, input_path: str, output_path: str, **options) -> bool:
        """Convert a single file"""
        result = self.processor.convert_file(
            Path(input_path), Path(output_path), options
        )
        return result.success
    
    def convert_batch(self, input_folder: str, output_folder: str, 
                     file_pattern: str = "*", output_format: str = None,
                     recursive: bool = True, **options) -> Dict[str, Any]:
        """Convert multiple files"""
        
        self.batch_processor.add_files(
            Path(input_folder), Path(output_folder),
            recursive, file_pattern, output_format, options
        )
        
        results = self.batch_processor.process_all()
        
        # Summarize results
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        return {
            'total': len(results),
            'successful': successful,
            'failed': failed,
            'results': results
        }
    
    def get_supported_conversions(self) -> Dict[str, List[str]]:
        """Get all supported conversion types"""
        conversions = {}
        for file_type in FileType:
            if file_type != FileType.UNKNOWN:
                formats = self.processor.get_supported_formats(file_type)
                if formats:
                    conversions[file_type.value] = formats
        return conversions