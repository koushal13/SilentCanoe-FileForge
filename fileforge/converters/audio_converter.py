"""
Audio Converter for SilentCanoe FileForge

Supports conversion between major audio formats:
- MP3 (MPEG-1 Audio Layer III)
- WAV (Waveform Audio File Format) 
- FLAC (Free Lossless Audio Codec)
- AAC (Advanced Audio Coding)
- OGG (Ogg Vorbis)
- WMA (Windows Media Audio)
- M4A (MPEG-4 Audio)
- OPUS (Opus Interactive Audio Codec)
- AIFF (Audio Interchange File Format)

Features:
- Quality/bitrate control
- Sample rate conversion
- Channel manipulation (mono/stereo)
- Volume normalization
- Metadata preservation
- Batch conversion
"""

import os
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class AudioConverter:
    """Audio format converter using FFmpeg"""
    
    SUPPORTED_INPUT = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
        '.opus', '.aiff', '.au', '.ra', '.amr', '.3gp'
    }
    
    SUPPORTED_OUTPUT = {
        'mp3': {'codec': 'libmp3lame', 'ext': 'mp3'},
        'wav': {'codec': 'pcm_s16le', 'ext': 'wav'},
        'flac': {'codec': 'flac', 'ext': 'flac'},
        'aac': {'codec': 'aac', 'ext': 'aac'},
        'ogg': {'codec': 'libvorbis', 'ext': 'ogg'},
        'm4a': {'codec': 'aac', 'ext': 'm4a'},
        'opus': {'codec': 'libopus', 'ext': 'opus'},
        'aiff': {'codec': 'pcm_s16be', 'ext': 'aiff'}
    }
    
    # Quality presets
    QUALITY_PRESETS = {
        'low': {'mp3': '128k', 'aac': '96k', 'ogg': '128k'},
        'medium': {'mp3': '192k', 'aac': '128k', 'ogg': '192k'},
        'high': {'mp3': '320k', 'aac': '256k', 'ogg': '320k'},
        'lossless': {'flac': '0', 'wav': None}
    }
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
        if not self.ffmpeg_available:
            logger.warning("FFmpeg not found. Audio conversion will be limited.")
    
    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats"""
        return list(self.SUPPORTED_OUTPUT.keys())
    
    def get_audio_info(self, audio_path: Path) -> Dict[str, Any]:
        """Get detailed information about an audio file"""
        if not self.ffmpeg_available:
            return {}
        
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(audio_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                audio_stream = None
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'audio':
                        audio_stream = stream
                        break
                
                if audio_stream:
                    return {
                        'format': data['format'].get('format_name', 'unknown'),
                        'duration': float(data['format'].get('duration', 0)),
                        'bitrate': int(data['format'].get('bit_rate', 0)),
                        'sample_rate': int(audio_stream.get('sample_rate', 0)),
                        'channels': int(audio_stream.get('channels', 0)),
                        'codec': audio_stream.get('codec_name', 'unknown'),
                        'size': int(data['format'].get('size', 0))
                    }
            
            return {}
            
        except Exception as e:
            logger.error(f"Failed to get audio info for {audio_path}: {e}")
            return {}
    
    def convert(self, input_path: Path, output_path: Path, **options) -> bool:
        """
        Convert audio file to another format
        
        Args:
            input_path: Source audio file
            output_path: Destination audio file
            **options: Conversion options
        
        Options:
            quality: 'low', 'medium', 'high', 'lossless' or custom bitrate
            sample_rate: Target sample rate (e.g., 44100, 48000)
            channels: Number of channels (1=mono, 2=stereo)
            volume: Volume adjustment (e.g., 0.5, 2.0)
            start_time: Start time in seconds
            duration: Duration to convert in seconds
            fade_in: Fade in duration in seconds
            fade_out: Fade out duration in seconds
            normalize: Normalize audio volume
            preserve_metadata: Keep original metadata
        """
        
        if not self.ffmpeg_available:
            logger.error("FFmpeg required for audio conversion")
            return False
        
        try:
            output_format = output_path.suffix.lower().lstrip('.')
            
            if output_format not in self.SUPPORTED_OUTPUT:
                logger.error(f"Unsupported output format: {output_format}")
                return False
            
            # Build FFmpeg command
            cmd = ['ffmpeg', '-i', str(input_path)]
            
            # Input options
            if 'start_time' in options:
                cmd.extend(['-ss', str(options['start_time'])])
            
            if 'duration' in options:
                cmd.extend(['-t', str(options['duration'])])
            
            # Audio codec
            codec_info = self.SUPPORTED_OUTPUT[output_format]
            cmd.extend(['-c:a', codec_info['codec']])
            
            # Quality/bitrate
            quality = options.get('quality', 'medium')
            if quality in self.QUALITY_PRESETS:
                preset = self.QUALITY_PRESETS[quality]
                if output_format in preset and preset[output_format]:
                    cmd.extend(['-b:a', preset[output_format]])
            else:
                # Custom bitrate
                cmd.extend(['-b:a', str(quality)])
            
            # Sample rate
            if 'sample_rate' in options:
                cmd.extend(['-ar', str(options['sample_rate'])])
            
            # Channels
            if 'channels' in options:
                cmd.extend(['-ac', str(options['channels'])])
            
            # Audio filters
            filters = []
            
            # Volume adjustment
            if 'volume' in options:
                filters.append(f"volume={options['volume']}")
            
            # Fade effects
            if 'fade_in' in options:
                filters.append(f"afade=in:st=0:d={options['fade_in']}")
            
            if 'fade_out' in options:
                duration = options.get('duration')
                if duration:
                    fade_start = duration - options['fade_out']
                    filters.append(f"afade=out:st={fade_start}:d={options['fade_out']}")
            
            # Normalization
            if options.get('normalize', False):
                filters.append("loudnorm")
            
            # Apply filters
            if filters:
                cmd.extend(['-af', ','.join(filters)])
            
            # Metadata handling
            if not options.get('preserve_metadata', True):
                cmd.extend(['-map_metadata', '-1'])
            
            # Output options
            cmd.extend(['-y', str(output_path)])  # Overwrite output file
            
            # Execute conversion
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info(f"Converted {input_path.name} to {output_path.name}")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Audio conversion failed: {e}")
            return False
    
    def batch_convert(self, input_folder: Path, output_folder: Path,
                     output_format: str, recursive: bool = True, **options) -> List[Dict[str, Any]]:
        """Convert multiple audio files"""
        results = []
        
        pattern = "**/*" if recursive else "*"
        for input_file in input_folder.glob(pattern):
            if input_file.is_file() and input_file.suffix.lower() in self.SUPPORTED_INPUT:
                
                relative_path = input_file.relative_to(input_folder)
                output_file = output_folder / relative_path.with_suffix(f'.{output_format}')
                
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                success = self.convert(input_file, output_file, **options)
                
                results.append({
                    'input': str(input_file),
                    'output': str(output_file),
                    'success': success
                })
        
        return results
    
    def extract_audio_from_video(self, video_path: Path, audio_path: Path, **options) -> bool:
        """Extract audio track from video file"""
        if not self.ffmpeg_available:
            return False
        
        try:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'copy',  # Copy audio without re-encoding
                '-y', str(audio_path)
            ]
            
            # Apply audio-specific options if needed
            if 'quality' in options or 'sample_rate' in options:
                # Re-encode with specific options
                cmd = ['ffmpeg', '-i', str(video_path), '-vn']
                
                output_format = audio_path.suffix.lower().lstrip('.')
                if output_format in self.SUPPORTED_OUTPUT:
                    codec_info = self.SUPPORTED_OUTPUT[output_format]
                    cmd.extend(['-c:a', codec_info['codec']])
                
                # Add quality options as in convert method
                if 'quality' in options:
                    quality = options['quality']
                    if quality in self.QUALITY_PRESETS:
                        preset = self.QUALITY_PRESETS[quality]
                        if output_format in preset and preset[output_format]:
                            cmd.extend(['-b:a', preset[output_format]])
                
                cmd.extend(['-y', str(audio_path)])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Audio extraction failed: {e}")
            return False
    
    def merge_audio_files(self, input_paths: List[Path], output_path: Path, **options) -> bool:
        """Merge multiple audio files into one"""
        if not self.ffmpeg_available or len(input_paths) < 2:
            return False
        
        try:
            # Create input list for FFmpeg
            cmd = ['ffmpeg']
            
            # Add input files
            for input_path in input_paths:
                cmd.extend(['-i', str(input_path)])
            
            # Filter complex for concatenation
            filter_inputs = ''.join(f'[{i}:a]' for i in range(len(input_paths)))
            cmd.extend([
                '-filter_complex',
                f'{filter_inputs}concat=n={len(input_paths)}:v=0:a=1[out]',
                '-map', '[out]',
                '-y', str(output_path)
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Audio merge failed: {e}")
            return False
    
    def split_audio(self, input_path: Path, output_folder: Path, segment_duration: int = 300) -> bool:
        """Split audio file into segments"""
        if not self.ffmpeg_available:
            return False
        
        try:
            output_pattern = output_folder / f"{input_path.stem}_part_%03d{input_path.suffix}"
            
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-f', 'segment',
                '-segment_time', str(segment_duration),
                '-c', 'copy',
                '-y', str(output_pattern)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Audio split failed: {e}")
            return False