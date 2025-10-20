#!/usr/bin/env python3
"""
SilentCanoe FileForge - Complete Conversion Utility
Full-featured file converter with GUI and actual conversion capabilities
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path
import shutil
import threading
import json
from datetime import datetime

# Import our professional image converter
try:
    from professional_image_converter import ImageConverter
    PROFESSIONAL_CONVERTER_AVAILABLE = True
except ImportError:
    PROFESSIONAL_CONVERTER_AVAILABLE = False
    print("⚠️ Professional Image Converter not available")

# Try to import optional libraries for document processing
try:
    from PyPDF2 import PdfReader, PdfWriter, PdfMerger
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    HTML_PARSING_AVAILABLE = True
except ImportError:
    HTML_PARSING_AVAILABLE = False

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    PDF_CREATION_AVAILABLE = True
except ImportError:
    PDF_CREATION_AVAILABLE = False

try:
    from PIL import Image, ImageOps
    import pillow_heif
    IMAGING_AVAILABLE = True
except ImportError:
    IMAGING_AVAILABLE = False
    PROFESSIONAL_CONVERTER_AVAILABLE = False
    print("⚠️ Professional converter not available, using basic conversion")

class FileForgeConverter:
    """Complete file conversion utility with working conversion features."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔧 SilentCanoe FileForge - File Converter")
        self.root.geometry("1200x800")
        
        # Maximize window automatically
        self.root.state('zoomed')  # Windows maximization
        self.root.configure(bg='white')
        
        # Initialize professional image converter
        if PROFESSIONAL_CONVERTER_AVAILABLE:
            self.image_converter = ImageConverter()
            print("✅ Professional image converter loaded")
        else:
            self.image_converter = None
            print("⚠️ Using basic image conversion")
        
        # Conversion settings
        self.selected_files = []
        self.output_directory = ""
        self.current_operation = ""
        
        # Supported conversions (working implementations)
        self.conversions = {
            'image': {
                'formats': ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp'],
                'targets': ['JPG', 'PNG', 'BMP', 'TIFF', 'WebP'],
                'operations': ['Convert', 'Resize', 'Rotate', 'Enhance', 'Thumbnail']
            },
            'text': {
                'formats': ['txt', 'md', 'rtf', 'csv', 'json', 'xml'],
                'targets': ['TXT', 'MD', 'HTML', 'JSON', 'CSV'],
                'operations': ['Convert', 'Format', 'Clean', 'Encode']
            },
            'document': {
                'formats': ['pdf', 'docx', 'doc', 'odt'],
                'targets': ['PDF', 'DOCX', 'TXT', 'HTML'],
                'operations': ['Convert', 'Merge', 'Split', 'Compress']
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the complete user interface."""
        # Header
        self.create_header()
        
        # Main content with notebook
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self):
        """Create header section."""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title and subtitle
        title_label = tk.Label(
            header_frame,
            text="🔧 SilentCanoe FileForge",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Universal File Conversion Utility - Full Version",
            font=('Arial', 11),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
    def create_main_content(self):
        """Create main content area with tabs."""
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create notebook for different conversion types
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Image Converter Tab
        self.create_image_converter_tab()
        
        # Document Converter Tab
        self.create_document_converter_tab()
        
        # Text Converter Tab
        self.create_text_converter_tab()
        
        # Batch Processor Tab
        self.create_batch_processor_tab()
        
        # Settings Tab
        self.create_settings_tab()
        
    def create_image_converter_tab(self):
        """Create image conversion tab with working features."""
        img_frame = ttk.Frame(self.notebook)
        self.notebook.add(img_frame, text="🖼️ Image Converter")
        
        # File selection area
        selection_frame = tk.LabelFrame(img_frame, text="📁 Select Images", font=('Arial', 10, 'bold'))
        selection_frame.pack(fill='x', padx=10, pady=10)
        
        # File selection buttons
        btn_frame = tk.Frame(selection_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.select_images_btn = tk.Button(
            btn_frame,
            text="📁 Select Images",
            command=self.select_image_files,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.select_images_btn.pack(side='left', padx=(0, 10))
        
        self.clear_images_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear",
            command=self.clear_image_selection,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.clear_images_btn.pack(side='left')
        
        # Selected files display
        self.image_files_listbox = tk.Listbox(selection_frame, height=6)
        self.image_files_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Conversion settings
        settings_frame = tk.LabelFrame(img_frame, text="⚙️ Conversion Settings", font=('Arial', 10, 'bold'))
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        # Format selection
        format_frame = tk.Frame(settings_frame)
        format_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(format_frame, text="Output Format:", font=('Arial', 10, 'bold')).pack(side='left')
        
        self.image_format_var = tk.StringVar(value="JPG")
        format_combo = ttk.Combobox(format_frame, textvariable=self.image_format_var, 
                                   values=['JPG', 'PNG', 'BMP', 'TIFF', 'WebP'], state='readonly')
        format_combo.pack(side='left', padx=(10, 0))
        
        # Quality setting
        quality_frame = tk.Frame(settings_frame)
        quality_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(quality_frame, text="Quality:", font=('Arial', 10, 'bold')).pack(side='left')
        
        self.quality_var = tk.IntVar(value=90)
        quality_scale = tk.Scale(quality_frame, from_=10, to=100, orient='horizontal',
                               variable=self.quality_var, length=200)
        quality_scale.pack(side='left', padx=(10, 0))
        
        # Resize options
        resize_frame = tk.Frame(settings_frame)
        resize_frame.pack(fill='x', padx=10, pady=5)
        
        self.resize_enabled = tk.BooleanVar()
        resize_check = tk.Checkbutton(resize_frame, text="Resize Images", 
                                    variable=self.resize_enabled, font=('Arial', 10, 'bold'))
        resize_check.pack(side='left')
        
        tk.Label(resize_frame, text="Width:").pack(side='left', padx=(20, 5))
        self.width_var = tk.StringVar(value="800")
        width_entry = tk.Entry(resize_frame, textvariable=self.width_var, width=8)
        width_entry.pack(side='left')
        
        tk.Label(resize_frame, text="Height:").pack(side='left', padx=(10, 5))
        self.height_var = tk.StringVar(value="600")
        height_entry = tk.Entry(resize_frame, textvariable=self.height_var, width=8)
        height_entry.pack(side='left')
        
        # Output directory
        output_frame = tk.LabelFrame(img_frame, text="📂 Output Directory", font=('Arial', 10, 'bold'))
        output_frame.pack(fill='x', padx=10, pady=10)
        
        output_btn_frame = tk.Frame(output_frame)
        output_btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.select_output_btn = tk.Button(
            output_btn_frame,
            text="📂 Select Output Folder",
            command=self.select_output_directory,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.select_output_btn.pack(side='left')
        
        self.output_label = tk.Label(output_btn_frame, text="No output directory selected", 
                                   fg='#7f8c8d', font=('Arial', 10))
        self.output_label.pack(side='left', padx=(15, 0))
        
        # Convert button
        convert_frame = tk.Frame(img_frame)
        convert_frame.pack(fill='x', padx=10, pady=20)
        
        # Conversion engine indicator
        engine_frame = tk.Frame(convert_frame)
        engine_frame.pack(fill='x', pady=(0, 10))
        
        engine_text = "🔧 PROFESSIONAL ENGINE (6-Checkpoint Validation)" if PROFESSIONAL_CONVERTER_AVAILABLE else "⚠️ BASIC ENGINE (Limited Validation)"
        engine_color = "#27ae60" if PROFESSIONAL_CONVERTER_AVAILABLE else "#e67e22"
        
        tk.Label(engine_frame, text="Conversion Engine:", font=('Arial', 10, 'bold')).pack(side='left')
        tk.Label(engine_frame, text=engine_text, fg=engine_color, font=('Arial', 10, 'bold')).pack(side='left', padx=(10, 0))
        
        self.convert_images_btn = tk.Button(
            convert_frame,
            text="🚀 CONVERT IMAGES",
            command=self.convert_images,
            bg='#f39c12',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=30,
            pady=15
        )
        self.convert_images_btn.pack()
        
    def create_document_converter_tab(self):
        """Create document conversion tab with working features."""
        doc_frame = ttk.Frame(self.notebook)
        self.notebook.add(doc_frame, text="📄 Document Converter")
        
        # Title
        tk.Label(doc_frame, text="📄 Document Converter", 
                font=('Arial', 20, 'bold'), fg='#2c3e50').pack(pady=20)
        
        # File selection
        selection_frame = tk.LabelFrame(doc_frame, text="📁 Select Documents", font=('Arial', 10, 'bold'))
        selection_frame.pack(fill='x', padx=20, pady=10)
        
        btn_frame = tk.Frame(selection_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.select_docs_btn = tk.Button(
            btn_frame,
            text="� Select Documents",
            command=self.select_document_files,
            bg='#e67e22',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.select_docs_btn.pack(side='left', padx=(0, 10))
        
        self.clear_docs_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear",
            command=self.clear_document_selection,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.clear_docs_btn.pack(side='left')
        
        # Selected files display
        self.doc_files_listbox = tk.Listbox(selection_frame, height=6)
        self.doc_files_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Document operations
        operations_frame = tk.LabelFrame(doc_frame, text="⚙️ Document Operations", font=('Arial', 10, 'bold'))
        operations_frame.pack(fill='x', padx=20, pady=10)
        
        # Create three columns for operations
        col1 = tk.Frame(operations_frame)
        col1.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        col2 = tk.Frame(operations_frame)
        col2.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        col3 = tk.Frame(operations_frame)
        col3.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # PDF Operations
        tk.Label(col1, text="📄 PDF Operations", font=('Arial', 11, 'bold'), fg='#c0392b').pack(pady=5)
        
        pdf_ops = [
            ("🔗 Merge PDFs", self.merge_pdfs),
            ("✂️ Split PDF", self.split_pdf),
            ("🗜️ Compress PDF", self.compress_pdf),
            ("🔒 Encrypt PDF", self.encrypt_pdf)
        ]
        
        for text, command in pdf_ops:
            btn = tk.Button(col1, text=text, command=command, bg='#c0392b', fg='white',
                          font=('Arial', 9, 'bold'), pady=5)
            btn.pack(fill='x', pady=2)
        
        # Conversion Operations
        tk.Label(col2, text="🔄 Format Conversion", font=('Arial', 11, 'bold'), fg='#8e44ad').pack(pady=5)
        
        conversion_ops = [
            ("📄→📝 PDF to Text", lambda: self.convert_document("txt")),
            ("📝→📄 Text to PDF", lambda: self.convert_document("pdf")),
            ("📄→🌐 PDF to HTML", lambda: self.convert_document("html")),
            ("📝→📋 Text to Markdown", lambda: self.convert_document("md"))
        ]
        
        for text, command in conversion_ops:
            btn = tk.Button(col2, text=text, command=command, bg='#8e44ad', fg='white',
                          font=('Arial', 9, 'bold'), pady=5)
            btn.pack(fill='x', pady=2)
        
        # Text Operations
        tk.Label(col3, text="📝 Text Processing", font=('Arial', 11, 'bold'), fg='#27ae60').pack(pady=5)
        
        text_ops = [
            ("🔤 Extract Text", self.extract_text),
            ("📊 Word Count", self.word_count),
            ("🔍 Find & Replace", self.find_replace),
            ("📋 Format Text", self.format_text)
        ]
        
        for text, command in text_ops:
            btn = tk.Button(col3, text=text, command=command, bg='#27ae60', fg='white',
                          font=('Arial', 9, 'bold'), pady=5)
            btn.pack(fill='x', pady=2)
        
        # Output settings
        output_frame = tk.LabelFrame(doc_frame, text="� Output Settings", font=('Arial', 10, 'bold'))
        output_frame.pack(fill='x', padx=20, pady=10)
        
        output_controls = tk.Frame(output_frame)
        output_controls.pack(fill='x', padx=10, pady=10)
        
        # Output directory
        self.select_doc_output_btn = tk.Button(
            output_controls,
            text="📂 Select Output Folder",
            command=self.select_document_output_directory,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.select_doc_output_btn.pack(side='left')
        
        self.doc_output_label = tk.Label(output_controls, text="Same as source directory", 
                                       fg='#7f8c8d', font=('Arial', 10))
        self.doc_output_label.pack(side='left', padx=(15, 0))
        
    # Document Converter Methods
    def select_document_files(self):
        """Select document files for processing."""
        file_types = [
            ("All Documents", "*.pdf;*.txt;*.docx;*.html;*.md;*.rtf"),
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt"),
            ("Word documents", "*.docx"),
            ("HTML files", "*.html"),
            ("Markdown files", "*.md"),
            ("Rich Text Format", "*.rtf"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Document Files",
            filetypes=file_types
        )
        
        if files:
            self.selected_doc_files.extend(files)
            self.update_document_list()
    
    def clear_document_selection(self):
        """Clear selected document files."""
        self.selected_doc_files = []
        self.update_document_list()
    
    def update_document_list(self):
        """Update the document files listbox."""
        self.doc_files_listbox.delete(0, tk.END)
        for file_path in self.selected_doc_files:
            filename = os.path.basename(file_path)
            self.doc_files_listbox.insert(tk.END, filename)
    
    def select_document_output_directory(self):
        """Select output directory for document operations."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.doc_output_directory = directory
            self.doc_output_label.config(text=f"Output: {os.path.basename(directory)}")
    
    def merge_pdfs(self):
        """Merge multiple PDF files into one."""
        if not self.selected_doc_files:
            messagebox.showwarning("Warning", "Please select PDF files to merge.")
            return
        
        if not PDF_AVAILABLE:
            messagebox.showerror("Error", "PyPDF2 library not installed.\nPlease install it: pip install PyPDF2")
            return
        
        pdf_files = [f for f in self.selected_doc_files if f.lower().endswith('.pdf')]
        if len(pdf_files) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 PDF files to merge.")
            return
        
        try:
            output_file = filedialog.asksaveasfilename(
                title="Save merged PDF as...",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if output_file:
                merger = PdfMerger()
                for pdf_file in pdf_files:
                    merger.append(pdf_file)
                
                merger.write(output_file)
                merger.close()
                
                messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved as: {os.path.basename(output_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs: {str(e)}")
    
    def split_pdf(self):
        """Split a PDF file into individual pages."""
        if not PDF_AVAILABLE:
            messagebox.showerror("Error", "PyPDF2 library not installed.\nPlease install it: pip install PyPDF2")
            return
            
        pdf_files = [f for f in self.selected_doc_files if f.lower().endswith('.pdf')]
        if not pdf_files:
            messagebox.showwarning("Warning", "Please select a PDF file to split.")
            return
        
        if len(pdf_files) > 1:
            messagebox.showwarning("Warning", "Please select only one PDF file to split.")
            return
        
        try:
            output_dir = self.doc_output_directory or os.path.dirname(pdf_files[0])
            
            reader = PdfReader(pdf_files[0])
            base_name = os.path.splitext(os.path.basename(pdf_files[0]))[0]
            
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                output_file = os.path.join(output_dir, f"{base_name}_page_{i+1}.pdf")
                with open(output_file, 'wb') as f:
                    writer.write(f)
            
            messagebox.showinfo("Success", f"PDF split into {len(reader.pages)} pages!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to split PDF: {str(e)}")
    
    def compress_pdf(self):
        """Compress PDF files to reduce size."""
        pdf_files = [f for f in self.selected_doc_files if f.lower().endswith('.pdf')]
        if not pdf_files:
            messagebox.showwarning("Warning", "Please select PDF files to compress.")
            return
        
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            for pdf_file in pdf_files:
                reader = PdfReader(pdf_file)
                writer = PdfWriter()
                
                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)
                
                output_dir = self.doc_output_directory or os.path.dirname(pdf_file)
                base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                output_file = os.path.join(output_dir, f"{base_name}_compressed.pdf")
                
                with open(output_file, 'wb') as f:
                    writer.write(f)
            
            messagebox.showinfo("Success", f"Compressed {len(pdf_files)} PDF file(s)!")
        except ImportError:
            messagebox.showerror("Error", "PyPDF2 library not installed. Please install it: pip install PyPDF2")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compress PDF: {str(e)}")
    
    def encrypt_pdf(self):
        """Encrypt PDF files with a password."""
        pdf_files = [f for f in self.selected_doc_files if f.lower().endswith('.pdf')]
        if not pdf_files:
            messagebox.showwarning("Warning", "Please select PDF files to encrypt.")
            return
        
        # Simple password dialog
        password = simpledialog.askstring("Password", "Enter password for encryption:", show='*')
        if not password:
            return
        
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            for pdf_file in pdf_files:
                reader = PdfReader(pdf_file)
                writer = PdfWriter()
                
                for page in reader.pages:
                    writer.add_page(page)
                
                writer.encrypt(password)
                
                output_dir = self.doc_output_directory or os.path.dirname(pdf_file)
                base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                output_file = os.path.join(output_dir, f"{base_name}_encrypted.pdf")
                
                with open(output_file, 'wb') as f:
                    writer.write(f)
            
            messagebox.showinfo("Success", f"Encrypted {len(pdf_files)} PDF file(s)!")
        except ImportError:
            messagebox.showerror("Error", "PyPDF2 library not installed. Please install it: pip install PyPDF2")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt PDF: {str(e)}")
    
    def convert_document(self, target_format):
        """Convert documents to target format."""
        if not self.selected_doc_files:
            messagebox.showwarning("Warning", "Please select documents to convert.")
            return
        
        try:
            output_dir = self.doc_output_directory or os.path.dirname(self.selected_doc_files[0])
            converted_count = 0
            
            for file_path in self.selected_doc_files:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if target_format == "txt":
                    output_file = os.path.join(output_dir, f"{base_name}.txt")
                    self._convert_to_text(file_path, output_file)
                elif target_format == "pdf":
                    output_file = os.path.join(output_dir, f"{base_name}.pdf")
                    self._convert_to_pdf(file_path, output_file)
                elif target_format == "html":
                    output_file = os.path.join(output_dir, f"{base_name}.html")
                    self._convert_to_html(file_path, output_file)
                elif target_format == "md":
                    output_file = os.path.join(output_dir, f"{base_name}.md")
                    self._convert_to_markdown(file_path, output_file)
                
                converted_count += 1
            
            messagebox.showinfo("Success", f"Converted {converted_count} document(s) to {target_format.upper()}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert documents: {str(e)}")
    
    def _convert_to_text(self, input_file, output_file):
        """Convert various formats to text."""
        file_ext = os.path.splitext(input_file)[1].lower()
        
        if file_ext == '.pdf':
            if not PDF_AVAILABLE:
                raise Exception("PyPDF2 library not installed")
            
            reader = PdfReader(input_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
        elif file_ext in ['.html', '.htm']:
            if not HTML_PARSING_AVAILABLE:
                # Fallback: basic HTML tag removal
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple tag removal (not perfect but functional)
                    import re
                    text = re.sub('<[^<]+?>', '', content)
            else:
                with open(input_file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    text = soup.get_text()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            # For plain text files and others, just copy
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def _convert_to_pdf(self, input_file, output_file):
        """Convert text files to PDF."""
        if not PDF_CREATION_AVAILABLE:
            raise Exception("ReportLab library not installed")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        c = canvas.Canvas(output_file, pagesize=letter)
        width, height = letter
        
        # Simple text wrapping
        lines = content.split('\n')
        y = height - 50
        
        for line in lines:
            if y < 50:  # Start new page
                c.showPage()
                y = height - 50
            
            c.drawString(50, y, line[:80])  # Limit line length
            y -= 15
        
        c.save()
    
    def _convert_to_html(self, input_file, output_file):
        """Convert text files to HTML."""
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{os.path.basename(input_file)}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        pre {{ white-space: pre-wrap; }}
    </style>
</head>
<body>
    <h1>{os.path.basename(input_file)}</h1>
    <pre>{content}</pre>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _convert_to_markdown(self, input_file, output_file):
        """Convert text files to Markdown."""
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple conversion - add markdown header
        markdown_content = f"# {os.path.basename(input_file)}\n\n{content}"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def extract_text(self):
        """Extract text from documents."""
        if not self.selected_doc_files:
            messagebox.showwarning("Warning", "Please select documents to extract text from.")
            return
        
        try:
            output_dir = self.doc_output_directory or os.path.dirname(self.selected_doc_files[0])
            extracted_count = 0
            
            for file_path in self.selected_doc_files:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_file = os.path.join(output_dir, f"{base_name}_extracted.txt")
                self._convert_to_text(file_path, output_file)
                extracted_count += 1
            
            messagebox.showinfo("Success", f"Extracted text from {extracted_count} document(s)!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text: {str(e)}")
    
    def word_count(self):
        """Count words in selected documents."""
        if not self.selected_doc_files:
            messagebox.showwarning("Warning", "Please select documents to count words.")
            return
        
        try:
            total_words = 0
            total_chars = 0
            total_lines = 0
            results = []
            
            for file_path in self.selected_doc_files:
                # Extract text first
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if file_ext == '.pdf':
                    if PDF_AVAILABLE:
                        reader = PdfReader(file_path)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                    else:
                        text = "PDF reading requires PyPDF2 library"
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                
                words = len(text.split())
                chars = len(text)
                lines = len(text.split('\n'))
                
                total_words += words
                total_chars += chars
                total_lines += lines
                
                results.append(f"{os.path.basename(file_path)}: {words} words, {chars} characters, {lines} lines")
            
            result_text = "\n".join(results)
            result_text += f"\n\nTOTAL: {total_words} words, {total_chars} characters, {total_lines} lines"
            
            # Show results in a new window
            result_window = tk.Toplevel(self.root)
            result_window.title("Word Count Results")
            result_window.geometry("500x400")
            
            text_widget = tk.Text(result_window, wrap='word')
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            text_widget.insert('1.0', result_text)
            text_widget.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to count words: {str(e)}")
    
    def find_replace(self):
        """Find and replace text in documents."""
        if not self.selected_doc_files:
            messagebox.showwarning("Warning", "Please select documents for find & replace.")
            return
        
        # Create find & replace dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Find & Replace")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Find:", font=('Arial', 10, 'bold')).pack(pady=5)
        find_entry = tk.Entry(dialog, width=50)
        find_entry.pack(pady=5)
        
        tk.Label(dialog, text="Replace with:", font=('Arial', 10, 'bold')).pack(pady=5)
        replace_entry = tk.Entry(dialog, width=50)
        replace_entry.pack(pady=5)
        
        def perform_replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            
            if not find_text:
                messagebox.showwarning("Warning", "Please enter text to find.")
                return
            
            try:
                output_dir = self.doc_output_directory or os.path.dirname(self.selected_doc_files[0])
                processed_count = 0
                
                for file_path in self.selected_doc_files:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content.replace(find_text, replace_text)
                    
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_file = os.path.join(output_dir, f"{base_name}_replaced.txt")
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    processed_count += 1
                
                messagebox.showinfo("Success", f"Find & replace completed on {processed_count} file(s)!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to perform find & replace: {str(e)}")
        
        tk.Button(dialog, text="Replace All", command=perform_replace, 
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def format_text(self):
        """Format text documents (remove extra spaces, fix line breaks, etc.)."""
        if not self.selected_doc_files:
            messagebox.showwarning("Warning", "Please select text documents to format.")
            return
        
        try:
            output_dir = self.doc_output_directory or os.path.dirname(self.selected_doc_files[0])
            formatted_count = 0
            
            for file_path in self.selected_doc_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic text formatting
                # Remove extra whitespace
                lines = content.split('\n')
                formatted_lines = []
                
                for line in lines:
                    # Remove leading/trailing whitespace
                    line = line.strip()
                    # Replace multiple spaces with single space
                    line = ' '.join(line.split())
                    formatted_lines.append(line)
                
                # Remove empty lines
                formatted_lines = [line for line in formatted_lines if line]
                
                formatted_content = '\n'.join(formatted_lines)
                
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_file = os.path.join(output_dir, f"{base_name}_formatted.txt")
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                formatted_count += 1
            
            messagebox.showinfo("Success", f"Formatted {formatted_count} document(s)!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to format documents: {str(e)}")
        
    def create_text_converter_tab(self):
        """Create text conversion tab."""
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="📝 Text Converter")
        
        # Text converter implementation
        tk.Label(text_frame, text="📝 Text File Converter", 
                font=('Arial', 20, 'bold'), fg='#2c3e50').pack(pady=30)
        
        # Text area for input
        input_frame = tk.LabelFrame(text_frame, text="Input Text", font=('Arial', 10, 'bold'))
        input_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.text_input = tk.Text(input_frame, height=10, wrap=tk.WORD, font=('Consolas', 10))
        self.text_input.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load file button
        load_frame = tk.Frame(text_frame)
        load_frame.pack(fill='x', padx=20, pady=5)
        
        load_btn = tk.Button(load_frame, text="📁 Load Text File", 
                           command=self.load_text_file, bg='#3498db', fg='white',
                           font=('Arial', 10, 'bold'), padx=15, pady=5)
        load_btn.pack(side='left')
        
        # Format options
        format_frame = tk.Frame(text_frame)
        format_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(format_frame, text="Convert to:", font=('Arial', 10, 'bold')).pack(side='left')
        
        self.text_format_var = tk.StringVar(value="HTML")
        text_combo = ttk.Combobox(format_frame, textvariable=self.text_format_var,
                                values=['HTML', 'JSON', 'XML', 'CSV', 'MD'], state='readonly')
        text_combo.pack(side='left', padx=(10, 0))
        
        convert_text_btn = tk.Button(format_frame, text="🔄 Convert Text",
                                   command=self.convert_text, bg='#27ae60', fg='white',
                                   font=('Arial', 10, 'bold'), padx=15, pady=5)
        convert_text_btn.pack(side='left', padx=(20, 0))
        
    def create_batch_processor_tab(self):
        """Create advanced batch processing tab with filters and live updates."""
        batch_frame = ttk.Frame(self.notebook)
        self.notebook.add(batch_frame, text="⚡ Advanced Batch Processor")
        
        # Title
        tk.Label(batch_frame, text="⚡ Advanced Batch File Processor", 
                font=('Arial', 20, 'bold'), fg='#2c3e50').pack(pady=20)
        
        # Create main container with scrollable content
        main_container = tk.Frame(batch_frame)
        main_container.pack(fill='both', expand=True, padx=20)
        
        # Left panel - Configuration
        left_panel = tk.Frame(main_container)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Directory selection
        dir_frame = tk.LabelFrame(left_panel, text="📁 Source Configuration", font=('Arial', 10, 'bold'))
        dir_frame.pack(fill='x', pady=10)
        
        # Root directory
        root_dir_frame = tk.Frame(dir_frame)
        root_dir_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(root_dir_frame, text="Root Directory:", font=('Arial', 9, 'bold')).pack(anchor='w')
        
        dir_select_frame = tk.Frame(root_dir_frame)
        dir_select_frame.pack(fill='x', pady=5)
        
        select_dir_btn = tk.Button(dir_select_frame, text="📂 Browse",
                                 command=self.select_batch_root_directory, bg='#9b59b6', fg='white',
                                 font=('Arial', 9, 'bold'), padx=15, pady=5)
        select_dir_btn.pack(side='left')
        
        self.batch_root_dir_label = tk.Label(dir_select_frame, text="No directory selected",
                                           fg='#7f8c8d', font=('Arial', 9))
        self.batch_root_dir_label.pack(side='left', padx=(10, 0))
        
        # Recursive processing option
        self.recursive_var = tk.BooleanVar(value=True)
        recursive_check = tk.Checkbutton(dir_frame, text="🔄 Include subdirectories (recursive)",
                                       variable=self.recursive_var, font=('Arial', 9, 'bold'))
        recursive_check.pack(anchor='w', padx=10, pady=5)
        
        # Filter configuration
        filter_frame = tk.LabelFrame(left_panel, text="🔍 File Filters", font=('Arial', 10, 'bold'))
        filter_frame.pack(fill='x', pady=10)
        
        # From format filter
        from_format_frame = tk.Frame(filter_frame)
        from_format_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(from_format_frame, text="From Format:", font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.from_format_var = tk.StringVar(value="All Images")
        from_format_combo = ttk.Combobox(from_format_frame, textvariable=self.from_format_var,
                                       values=["All Images", "HEIC/HEIF", "PNG", "JPEG", "BMP", "TIFF", "WebP", "GIF"],
                                       state='readonly', width=20)
        from_format_combo.pack(pady=2)
        
        # To format
        to_format_frame = tk.Frame(filter_frame)
        to_format_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(to_format_frame, text="To Format:", font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.batch_to_format_var = tk.StringVar(value="JPG")
        to_format_combo = ttk.Combobox(to_format_frame, textvariable=self.batch_to_format_var,
                                     values=["JPG", "PNG", "WebP", "BMP", "TIFF"], state='readonly', width=20)
        to_format_combo.pack(pady=2)
        
        # Quality settings
        quality_frame = tk.Frame(filter_frame)
        quality_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(quality_frame, text="Quality:", font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.batch_quality_var = tk.IntVar(value=90)
        quality_scale = tk.Scale(quality_frame, from_=10, to=100, orient='horizontal',
                               variable=self.batch_quality_var, length=150)
        quality_scale.pack(pady=2)
        
        # Advanced options
        options_frame = tk.LabelFrame(left_panel, text="⚙️ Advanced Options", font=('Arial', 10, 'bold'))
        options_frame.pack(fill='x', pady=10)
        
        # Delete original option
        self.delete_original_var = tk.BooleanVar()
        delete_check = tk.Checkbutton(options_frame, text="🗑️ Delete original files after conversion",
                                    variable=self.delete_original_var, font=('Arial', 9, 'bold'), fg='#e74c3c')
        delete_check.pack(anchor='w', padx=10, pady=5)
        
        # Resize option
        self.batch_resize_var = tk.BooleanVar()
        resize_check = tk.Checkbutton(options_frame, text="📏 Resize images",
                                    variable=self.batch_resize_var, font=('Arial', 9, 'bold'))
        resize_check.pack(anchor='w', padx=10, pady=2)
        
        resize_settings_frame = tk.Frame(options_frame)
        resize_settings_frame.pack(fill='x', padx=20, pady=2)
        
        tk.Label(resize_settings_frame, text="Max Width:", font=('Arial', 8)).pack(side='left')
        self.batch_max_width_var = tk.StringVar(value="1920")
        width_entry = tk.Entry(resize_settings_frame, textvariable=self.batch_max_width_var, width=8)
        width_entry.pack(side='left', padx=5)
        
        tk.Label(resize_settings_frame, text="Max Height:", font=('Arial', 8)).pack(side='left', padx=(10, 0))
        self.batch_max_height_var = tk.StringVar(value="1080")
        height_entry = tk.Entry(resize_settings_frame, textvariable=self.batch_max_height_var, width=8)
        height_entry.pack(side='left', padx=5)
        
        # Output directory
        output_frame = tk.LabelFrame(left_panel, text="📂 Output Directory", font=('Arial', 10, 'bold'))
        output_frame.pack(fill='x', pady=10)
        
        output_btn_frame = tk.Frame(output_frame)
        output_btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.select_batch_output_btn = tk.Button(output_btn_frame, text="📂 Select Output",
                                               command=self.select_batch_output_directory, bg='#27ae60', fg='white',
                                               font=('Arial', 9, 'bold'), padx=15, pady=5)
        self.select_batch_output_btn.pack(side='left')
        
        self.batch_output_label = tk.Label(output_btn_frame, text="Same as source",
                                         fg='#7f8c8d', font=('Arial', 9))
        self.batch_output_label.pack(side='left', padx=(10, 0))
        
        # Control buttons
        control_frame = tk.Frame(left_panel)
        control_frame.pack(fill='x', pady=20)
        
        # Scan button
        self.scan_btn = tk.Button(control_frame, text="🔍 SCAN FILES",
                                command=self.scan_batch_files, bg='#3498db', fg='white',
                                font=('Arial', 10, 'bold'), padx=20, pady=8)
        self.scan_btn.pack(fill='x', pady=5)
        
        # Start batch button
        self.start_batch_btn = tk.Button(control_frame, text="🚀 START BATCH CONVERSION",
                                       command=self.start_batch_conversion, bg='#e74c3c', fg='white',
                                       font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.start_batch_btn.pack(fill='x', pady=10)
        self.start_batch_btn.config(state='disabled')
        
        # Right panel - Live status and progress
        right_panel = tk.Frame(main_container)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # File list and status
        status_frame = tk.LabelFrame(right_panel, text="📋 Files Found", font=('Arial', 10, 'bold'))
        status_frame.pack(fill='both', expand=True, pady=10)
        
        # Files treeview
        columns = ('File', 'From', 'To', 'Size', 'Status')
        self.batch_files_tree = ttk.Treeview(status_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.batch_files_tree.heading(col, text=col)
            if col == 'File':
                self.batch_files_tree.column(col, width=200)
            elif col == 'Status':
                self.batch_files_tree.column(col, width=150)
            else:
                self.batch_files_tree.column(col, width=80)
        
        # Scrollbars for treeview
        tree_scroll_y = ttk.Scrollbar(status_frame, orient='vertical', command=self.batch_files_tree.yview)
        tree_scroll_x = ttk.Scrollbar(status_frame, orient='horizontal', command=self.batch_files_tree.xview)
        self.batch_files_tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        # Pack treeview and scrollbars
        self.batch_files_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        tree_scroll_y.pack(side='right', fill='y')
        
        # Progress frame
        progress_frame = tk.LabelFrame(right_panel, text="📊 Conversion Progress", font=('Arial', 10, 'bold'))
        progress_frame.pack(fill='x', pady=10)
        
        # Overall progress
        self.overall_progress_label = tk.Label(progress_frame, text="Ready to scan files",
                                             font=('Arial', 10, 'bold'), fg='#2c3e50')
        self.overall_progress_label.pack(pady=5)
        
        self.overall_progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.overall_progress_bar.pack(pady=5, padx=20)
        
        # Current file progress
        self.current_file_label = tk.Label(progress_frame, text="",
                                         font=('Arial', 9), fg='#7f8c8d')
        self.current_file_label.pack(pady=2)
        
        # Statistics
        stats_frame = tk.Frame(progress_frame)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.batch_stats_labels = {}
        stats_items = [('Files Found', 'found'), ('Converted', 'converted'), ('Failed', 'failed'), ('Skipped', 'skipped')]
        
        for i, (label, key) in enumerate(stats_items):
            frame = tk.Frame(stats_frame)
            frame.pack(side='left', expand=True, fill='x')
            
            tk.Label(frame, text=label + ":", font=('Arial', 8, 'bold')).pack()
            self.batch_stats_labels[key] = tk.Label(frame, text="0", font=('Arial', 12, 'bold'), fg='#3498db')
            self.batch_stats_labels[key].pack()
        
        # Initialize batch processing variables
        self.batch_files_list = []
        self.batch_stats = {'found': 0, 'converted': 0, 'failed': 0, 'skipped': 0}
        self.batch_output_directory = None
        self.batch_processing = False
        
    def create_settings_tab(self):
        """Create settings and about tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings content
        tk.Label(settings_frame, text="⚙️ FileForge Settings", 
                font=('Arial', 18, 'bold'), fg='#2c3e50').pack(pady=20)
        
        # General settings
        general_frame = tk.LabelFrame(settings_frame, text="General Settings", font=('Arial', 10, 'bold'))
        general_frame.pack(fill='x', padx=20, pady=10)
        
        # Theme selection
        theme_frame = tk.Frame(general_frame)
        theme_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(theme_frame, text="Theme:", font=('Arial', 10, 'bold')).pack(side='left')
        self.theme_var = tk.StringVar(value="Light")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                 values=['Light', 'Dark', 'Auto'], state='readonly')
        theme_combo.pack(side='left', padx=(10, 0))
        
        # Default quality
        quality_frame = tk.Frame(general_frame)
        quality_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(quality_frame, text="Default Quality:", font=('Arial', 10, 'bold')).pack(side='left')
        self.default_quality_var = tk.IntVar(value=90)
        quality_scale = tk.Scale(quality_frame, from_=10, to=100, orient='horizontal',
                               variable=self.default_quality_var, length=200)
        quality_scale.pack(side='left', padx=(10, 0))
        
        # About section
        about_frame = tk.LabelFrame(settings_frame, text="About SilentCanoe FileForge", font=('Arial', 10, 'bold'))
        about_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        about_text = """
🔧 SilentCanoe FileForge v1.0
Universal File Conversion Toolkit

✨ Features:
• Image conversion with quality control
• Batch processing capabilities  
• Text format conversion
• Professional GUI interface
• Command-line support

🌐 Links:
• GitHub: https://github.com/koushal13/SilentCanoe-FileForge
• SilentCanoe: https://silentcanoe.com
• Documentation: See repository README

📄 License: MIT License
💻 Created by SilentCanoe Team
        """
        
        about_label = tk.Label(about_frame, text=about_text, justify='left',
                             font=('Arial', 10), bg='white')
        about_label.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_status_bar(self):
        """Create status bar."""
        self.status_bar = tk.Label(
            self.root,
            text="Ready - Select files to start converting",
            relief=tk.SUNKEN,
            anchor='w',
            bg='#ecf0f1',
            font=('Arial', 9)
        )
        self.status_bar.pack(side='bottom', fill='x')
        
    # File selection methods
    def select_image_files(self):
        """Select image files for conversion."""
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.heic *.webp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            self.selected_files = list(files)
            self.update_image_files_display()
            self.status_bar.config(text=f"Selected {len(files)} image(s)")
            
    def clear_image_selection(self):
        """Clear selected image files."""
        self.selected_files = []
        self.update_image_files_display()
        self.status_bar.config(text="Image selection cleared")
        
    def update_image_files_display(self):
        """Update the display of selected image files."""
        self.image_files_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            file_name = Path(file_path).name
            self.image_files_listbox.insert(tk.END, file_name)
            
    def select_output_directory(self):
        """Select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory = directory
            self.output_label.config(text=f"Output: {Path(directory).name}")
            self.status_bar.config(text=f"Output directory: {directory}")
            
    # Conversion methods
    def convert_images(self):
        """Convert selected images."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select image files first.")
            return
            
        if not self.output_directory:
            messagebox.showwarning("No Output", "Please select an output directory.")
            return
            
        # Start conversion in separate thread
        self.status_bar.config(text="Converting images...")
        self.convert_images_btn.config(state='disabled', text="Converting...")
        
        thread = threading.Thread(target=self._convert_images_thread)
        thread.daemon = True
        thread.start()
        
    def _convert_images_thread(self):
        """Convert images in background thread."""
        try:
            converted_count = 0
            total_files = len(self.selected_files)
            output_format = self.image_format_var.get().lower()
            
            for i, file_path in enumerate(self.selected_files):
                # Update progress
                self.root.after(0, lambda i=i: self.status_bar.config(
                    text=f"Converting {i+1}/{total_files}: {Path(file_path).name}"))
                
                # Simulate conversion (replace with actual conversion code)
                success = self._convert_single_image(file_path, output_format)
                
                if success:
                    converted_count += 1
                    
            # Conversion complete
            self.root.after(0, self._conversion_complete, converted_count, total_files)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Conversion failed: {str(e)}"))
            self.root.after(0, self._reset_convert_button)
            
    def _convert_single_image(self, input_path, output_format):
        """Convert a single image using the professional converter with validation."""
        
        # Use professional converter if available
        if self.image_converter and PROFESSIONAL_CONVERTER_AVAILABLE:
            print(f"🔧 Using PROFESSIONAL converter with 6-checkpoint validation")
            
            # Get conversion settings from UI
            quality = self.quality_var.get()
            max_width = None
            max_height = None
            
            if self.resize_enabled.get():
                try:
                    max_width = int(self.width_var.get()) if self.width_var.get() else None
                    max_height = int(self.height_var.get()) if self.height_var.get() else None
                except ValueError:
                    print("⚠️ Invalid resize dimensions, using original size")
            
            # Perform professional conversion with full validation
            result = self.image_converter.convert_single_image(
                input_path=input_path,
                output_dir=self.output_directory,
                output_format=output_format,
                quality=quality,
                max_width=max_width,
                max_height=max_height
            )
            
            # Print detailed results in GUI context
            if result['success']:
                print(f"✅ PROFESSIONAL CONVERSION SUCCESSFUL:")
                print(f"   ✅ All {len(result['checkpoints_passed'])}/6 checkpoints passed")
                print(f"   📁 Input: {Path(input_path).name}")
                print(f"   📁 Output: {Path(result['output_file']).name}")
                
                if result['conversion_info']:
                    info = result['conversion_info']
                    print(f"   ⏱️ Time: {info.get('conversion_time_seconds', 0):.2f}s")
                    print(f"   📏 Size: {info.get('original_size')} → {info.get('final_size')}")
                    input_kb = info.get('file_size_before', 0) / 1024
                    output_kb = info.get('file_size_after', 0) / 1024
                    print(f"   💾 File: {input_kb:.1f}KB → {output_kb:.1f}KB")
                
                return True
            else:
                print(f"❌ PROFESSIONAL CONVERSION FAILED:")
                print(f"   Error: {result['error']}")
                print(f"   ❌ Failed checkpoints: {result['checkpoints_failed']}")
                print(f"   ✅ Passed checkpoints: {result['checkpoints_passed']}")
                return False
        
        # Fallback to basic conversion if professional converter not available
        else:
            print(f"⚠️ Using BASIC conversion (professional converter not available)")
            return self._basic_image_conversion(input_path, output_format)
    
    def _basic_image_conversion(self, input_path, output_format):
        """Basic image conversion fallback."""
        try:
            # Import image processing libraries
            try:
                from PIL import Image, ImageOps
                import pillow_heif
                # Register HEIF opener with Pillow
                pillow_heif.register_heif_opener()
            except ImportError as e:
                print(f"❌ Image conversion libraries not available: {e}")
                print("Please install: pip install Pillow pillow-heif")
                return False
            
            input_file = Path(input_path)
            output_extension = 'jpg' if output_format.lower() == 'jpeg' else output_format.lower()
            output_file = Path(self.output_directory) / f"{input_file.stem}.{output_extension}"
            
            print(f"🔄 Converting: {input_file.name} → {output_file.name}")
            
            # Validate input file
            if not input_file.exists():
                print(f"❌ Input file not found: {input_file}")
                return False
                
            # Open and process the image
            with Image.open(input_path) as img:
                print(f"📖 Opened: {img.format} {img.mode} {img.width}x{img.height}")
                
                # Handle EXIF orientation
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    img = ImageOps.exif_transpose(img)
                    print("🔄 Applied EXIF orientation correction")
                
                # Convert color mode for different formats
                if output_format.lower() in ('jpg', 'jpeg'):
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Convert to RGB with white background for JPEG
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                        print("🎨 Converted to RGB for JPEG")
                elif output_format.lower() == 'png':
                    if img.mode not in ('RGBA', 'RGB', 'L'):
                        img = img.convert('RGBA')
                        print("🎨 Converted to RGBA for PNG")
                
                # Apply resize if enabled
                if self.resize_enabled.get():
                    try:
                        new_width = int(self.width_var.get()) if self.width_var.get() else img.width
                        new_height = int(self.height_var.get()) if self.height_var.get() else img.height
                        
                        if new_width != img.width or new_height != img.height:
                            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            print(f"📏 Resized to {new_width}x{new_height}")
                    except ValueError:
                        print("⚠️ Invalid resize dimensions, keeping original size")
                
                # Prepare save parameters
                save_kwargs = {}
                quality = self.quality_var.get()
                
                if output_format.lower() in ('jpg', 'jpeg'):
                    save_kwargs = {
                        'format': 'JPEG',
                        'quality': quality,
                        'optimize': True
                    }
                elif output_format.lower() == 'png':
                    save_kwargs = {
                        'format': 'PNG',
                        'optimize': True
                    }
                elif output_format.lower() == 'webp':
                    save_kwargs = {
                        'format': 'WebP',
                        'quality': quality,
                        'optimize': True
                    }
                elif output_format.lower() == 'tiff':
                    save_kwargs = {
                        'format': 'TIFF',
                        'compression': 'lzw'
                    }
                else:
                    save_kwargs = {'format': output_format.upper()}
                
                print(f"💾 Saving as {save_kwargs.get('format', output_format)} with quality {quality}%")
                
                # Save the converted image
                img.save(output_file, **save_kwargs)
                
                # Verify the conversion worked
                if output_file.exists() and output_file.stat().st_size > 0:
                    # Quick validation: try to open the saved file
                    with Image.open(output_file) as test_img:
                        test_img.load()  # Force load to verify integrity
                        print(f"✅ Conversion successful: {test_img.format} {test_img.width}x{test_img.height}")
                        
                        # Calculate compression info
                        input_size = input_file.stat().st_size
                        output_size = output_file.stat().st_size
                        compression = ((input_size - output_size) / input_size * 100) if input_size > 0 else 0
                        print(f"📊 Size: {input_size/1024:.1f}KB → {output_size/1024:.1f}KB ({compression:+.1f}%)")
                        
                    return True
                else:
                    print(f"❌ Output file not created or empty")
                    return False
            
        except Exception as e:
            print(f"❌ Error converting {input_path}: {e}")
            return False
            
    def _conversion_complete(self, converted_count, total_files):
        """Handle conversion completion."""
        self.convert_images_btn.config(state='normal', text="🚀 CONVERT IMAGES")
        
        if converted_count == total_files:
            messagebox.showinfo("Success", 
                              f"Successfully converted {converted_count} images!")
            self.status_bar.config(text=f"Conversion complete: {converted_count} files converted")
        else:
            messagebox.showwarning("Partial Success", 
                                 f"Converted {converted_count} out of {total_files} images.")
            self.status_bar.config(text=f"Conversion complete: {converted_count}/{total_files} converted")
            
    def _reset_convert_button(self):
        """Reset convert button state."""
        self.convert_images_btn.config(state='normal', text="🚀 CONVERT IMAGES")
        
    # Text conversion methods
    def load_text_file(self):
        """Load a text file."""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[
                ("Text files", "*.txt *.md *.rtf"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_input.delete('1.0', tk.END)
                    self.text_input.insert('1.0', content)
                    self.status_bar.config(text=f"Loaded: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def convert_text(self):
        """Convert text to selected format."""
        content = self.text_input.get('1.0', tk.END).strip()
        
        if not content:
            messagebox.showwarning("No Content", "Please enter or load text content.")
            return
            
        output_format = self.text_format_var.get()
        
        # Simple format conversions
        try:
            if output_format == "HTML":
                converted = self._text_to_html(content)
            elif output_format == "JSON":
                converted = self._text_to_json(content)
            elif output_format == "XML":
                converted = self._text_to_xml(content)
            elif output_format == "CSV":
                converted = self._text_to_csv(content)
            elif output_format == "MD":
                converted = self._text_to_markdown(content)
            else:
                converted = content
                
            # Save converted content
            output_path = filedialog.asksaveasfilename(
                title=f"Save as {output_format}",
                defaultextension=f".{output_format.lower()}",
                filetypes=[(f"{output_format} files", f"*.{output_format.lower()}")]
            )
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(converted)
                messagebox.showinfo("Success", f"Text converted and saved as {output_format}!")
                self.status_bar.config(text=f"Converted to {output_format}: {Path(output_path).name}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
            
    def _text_to_html(self, text):
        """Convert text to HTML."""
        lines = text.split('\n')
        html = "<html>\n<head><title>Converted Text</title></head>\n<body>\n"
        for line in lines:
            if line.strip():
                html += f"<p>{line}</p>\n"
            else:
                html += "<br>\n"
        html += "</body>\n</html>"
        return html
        
    def _text_to_json(self, text):
        """Convert text to JSON."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        data = {
            "content": text,
            "lines": lines,
            "line_count": len(lines),
            "converted_at": datetime.now().isoformat()
        }
        return json.dumps(data, indent=2)
        
    def _text_to_xml(self, text):
        """Convert text to XML."""
        lines = text.split('\n')
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<document>\n'
        for i, line in enumerate(lines):
            if line.strip():
                xml += f'  <line id="{i+1}">{line}</line>\n'
        xml += '</document>'
        return xml
        
    def _text_to_csv(self, text):
        """Convert text to CSV."""
        lines = text.split('\n')
        csv_content = "Line,Content\n"
        for i, line in enumerate(lines):
            csv_content += f'{i+1},"{line}"\n'
        return csv_content
        
    def _text_to_markdown(self, text):
        """Convert text to Markdown."""
        lines = text.split('\n')
        md = "# Converted Text\n\n"
        for line in lines:
            if line.strip():
                md += f"{line}\n\n"
        return md
        
    # Advanced batch processing methods
    def select_batch_root_directory(self):
        """Select root directory for batch processing."""
        directory = filedialog.askdirectory(title="Select Root Directory for Batch Processing")
        if directory:
            self.batch_root_directory = directory
            self.batch_root_dir_label.config(text=f"Root: {Path(directory).name}")
            self.status_bar.config(text=f"Batch root directory: {directory}")
            # Reset file list when directory changes
            self.batch_files_list = []
            self.update_batch_stats()
            self.start_batch_btn.config(state='disabled')
    
    def select_batch_output_directory(self):
        """Select output directory for batch processing."""
        directory = filedialog.askdirectory(title="Select Output Directory (leave empty for same as source)")
        if directory:
            self.batch_output_directory = directory
            self.batch_output_label.config(text=f"Output: {Path(directory).name}")
        else:
            self.batch_output_directory = None
            self.batch_output_label.config(text="Same as source")
    
    def get_file_extensions_for_filter(self, filter_type):
        """Get file extensions based on filter selection."""
        filter_map = {
            "All Images": ['heic', 'heif', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif', 'webp', 'gif'],
            "HEIC/HEIF": ['heic', 'heif'],
            "PNG": ['png'],
            "JPEG": ['jpg', 'jpeg'],
            "BMP": ['bmp'],
            "TIFF": ['tiff', 'tif'],
            "WebP": ['webp'],
            "GIF": ['gif']
        }
        return filter_map.get(filter_type, [])
    
    def scan_batch_files(self):
        """Scan for files based on current filters."""
        if not hasattr(self, 'batch_root_directory'):
            messagebox.showwarning("No Directory", "Please select a root directory first.")
            return
        
        self.scan_btn.config(state='disabled', text="🔍 SCANNING...")
        self.batch_files_tree.delete(*self.batch_files_tree.get_children())
        
        # Start scanning in separate thread
        thread = threading.Thread(target=self._scan_files_thread)
        thread.daemon = True
        thread.start()
    
    def _scan_files_thread(self):
        """Scan files in background thread."""
        try:
            root_path = Path(self.batch_root_directory)
            from_filter = self.from_format_var.get()
            extensions = self.get_file_extensions_for_filter(from_filter)
            
            self.batch_files_list = []
            
            # Update status
            self.root.after(0, lambda: self.overall_progress_label.config(text="Scanning files..."))
            
            # Scan files
            if self.recursive_var.get():
                file_pattern = root_path.rglob("*")
            else:
                file_pattern = root_path.glob("*")
            
            files_found = []
            for file_path in file_pattern:
                if file_path.is_file():
                    ext = file_path.suffix.lower().lstrip('.')
                    if ext in extensions:
                        files_found.append(file_path)
            
            # Process found files
            total_files = len(files_found)
            
            for i, file_path in enumerate(files_found):
                try:
                    file_size = file_path.stat().st_size
                    size_str = self._format_file_size(file_size)
                    
                    from_format = file_path.suffix.upper().lstrip('.')
                    to_format = self.batch_to_format_var.get()
                    
                    file_info = {
                        'path': file_path,
                        'name': file_path.name,
                        'from_format': from_format,
                        'to_format': to_format,
                        'size': file_size,
                        'size_str': size_str,
                        'status': 'Ready'
                    }
                    
                    self.batch_files_list.append(file_info)
                    
                    # Update UI
                    self.root.after(0, self._add_file_to_tree, file_info)
                    
                    # Update progress
                    progress = (i + 1) / total_files * 100
                    self.root.after(0, lambda p=progress: self.overall_progress_bar.config(value=p))
                    self.root.after(0, lambda: self.current_file_label.config(text=f"Scanning: {file_path.name}"))
                    
                except Exception as e:
                    print(f"Error scanning {file_path}: {e}")
            
            # Update final stats
            self.batch_stats['found'] = len(self.batch_files_list)
            self.root.after(0, self._scan_complete)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", f"Failed to scan files: {str(e)}"))
            self.root.after(0, self._scan_complete)
    
    def _add_file_to_tree(self, file_info):
        """Add file to the treeview."""
        self.batch_files_tree.insert('', 'end', values=(
            file_info['name'],
            file_info['from_format'],
            file_info['to_format'],
            file_info['size_str'],
            file_info['status']
        ))
    
    def _scan_complete(self):
        """Handle scan completion."""
        self.scan_btn.config(state='normal', text="🔍 SCAN FILES")
        self.overall_progress_bar.config(value=0)
        self.current_file_label.config(text="")
        
        files_count = len(self.batch_files_list)
        self.overall_progress_label.config(text=f"Found {files_count} files ready for conversion")
        
        if files_count > 0:
            self.start_batch_btn.config(state='normal')
        else:
            self.start_batch_btn.config(state='disabled')
        
        self.update_batch_stats()
    
    def start_batch_conversion(self):
        """Start batch conversion process."""
        if not self.batch_files_list:
            messagebox.showwarning("No Files", "No files found for conversion.")
            return
        
        # Confirm if delete original is enabled
        if self.delete_original_var.get():
            result = messagebox.askyesno(
                "Confirm Delete",
                f"⚠️ WARNING: You have enabled 'Delete original files'.\n\n"
                f"This will PERMANENTLY DELETE {len(self.batch_files_list)} original files after conversion.\n\n"
                f"Are you sure you want to continue?",
                icon='warning'
            )
            if not result:
                return
        
        # Start conversion
        self.batch_processing = True
        self.start_batch_btn.config(state='disabled', text="🔄 CONVERTING...")
        self.scan_btn.config(state='disabled')
        
        # Reset stats
        self.batch_stats = {'found': len(self.batch_files_list), 'converted': 0, 'failed': 0, 'skipped': 0}
        self.update_batch_stats()
        
        # Start conversion thread
        thread = threading.Thread(target=self._batch_conversion_thread)
        thread.daemon = True
        thread.start()
    
    def _batch_conversion_thread(self):
        """Perform batch conversion in background thread."""
        total_files = len(self.batch_files_list)
        
        try:
            for i, file_info in enumerate(self.batch_files_list):
                if not self.batch_processing:  # Check if cancelled
                    break
                
                # Update current file
                self.root.after(0, lambda f=file_info: self.current_file_label.config(
                    text=f"Converting: {f['name']}"))
                
                # Update tree status
                self.root.after(0, self._update_tree_item_status, i, "Converting...")
                
                # Perform conversion
                success = self._convert_batch_file(file_info)
                
                if success:
                    self.batch_stats['converted'] += 1
                    self.root.after(0, self._update_tree_item_status, i, "✅ Converted")
                    
                    # Delete original if requested
                    if self.delete_original_var.get():
                        try:
                            file_info['path'].unlink()
                            self.root.after(0, self._update_tree_item_status, i, "✅ Converted (Original Deleted)")
                        except Exception as e:
                            print(f"Failed to delete {file_info['path']}: {e}")
                            self.root.after(0, self._update_tree_item_status, i, "✅ Converted (Delete Failed)")
                else:
                    self.batch_stats['failed'] += 1
                    self.root.after(0, self._update_tree_item_status, i, "❌ Failed")
                
                # Update progress
                progress = (i + 1) / total_files * 100
                self.root.after(0, lambda p=progress: self.overall_progress_bar.config(value=p))
                self.root.after(0, self.update_batch_stats)
                
                # Small delay to prevent UI freezing
                import time
                time.sleep(0.1)
            
            # Conversion complete
            self.root.after(0, self._batch_conversion_complete)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Conversion Error", f"Batch conversion failed: {str(e)}"))
            self.root.after(0, self._batch_conversion_complete)
    
    def _convert_batch_file(self, file_info):
        """Convert a single file in batch mode."""
        try:
            # Determine output directory
            if self.batch_output_directory:
                output_dir = self.batch_output_directory
            else:
                output_dir = file_info['path'].parent
            
            # Get conversion settings
            output_format = self.batch_to_format_var.get()
            quality = self.batch_quality_var.get()
            
            max_width = None
            max_height = None
            if self.batch_resize_var.get():
                try:
                    max_width = int(self.batch_max_width_var.get()) if self.batch_max_width_var.get() else None
                    max_height = int(self.batch_max_height_var.get()) if self.batch_max_height_var.get() else None
                except ValueError:
                    pass
            
            # Use professional converter if available
            if self.image_converter and PROFESSIONAL_CONVERTER_AVAILABLE:
                result = self.image_converter.convert_single_image(
                    input_path=str(file_info['path']),
                    output_dir=output_dir,
                    output_format=output_format,
                    quality=quality,
                    max_width=max_width,
                    max_height=max_height
                )
                return result['success']
            else:
                # Fallback to basic conversion
                return self._basic_batch_conversion(file_info, output_dir, output_format, quality, max_width, max_height)
                
        except Exception as e:
            print(f"Error converting {file_info['path']}: {e}")
            return False
    
    def _basic_batch_conversion(self, file_info, output_dir, output_format, quality, max_width, max_height):
        """Basic batch conversion fallback."""
        try:
            from PIL import Image, ImageOps
            import pillow_heif
            pillow_heif.register_heif_opener()
            
            input_path = file_info['path']
            output_ext = 'jpg' if output_format.lower() == 'jpeg' else output_format.lower()
            output_path = Path(output_dir) / f"{input_path.stem}.{output_ext}"
            
            with Image.open(input_path) as img:
                # Handle EXIF orientation
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    img = ImageOps.exif_transpose(img)
                
                # Convert color mode for JPEG
                if output_format.lower() in ('jpg', 'jpeg'):
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                
                # Resize if requested
                if max_width or max_height:
                    img = self._resize_image(img, max_width, max_height)
                
                # Save with appropriate settings
                save_kwargs = {}
                if output_format.lower() in ('jpg', 'jpeg'):
                    save_kwargs = {'format': 'JPEG', 'quality': quality, 'optimize': True}
                elif output_format.lower() == 'png':
                    save_kwargs = {'format': 'PNG', 'optimize': True}
                elif output_format.lower() == 'webp':
                    save_kwargs = {'format': 'WebP', 'quality': quality, 'optimize': True}
                else:
                    save_kwargs = {'format': output_format.upper()}
                
                img.save(output_path, **save_kwargs)
                
                # Verify output
                return output_path.exists() and output_path.stat().st_size > 0
                
        except Exception as e:
            print(f"Basic conversion failed for {file_info['path']}: {e}")
            return False
    
    def _resize_image(self, img, max_width, max_height):
        """Resize image while maintaining aspect ratio."""
        if not max_width and not max_height:
            return img
        
        width, height = img.size
        aspect_ratio = width / height
        
        if max_width and max_height:
            if width / max_width > height / max_height:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        elif max_width:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def _update_tree_item_status(self, index, status):
        """Update status of tree item."""
        children = self.batch_files_tree.get_children()
        if index < len(children):
            item_id = children[index]
            values = list(self.batch_files_tree.item(item_id)['values'])
            values[4] = status  # Status column
            self.batch_files_tree.item(item_id, values=values)
    
    def _batch_conversion_complete(self):
        """Handle batch conversion completion."""
        self.batch_processing = False
        self.start_batch_btn.config(state='normal', text="🚀 START BATCH CONVERSION")
        self.scan_btn.config(state='normal')
        self.overall_progress_bar.config(value=100)
        self.current_file_label.config(text="")
        
        converted = self.batch_stats['converted']
        failed = self.batch_stats['failed']
        total = self.batch_stats['found']
        
        self.overall_progress_label.config(
            text=f"Batch conversion complete: {converted} successful, {failed} failed ({total} total)")
        
        # Show completion message
        if failed == 0:
            messagebox.showinfo("Batch Complete", 
                              f"🎉 Successfully converted all {converted} files!")
        else:
            messagebox.showwarning("Batch Complete", 
                                 f"Conversion finished:\n✅ Successful: {converted}\n❌ Failed: {failed}")
    
    def update_batch_stats(self):
        """Update batch statistics display."""
        for key, label in self.batch_stats_labels.items():
            label.config(text=str(self.batch_stats.get(key, 0)))
        
    def _format_file_size(self, size_bytes):
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
        
    def run(self):
        """Run the application."""
        self.root.mainloop()

def main():
    """Main function."""
    print("🔧 Starting SilentCanoe FileForge - Complete Converter...")
    print("✨ Features:")
    print("   • Image conversion with quality control")
    print("   • Text format conversion")
    print("   • Batch processing capabilities")
    print("   • Professional GUI with multiple tabs")
    print("🚀 Ready for file conversion!")
    print()
    
    try:
        app = FileForgeConverter()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()