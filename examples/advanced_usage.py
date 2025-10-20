#!/usr/bin/env python3
"""
Advanced FileForge Examples
===========================

This script demonstrates advanced usage patterns and features of FileForge.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Add the parent directory to sys.path so we can import fileforge
sys.path.insert(0, str(Path(__file__).parent.parent))

def batch_image_processing_example():
    """Example: Advanced batch image processing with custom settings."""
    print("🖼️ Advanced Batch Image Processing")
    print("-" * 40)
    
    # Example configuration for batch processing
    batch_config = {
        "input_folder": "photos/raw",
        "output_folder": "photos/processed", 
        "operations": [
            {
                "type": "convert",
                "from_format": "heic",
                "to_format": "jpg",
                "quality": 90
            },
            {
                "type": "resize", 
                "max_dimension": 1920,
                "preserve_aspect": True
            },
            {
                "type": "enhance",
                "brightness": 1.1,
                "contrast": 1.05,
                "saturation": 1.02
            },
            {
                "type": "watermark",
                "text": "© SilentCanoe 2024",
                "position": "bottom-right",
                "opacity": 0.7
            }
        ],
        "parallel_workers": 4,
        "preserve_metadata": True,
        "create_thumbnails": True,
        "thumbnail_size": (300, 300)
    }
    
    print("📋 Batch Configuration:")
    print(json.dumps(batch_config, indent=2))
    
    # Show equivalent CLI command
    print("\n💻 Equivalent CLI Command:")
    cli_cmd = f"""python fileforge.py batch images {batch_config['input_folder']} \\
    --output {batch_config['output_folder']} \\
    --to jpg --quality {batch_config['operations'][0]['quality']} \\
    --resize {batch_config['operations'][1]['max_dimension']} \\
    --enhance brightness=1.1,contrast=1.05,saturation=1.02 \\
    --watermark "© SilentCanoe 2024" --watermark-position bottom-right \\
    --threads {batch_config['parallel_workers']} \\
    --preserve-metadata --create-thumbnails"""
    
    print(cli_cmd)

def pdf_workflow_example():
    """Example: Complete PDF processing workflow."""
    print("\n📄 PDF Processing Workflow")
    print("-" * 40)
    
    workflow_steps = [
        {
            "step": 1,
            "action": "Merge multiple documents",
            "command": "python fileforge.py pdf merge contract.pdf appendix.pdf signatures.pdf final_contract.pdf"
        },
        {
            "step": 2, 
            "action": "Add password protection",
            "command": "python fileforge.py pdf encrypt final_contract.pdf secure_contract.pdf --password 'SecurePass123'"
        },
        {
            "step": 3,
            "action": "Compress for email",
            "command": "python fileforge.py pdf compress secure_contract.pdf email_contract.pdf --level high"
        },
        {
            "step": 4,
            "action": "Add watermark",
            "command": "python fileforge.py pdf watermark email_contract.pdf final_watermarked.pdf 'CONFIDENTIAL' --opacity 0.3"
        },
        {
            "step": 5,
            "action": "Extract specific pages",
            "command": "python fileforge.py pdf split final_watermarked.pdf --pages 1-5,10-15 --output summary.pdf"
        }
    ]
    
    for step in workflow_steps:
        print(f"📌 Step {step['step']}: {step['action']}")
        print(f"   {step['command']}")
        print()

def media_conversion_pipeline():
    """Example: Media conversion pipeline for content creators."""
    print("🎬 Media Conversion Pipeline")
    print("-" * 40)
    
    pipeline_config = {
        "video_processing": {
            "input_formats": ["mov", "avi", "mkv"],
            "output_format": "mp4",
            "resolutions": {
                "youtube": "1080p",
                "instagram": "720p", 
                "tiktok": "1080p_vertical"
            },
            "compression": "medium",
            "watermark": "SilentCanoe Studios"
        },
        "audio_processing": {
            "extract_audio": True,
            "audio_format": "mp3",
            "quality": "high",
            "normalize": True,
            "fade_in": 0.5,
            "fade_out": 1.0
        }
    }
    
    print("📋 Pipeline Configuration:")
    print(json.dumps(pipeline_config, indent=2))
    
    # Show step-by-step commands
    commands = [
        "# Convert video for YouTube (1080p)",
        "python fileforge.py convert video raw_footage.mov youtube_video.mp4 --resolution 1080p --quality medium",
        "",
        "# Extract and process audio",
        "python fileforge.py convert audio raw_footage.mov audio_track.mp3 --quality high --normalize --fade-in 0.5 --fade-out 1.0",
        "",
        "# Create Instagram version (720p)",  
        "python fileforge.py convert video raw_footage.mov instagram_video.mp4 --resolution 720p --watermark 'SilentCanoe Studios'",
        "",
        "# Batch process entire folder",
        "python fileforge.py batch videos raw_footage/ --to mp4 --resolution 1080p --recursive --threads 6"
    ]
    
    print("\n💻 Pipeline Commands:")
    for cmd in commands:
        print(cmd)

def automation_script_example():
    """Example: Automation script for daily workflows."""
    print("\n🤖 Automation Script Example")
    print("-" * 40)
    
    script_content = '''#!/usr/bin/env python3
"""
Daily File Processing Automation
Processes files from watch folders and organizes output
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from fileforge import ConversionEngine, BatchProcessor

