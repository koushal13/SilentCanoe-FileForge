"""
PDF Processing Suite for SilentCanoe FileForge

Comprehensive PDF manipulation including:
- PDF to Word/Excel/PowerPoint conversion
- Word/Excel/PowerPoint to PDF conversion
- PDF merge, split, compress
- PDF encryption and password protection
- OCR (Optical Character Recognition)
- Form filling and extraction
- Watermarking and annotations
- PDF optimization and repair
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import fitz  # PyMuPDF
import subprocess
from PIL import Image

logger = logging.getLogger(__name__)

class DocumentConverter:
    """Comprehensive document converter with PDF focus"""
    
    SUPPORTED_INPUT = {
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.txt', '.rtf', '.odt', '.csv', '.html', '.htm'
    }
    
    SUPPORTED_OUTPUT = {
        'pdf': 'PDF',
        'docx': 'Word Document',
        'xlsx': 'Excel Spreadsheet', 
        'pptx': 'PowerPoint Presentation',
        'txt': 'Plain Text',
        'html': 'HTML',
        'rtf': 'Rich Text Format',
        'csv': 'Comma Separated Values'
    }
    
    def __init__(self):
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check for optional dependencies and external tools"""
        self.has_libreoffice = self._check_libreoffice()
        self.has_pandoc = self._check_pandoc()
        self.has_tesseract = self._check_tesseract()
        
        if not any([self.has_libreoffice, self.has_pandoc]):
            logger.warning("No document conversion engines available. Install LibreOffice or Pandoc for full functionality.")
    
    def _check_libreoffice(self) -> bool:
        """Check if LibreOffice is available"""
        try:
            result = subprocess.run(['libreoffice', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def _check_pandoc(self) -> bool:
        """Check if Pandoc is available"""
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def _check_tesseract(self) -> bool:
        """Check if Tesseract OCR is available"""
        try:
            result = subprocess.run(['tesseract', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats"""
        return list(self.SUPPORTED_OUTPUT.keys())
    
    def convert(self, input_path: Path, output_path: Path, **options) -> bool:
        """
        Convert document to another format
        
        Args:
            input_path: Source document
            output_path: Destination file
            **options: Conversion options
        
        Options:
            password: PDF password
            pages: Page range (e.g., "1-5,10")
            quality: Conversion quality for images
            ocr: Enable OCR for scanned PDFs
            preserve_formatting: Maintain original formatting
        """
        
        input_ext = input_path.suffix.lower()
        output_ext = output_path.suffix.lower().lstrip('.')
        
        # PDF-specific operations
        if input_ext == '.pdf':
            return self._convert_from_pdf(input_path, output_path, **options)
        elif output_ext == 'pdf':
            return self._convert_to_pdf(input_path, output_path, **options)
        else:
            return self._convert_document(input_path, output_path, **options)
    
    def _convert_from_pdf(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert PDF to other formats"""
        output_ext = output_path.suffix.lower().lstrip('.')
        
        try:
            # Open PDF
            doc = fitz.open(str(input_path))
            
            # Handle password protection
            if doc.needs_pass:
                password = options.get('password', '')
                if not doc.authenticate(password):
                    logger.error(f"Invalid password for {input_path}")
                    return False
            
            if output_ext in ['txt', 'text']:
                return self._pdf_to_text(doc, output_path, **options)
            elif output_ext in ['html', 'htm']:
                return self._pdf_to_html(doc, output_path, **options)
            elif output_ext in ['docx', 'xlsx', 'pptx']:
                return self._pdf_to_office(input_path, output_path, **options)
            elif output_ext in ['jpg', 'jpeg', 'png']:
                return self._pdf_to_images(doc, output_path, **options)
            else:
                logger.error(f"Unsupported output format: {output_ext}")
                return False
                
        except Exception as e:
            logger.error(f"PDF conversion failed: {e}")
            return False
        finally:
            if 'doc' in locals():
                doc.close()
    
    def _convert_to_pdf(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert other formats to PDF"""
        input_ext = input_path.suffix.lower()
        
        if input_ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt']:
            return self._office_to_pdf(input_path, output_path, **options)
        elif input_ext in ['.txt', '.rtf', '.html', '.htm', '.md']:
            return self._text_to_pdf(input_path, output_path, **options)
        elif input_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
            return self._image_to_pdf(input_path, output_path, **options)
        else:
            logger.error(f"Unsupported input format for PDF: {input_ext}")
            return False
    
    def _convert_document(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert between non-PDF document formats"""
        if self.has_pandoc:
            return self._pandoc_convert(input_path, output_path, **options)
        elif self.has_libreoffice:
            return self._libreoffice_convert(input_path, output_path, **options)
        else:
            logger.error("No document conversion engine available")
            return False
    
    def _pdf_to_text(self, doc: fitz.Document, output_path: Path, **options) -> bool:
        """Extract text from PDF"""
        try:
            text_content = []
            pages = options.get('pages', None)
            
            page_range = self._parse_page_range(pages, doc.page_count) if pages else range(doc.page_count)
            
            for page_num in page_range:
                page = doc[page_num]
                text = page.get_text()
                text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(text_content))
            
            return True
        except Exception as e:
            logger.error(f"PDF to text conversion failed: {e}")
            return False
    
    def _pdf_to_html(self, doc: fitz.Document, output_path: Path, **options) -> bool:
        """Convert PDF to HTML"""
        try:
            html_content = []
            html_content.append("<html><head><title>PDF Conversion</title></head><body>")
            
            pages = options.get('pages', None)
            page_range = self._parse_page_range(pages, doc.page_count) if pages else range(doc.page_count)
            
            for page_num in page_range:
                page = doc[page_num]
                text = page.get_text("html")
                html_content.append(f"<div class='page' id='page-{page_num + 1}'>{text}</div>")
            
            html_content.append("</body></html>")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(html_content))
            
            return True
        except Exception as e:
            logger.error(f"PDF to HTML conversion failed: {e}")
            return False
    
    def _pdf_to_office(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert PDF to Office formats using external tools"""
        if self.has_libreoffice:
            return self._libreoffice_convert(input_path, output_path, **options)
        else:
            logger.error("LibreOffice required for PDF to Office conversion")
            return False
    
    def _office_to_pdf(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert Office documents to PDF"""
        if self.has_libreoffice:
            try:
                cmd = [
                    'libreoffice',
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', str(output_path.parent),
                    str(input_path)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                # LibreOffice creates file with same name but .pdf extension
                expected_output = output_path.parent / (input_path.stem + '.pdf')
                if expected_output.exists() and expected_output != output_path:
                    expected_output.rename(output_path)
                
                return result.returncode == 0 and output_path.exists()
            except Exception as e:
                logger.error(f"LibreOffice conversion failed: {e}")
                return False
        else:
            logger.error("LibreOffice required for Office to PDF conversion")
            return False
    
    def _text_to_pdf(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert text files to PDF"""
        try:
            # Read text content
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create PDF using fitz
            doc = fitz.open()
            page = doc.new_page()
            
            # Simple text formatting
            font_size = options.get('font_size', 12)
            margin = options.get('margin', 72)  # 1 inch
            
            # Split content into lines and add to PDF
            lines = content.split('\n')
            y_position = margin
            
            for line in lines:
                if y_position > page.rect.height - margin:
                    page = doc.new_page()
                    y_position = margin
                
                page.insert_text((margin, y_position), line, fontsize=font_size)
                y_position += font_size + 2
            
            doc.save(str(output_path))
            doc.close()
            return True
            
        except Exception as e:
            logger.error(f"Text to PDF conversion failed: {e}")
            return False
    
    def _image_to_pdf(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert image to PDF"""
        try:
            img = Image.open(input_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(output_path, 'PDF', resolution=100.0)
            return True
            
        except Exception as e:
            logger.error(f"Image to PDF conversion failed: {e}")
            return False
    
    def _libreoffice_convert(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert using LibreOffice"""
        try:
            output_format = output_path.suffix.lower().lstrip('.')
            
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', output_format,
                '--outdir', str(output_path.parent),
                str(input_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # Handle renamed output file
            expected_output = output_path.parent / (input_path.stem + f'.{output_format}')
            if expected_output.exists() and expected_output != output_path:
                expected_output.rename(output_path)
            
            return result.returncode == 0 and output_path.exists()
            
        except Exception as e:
            logger.error(f"LibreOffice conversion failed: {e}")
            return False
    
    def _pandoc_convert(self, input_path: Path, output_path: Path, **options) -> bool:
        """Convert using Pandoc"""
        try:
            cmd = ['pandoc', str(input_path), '-o', str(output_path)]
            
            # Add format specifications if needed
            input_format = options.get('input_format')
            if input_format:
                cmd.extend(['-f', input_format])
            
            output_format = options.get('output_format')
            if output_format:
                cmd.extend(['-t', output_format])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.returncode == 0 and output_path.exists()
            
        except Exception as e:
            logger.error(f"Pandoc conversion failed: {e}")
            return False
    
    def _parse_page_range(self, page_range: str, total_pages: int) -> List[int]:
        """Parse page range string like '1-5,10,15-20'"""
        pages = []
        
        for part in page_range.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start - 1, min(end, total_pages)))
            else:
                page_num = int(part) - 1
                if 0 <= page_num < total_pages:
                    pages.append(page_num)
        
        return sorted(set(pages))
    
    # PDF-specific operations
    def merge_pdfs(self, input_paths: List[Path], output_path: Path, **options) -> bool:
        """Merge multiple PDFs into one"""
        try:
            merged_doc = fitz.open()
            
            for pdf_path in input_paths:
                doc = fitz.open(str(pdf_path))
                merged_doc.insert_pdf(doc)
                doc.close()
            
            merged_doc.save(str(output_path))
            merged_doc.close()
            return True
            
        except Exception as e:
            logger.error(f"PDF merge failed: {e}")
            return False
    
    def split_pdf(self, input_path: Path, output_folder: Path, **options) -> bool:
        """Split PDF into individual pages or ranges"""
        try:
            doc = fitz.open(str(input_path))
            
            split_mode = options.get('split_mode', 'pages')  # 'pages' or 'ranges'
            
            if split_mode == 'pages':
                # Split into individual pages
                for page_num in range(doc.page_count):
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                    
                    output_file = output_folder / f"{input_path.stem}_page_{page_num + 1}.pdf"
                    new_doc.save(str(output_file))
                    new_doc.close()
            
            doc.close()
            return True
            
        except Exception as e:
            logger.error(f"PDF split failed: {e}")
            return False
    
    def compress_pdf(self, input_path: Path, output_path: Path, **options) -> bool:
        """Compress PDF file"""
        try:
            doc = fitz.open(str(input_path))
            
            # Compression options
            compress_level = options.get('compress_level', 'medium')
            
            if compress_level == 'high':
                # Aggressive compression
                doc.save(str(output_path), 
                        garbage=4, 
                        deflate=True, 
                        clean=True,
                        linear=True)
            elif compress_level == 'low':
                # Light compression
                doc.save(str(output_path), 
                        garbage=2, 
                        deflate=True)
            else:  # medium
                doc.save(str(output_path), 
                        garbage=3, 
                        deflate=True, 
                        clean=True)
            
            doc.close()
            return True
            
        except Exception as e:
            logger.error(f"PDF compression failed: {e}")
            return False
    
    def encrypt_pdf(self, input_path: Path, output_path: Path, 
                   user_password: str, owner_password: str = None, **options) -> bool:
        """Encrypt PDF with password protection"""
        try:
            doc = fitz.open(str(input_path))
            
            permissions = options.get('permissions', -1)  # All permissions by default
            encrypt_method = options.get('encrypt_method', fitz.PDF_ENCRYPT_AES_256)
            
            doc.save(str(output_path),
                    encryption=encrypt_method,
                    user_pw=user_password,
                    owner_pw=owner_password or user_password,
                    permissions=permissions)
            
            doc.close()
            return True
            
        except Exception as e:
            logger.error(f"PDF encryption failed: {e}")
            return False
    
    def add_watermark(self, input_path: Path, output_path: Path, 
                     watermark_text: str, **options) -> bool:
        """Add text watermark to PDF"""
        try:
            doc = fitz.open(str(input_path))
            
            font_size = options.get('font_size', 40)
            opacity = options.get('opacity', 0.3)
            rotation = options.get('rotation', 45)
            color = options.get('color', (0.5, 0.5, 0.5))
            
            for page in doc:
                # Calculate position for center of page
                rect = page.rect
                center_x = rect.width / 2
                center_y = rect.height / 2
                
                # Add watermark text
                page.insert_text(
                    (center_x, center_y),
                    watermark_text,
                    fontsize=font_size,
                    color=color,
                    rotate=rotation
                )
            
            doc.save(str(output_path))
            doc.close()
            return True
            
        except Exception as e:
            logger.error(f"PDF watermarking failed: {e}")
            return False