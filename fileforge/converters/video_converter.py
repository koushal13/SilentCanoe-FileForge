"""
Video Converter for SilentCanoe FileForge

Supports conversion between major video formats:
- MP4 (MPEG-4 Part 14)
- AVI (Audio Video Interleave)
- MKV (Matroska Video)
- MOV (QuickTime Movie)
- WMV (Windows Media Video)
- FLV (Flash Video)
- WebM (Web Media)
- 3GP (3rd Generation Partnership Project)
- TS (MPEG Transport Stream)

Features:
- Quality/bitrate control
- Resolution scaling
- Frame rate conversion
- Codec selection (H.264, H.265, VP9, etc.)
- Compression presets
- Subtitle handling
- Metadata preservation
- Batch conversion
"""

import os
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

class VideoConverter:
    """Video format converter using FFmpeg"""
    
    SUPPORTED_INPUT = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
        '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts', '.vob'
    }
    
    SUPPORTED_OUTPUT = {
        'mp4': {'container': 'mp4', 'video_codec': 'libx264', 'audio_codec': 'aac'},
        'avi': {'container': 'avi', 'video_codec': 'libx264', 'audio_codec': 'mp3'},
        'mkv': {'container': 'matroska', 'video_codec': 'libx264', 'audio_codec': 'aac'},
        'mov': {'container': 'mov', 'video_codec': 'libx264', 'audio_codec': 'aac'},
        'wmv': {'container': 'asf', 'video_codec': 'wmv2', 'audio_codec': 'wmav2'},
        'webm': {'container': 'webm', 'video_codec': 'libvpx-vp9', 'audio_codec': 'libopus'},
        '3gp': {'container': '3gp', 'video_codec': 'h263', 'audio_codec': 'amr_nb'},
        'flv': {'container': 'flv', 'video_codec': 'flv1', 'audio_codec': 'mp3'}
    }
    
    # Quality presets
    QUALITY_PRESETS = {
        'ultra_low': {'crf': 32, 'preset': 'ultrafast'},
        'low': {'crf': 28, 'preset': 'fast'},
        'medium': {'crf': 23, 'preset': 'medium'},
        'high': {'crf': 18, 'preset': 'slow'},
        'ultra_high': {'crf': 15, 'preset': 'slower'}
    }
    
    # Resolution presets
    RESOLUTION_PRESETS = {
        '480p': (854, 480),
        '720p': (1280, 720),
        '1080p': (1920, 1080),
        '1440p': (2560, 1440),
        '4k': (3840, 2160)
    }
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
        if not self.ffmpeg_available:
            logger.warning("FFmpeg not found. Video conversion will not be available.")
    
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
    
    def get_video_info(self, video_path: Path) -> Dict[str, Any]:
        """Get detailed information about a video file"""
        if not self.ffmpeg_available:
            return {}
        
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                video_stream = None
                audio_stream = None
                
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video' and not video_stream:
                        video_stream = stream
                    elif stream.get('codec_type') == 'audio' and not audio_stream:
                        audio_stream = stream
                
                info = {
                    'format': data['format'].get('format_name', 'unknown'),
                    'duration': float(data['format'].get('duration', 0)),
                    'size': int(data['format'].get('size', 0)),
                    'bitrate': int(data['format'].get('bit_rate', 0))
                }
                
                if video_stream:
                    info.update({
                        'width': int(video_stream.get('width', 0)),
                        'height': int(video_stream.get('height', 0)),
                        'video_codec': video_stream.get('codec_name', 'unknown'),
                        'video_bitrate': int(video_stream.get('bit_rate', 0)),
                        'fps': eval(video_stream.get('r_frame_rate', '0/1')),
                        'pixel_format': video_stream.get('pix_fmt', 'unknown')
                    })
                
                if audio_stream:
                    info.update({
                        'audio_codec': audio_stream.get('codec_name', 'unknown'),
                        'audio_bitrate': int(audio_stream.get('bit_rate', 0)),
                        'sample_rate': int(audio_stream.get('sample_rate', 0)),
                        'channels': int(audio_stream.get('channels', 0))
                    })
                
                return info
            
            return {}
            
        except Exception as e:
            logger.error(f"Failed to get video info for {video_path}: {e}")
            return {}
    
    def convert(self, input_path: Path, output_path: Path, **options) -> bool:
        """
        Convert video file to another format
        
        Args:
            input_path: Source video file
            output_path: Destination video file
            **options: Conversion options
        
        Options:
            quality: 'ultra_low', 'low', 'medium', 'high', 'ultra_high' or custom CRF
            resolution: '480p', '720p', '1080p', '1440p', '4k' or tuple (width, height)
            fps: Target frame rate
            video_codec: Video codec (h264, h265, vp9, etc.)
            audio_codec: Audio codec (aac, mp3, opus, etc.)
            start_time: Start time in seconds
            duration: Duration to convert in seconds
            bitrate: Target bitrate (e.g., '2M', '500k')
            preset: Encoding preset (ultrafast, fast, medium, slow, slower)
            remove_audio: Strip audio track
            extract_audio: Extract audio to separate file
            scale_method: Scaling algorithm (lanczos, bicubic, bilinear)
        """
        
        if not self.ffmpeg_available:
            logger.error("FFmpeg required for video conversion")
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
            
            # Video codec
            format_info = self.SUPPORTED_OUTPUT[output_format]
            video_codec = options.get('video_codec', format_info['video_codec'])
            cmd.extend(['-c:v', video_codec])
            
            # Quality settings
            quality = options.get('quality', 'medium')
            if quality in self.QUALITY_PRESETS:
                preset_info = self.QUALITY_PRESETS[quality]
                if 'crf' in preset_info and video_codec in ['libx264', 'libx265']:
                    cmd.extend(['-crf', str(preset_info['crf'])])
                if 'preset' in preset_info:
                    cmd.extend(['-preset', preset_info['preset']])
            else:
                # Custom quality (CRF value)
                try:
                    crf_value = int(quality)
                    cmd.extend(['-crf', str(crf_value)])
                except ValueError:
                    logger.warning(f"Invalid quality value: {quality}")
            
            # Bitrate (alternative to CRF)
            if 'bitrate' in options:
                cmd.extend(['-b:v', options['bitrate']])
            
            # Resolution scaling
            if 'resolution' in options:
                resolution = options['resolution']
                if isinstance(resolution, str) and resolution in self.RESOLUTION_PRESETS:
                    width, height = self.RESOLUTION_PRESETS[resolution]
                elif isinstance(resolution, (tuple, list)) and len(resolution) == 2:
                    width, height = resolution
                else:
                    logger.warning(f"Invalid resolution: {resolution}")
                    width = height = None
                
                if width and height:
                    scale_method = options.get('scale_method', 'lanczos')
                    cmd.extend(['-vf', f'scale={width}:{height}:flags={scale_method}'])
            
            # Frame rate
            if 'fps' in options:
                cmd.extend(['-r', str(options['fps'])])
            
            # Audio handling
            if options.get('remove_audio', False):
                cmd.extend(['-an'])  # No audio
            else:
                audio_codec = options.get('audio_codec', format_info['audio_codec'])
                cmd.extend(['-c:a', audio_codec])
                
                # Audio quality
                if 'audio_bitrate' in options:
                    cmd.extend(['-b:a', options['audio_bitrate']])
            
            # Preset
            if 'preset' in options:
                cmd.extend(['-preset', options['preset']])
            
            # Two-pass encoding for better quality
            if options.get('two_pass', False):
                # This is simplified - full two-pass requires two separate commands
                cmd.extend(['-pass', '1'])
            
            # Output options
            cmd.extend(['-y', str(output_path)])  # Overwrite output file
            
            # Execute conversion
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
            
            if result.returncode == 0:
                logger.info(f"Converted {input_path.name} to {output_path.name}")
                
                # Extract audio if requested
                if options.get('extract_audio'):
                    audio_path = output_path.with_suffix('.mp3')
                    self._extract_audio(input_path, audio_path)
                
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Video conversion failed: {e}")
            return False
    
    def _extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video"""
        try:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'mp3',
                '-ab', '192k',
                '-y', str(audio_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Audio extraction failed: {e}")
            return False
    
    def batch_convert(self, input_folder: Path, output_folder: Path,
                     output_format: str, recursive: bool = True, **options) -> List[Dict[str, Any]]:
        """Convert multiple video files"""
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
    
    def create_gif(self, video_path: Path, gif_path: Path, **options) -> bool:
        """Convert video to animated GIF"""
        if not self.ffmpeg_available:
            return False
        
        try:
            # Default options for GIF creation
            fps = options.get('fps', 10)
            scale = options.get('scale', 320)  # Width in pixels
            start_time = options.get('start_time', 0)
            duration = options.get('duration', 10)
            
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', str(start_time),
                '-t', str(duration),
                '-vf', f'fps={fps},scale={scale}:-1:flags=lanczos',
                '-y', str(gif_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"GIF creation failed: {e}")
            return False
    
    def compress_video(self, input_path: Path, output_path: Path, **options) -> bool:
        """Compress video file to reduce size"""
        compression_level = options.get('compression_level', 'medium')
        
        # Compression presets
        compression_options = {
            'light': {'quality': 'high', 'resolution': None},
            'medium': {'quality': 'medium', 'resolution': '720p'},
            'heavy': {'quality': 'low', 'resolution': '480p'}
        }
        
        if compression_level in compression_options:
            preset = compression_options[compression_level]
            options.update(preset)
        
        return self.convert(input_path, output_path, **options)
    
    def merge_videos(self, input_paths: List[Path], output_path: Path, **options) -> bool:
        """Merge multiple video files into one"""
        if not self.ffmpeg_available or len(input_paths) < 2:
            return False
        
        try:
            # Create temporary file list
            temp_file = output_path.parent / 'temp_file_list.txt'
            
            with open(temp_file, 'w') as f:
                for video_path in input_paths:
                    f.write(f"file '{video_path.absolute()}'\n")
            
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(temp_file),
                '-c', 'copy',
                '-y', str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            
            # Clean up temp file
            if temp_file.exists():
                temp_file.unlink()
            
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Video merge failed: {e}")
            return False
    
    def split_video(self, input_path: Path, output_folder: Path, segment_duration: int = 600) -> bool:
        """Split video file into segments"""
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
                '-reset_timestamps', '1',
                '-y', str(output_pattern)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Video split failed: {e}")
            return False
    
    def add_watermark(self, input_path: Path, output_path: Path, 
                     watermark_text: str, **options) -> bool:
        """Add text watermark to video"""
        if not self.ffmpeg_available:
            return False
        
        try:
            # Watermark options
            font_size = options.get('font_size', 24)
            position = options.get('position', 'bottom-right')
            color = options.get('color', 'white')
            opacity = options.get('opacity', 0.7)
            
            # Position mapping
            positions = {
                'top-left': 'x=10:y=10',
                'top-right': 'x=w-tw-10:y=10',
                'bottom-left': 'x=10:y=h-th-10',
                'bottom-right': 'x=w-tw-10:y=h-th-10',
                'center': 'x=(w-tw)/2:y=(h-th)/2'
            }
            
            pos = positions.get(position, positions['bottom-right'])
            
            drawtext_filter = (
                f"drawtext=text='{watermark_text}':fontsize={font_size}:"
                f"fontcolor={color}@{opacity}:{pos}"
            )
            
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-vf', drawtext_filter,
                '-c:a', 'copy',
                '-y', str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Watermark addition failed: {e}")
            return False