def daily_photo_processing():
    """Process daily photo uploads."""
    watch_folder = Path("~/Desktop/Photos_To_Process").expanduser()
    output_base = Path("~/Pictures/Processed").expanduser()
    
    if not watch_folder.exists():
        return
    
    # Create dated output folder
    today = datetime.now().strftime("%Y-%m-%d")
    output_folder = output_base / today
    output_folder.mkdir(parents=True, exist_ok=True)
    
    engine = ConversionEngine()
    
    # Process HEIC files
    heic_files = list(watch_folder.glob("*.heic")) + list(watch_folder.glob("*.HEIC"))
    
    for heic_file in heic_files:
        jpg_output = output_folder / f"{heic_file.stem}.jpg"
        
        success = engine.convert_single(
            str(heic_file),
            str(jpg_output),
            quality=90,
            preserve_metadata=True
        )
        
        if success:
            # Move original to archive
            archive_folder = output_folder / "originals"
            archive_folder.mkdir(exist_ok=True)
            shutil.move(str(heic_file), str(archive_folder / heic_file.name))
            print(f"✅ Processed: {heic_file.name} -> {jpg_output.name}")
        else:
            print(f"❌ Failed: {heic_file.name}")

def document_organization():
    """Organize and convert documents."""
    doc_folder = Path("~/Documents/Inbox").expanduser()
    
    # Convert Word docs to PDF for archival
    word_files = list(doc_folder.glob("*.docx")) + list(doc_folder.glob("*.doc"))
    
    for doc in word_files:
        pdf_output = doc.parent / f"{doc.stem}.pdf"
        print(f"Converting: {doc.name} -> {pdf_output.name}")

if __name__ == "__main__":
    daily_photo_processing()
    document_organization()
'''
    
    print("📄 Automation Script Content:")
    print(script_content)

def performance_optimization_tips():
    """Example: Performance optimization strategies."""
    print("⚡ Performance Optimization Tips")
    print("-" * 40)
    
    optimization_tips = [
        {
            "category": "Hardware Optimization",
            "tips": [
                "Use SSD storage for 3-5x faster I/O operations",
                "Increase RAM for processing large files (8GB+ recommended)",
                "Use multi-core CPU with --threads parameter",
                "Enable GPU acceleration for video processing (if available)"
            ]
        },
        {
            "category": "Batch Processing",
            "tips": [
                "Set optimal thread count: CPU cores - 1",
                "Process files in size-sorted order (small files first)",
                "Use file filtering to avoid unnecessary conversions",
                "Enable resume functionality for large batches"
            ]
        },
        {
            "category": "Quality vs Speed",
            "tips": [
                "Use 'fast' quality preset for previews", 
                "Use 'high' quality only for final output",
                "Compress images to 85% quality for web use",
                "Use progressive JPEG for faster loading"
            ]
        },
        {
            "category": "Memory Management",
            "tips": [
                "Process files sequentially for large files (>100MB)",
                "Use streaming for video conversions",
                "Clear cache between batches",
                "Monitor memory usage with task manager"
            ]
        }
    ]
    
    for category_info in optimization_tips:
        print(f"\n📊 {category_info['category']}:")
        for tip in category_info['tips']:
            print(f"   • {tip}")

def main():
    """Run all advanced examples."""
    print("🔧 SilentCanoe FileForge - Advanced Examples")
    print("=" * 50)
    
    batch_image_processing_example()
    pdf_workflow_example()
    media_conversion_pipeline()
    automation_script_example()
    performance_optimization_tips()
    
    print("\n" + "=" * 50)
    print("🎓 Advanced examples complete!")
    print("💡 Modify these examples for your specific workflows")
    print("🔧 Create custom scripts for repetitive tasks")
    print("📚 Check the documentation for more features")

if __name__ == "__main__":
    main()