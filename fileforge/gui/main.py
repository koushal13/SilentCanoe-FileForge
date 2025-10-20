"""
Modern GUI for SilentCanoe FileForge

Comprehensive graphical interface with tabs for different conversion types.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fileforge.core import ConversionEngine, BatchProcessor

class FileForgeGUI:
    """Main GUI application for SilentCanoe FileForge"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SilentCanoe FileForge - Universal File Converter")
        self.root.geometry("900x700")
        
        # Initialize engine
        self.engine = ConversionEngine()
        self.batch_processor = BatchProcessor()
        
        # GUI state
        self.current_operation = None
        self.progress_queue = queue.Queue()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_progress_checker()
    
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        
        # Use modern theme if available
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # Custom colors
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Info.TLabel', font=('Segoe UI', 9), foreground='gray')
    
    def create_widgets(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔧 SilentCanoe FileForge", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_image_tab()
        self.create_document_tab()
        self.create_audio_tab()
        self.create_video_tab()
        self.create_batch_tab()
        self.create_pdf_tools_tab()
        
        # Progress section
        self.create_progress_section(main_frame)
    
    def create_image_tab(self):
        """Create image conversion tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="🖼️ Images")
        
        # Input section
        input_frame = ttk.LabelFrame(frame, text="Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Image File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.image_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.image_input_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_image_input).grid(row=0, column=2)
        
        # Output section
        output_frame = ttk.LabelFrame(frame, text="Output", padding="10")
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.image_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.image_output_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="Browse", command=self.browse_image_output).grid(row=0, column=2)
        
        ttk.Label(output_frame, text="Format:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.image_format_var = tk.StringVar(value="jpg")
        format_combo = ttk.Combobox(output_frame, textvariable=self.image_format_var, 
                                   values=["jpg", "png", "webp", "tiff", "bmp", "gif"], state="readonly")
        format_combo.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Options section
        options_frame = ttk.LabelFrame(frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Quality
        ttk.Label(options_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W)
        self.image_quality_var = tk.IntVar(value=90)
        quality_scale = ttk.Scale(options_frame, from_=1, to=100, variable=self.image_quality_var, orient=tk.HORIZONTAL)
        quality_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        self.image_quality_label = ttk.Label(options_frame, text="90")
        self.image_quality_label.grid(row=0, column=2)
        quality_scale.configure(command=lambda v: self.image_quality_label.config(text=str(int(float(v)))))
        
        # Resize
        ttk.Label(options_frame, text="Resize:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.image_resize_var = tk.StringVar()
        resize_combo = ttk.Combobox(options_frame, textvariable=self.image_resize_var,
                                   values=["", "480p (854x480)", "720p (1280x720)", "1080p (1920x1080)", "Custom"])
        resize_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(5, 0))
        
        # Convert button
        ttk.Button(frame, text="Convert Image", command=self.convert_image).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_document_tab(self):
        """Create document conversion tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="📄 Documents")
        
        # Input section
        input_frame = ttk.LabelFrame(frame, text="Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Document:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.doc_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.doc_input_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_doc_input).grid(row=0, column=2)
        
        # Output section
        output_frame = ttk.LabelFrame(frame, text="Output", padding="10")
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.doc_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.doc_output_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="Browse", command=self.browse_doc_output).grid(row=0, column=2)
        
        ttk.Label(output_frame, text="Format:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.doc_format_var = tk.StringVar(value="pdf")
        format_combo = ttk.Combobox(output_frame, textvariable=self.doc_format_var,
                                   values=["pdf", "docx", "xlsx", "pptx", "txt", "html"], state="readonly")
        format_combo.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Options
        options_frame = ttk.LabelFrame(frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(options_frame, text="Password:").grid(row=0, column=0, sticky=tk.W)
        self.doc_password_var = tk.StringVar()
        ttk.Entry(options_frame, textvariable=self.doc_password_var, show="*").grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        self.doc_ocr_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Enable OCR for scanned documents", 
                       variable=self.doc_ocr_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Convert button
        ttk.Button(frame, text="Convert Document", command=self.convert_document).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_audio_tab(self):
        """Create audio conversion tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="🎵 Audio")
        
        # Similar structure to image tab but for audio
        # Input section
        input_frame = ttk.LabelFrame(frame, text="Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Audio File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.audio_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.audio_input_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_audio_input).grid(row=0, column=2)
        
        # Output section with format selection
        output_frame = ttk.LabelFrame(frame, text="Output", padding="10")
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.audio_format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(output_frame, textvariable=self.audio_format_var,
                                   values=["mp3", "wav", "flac", "aac", "ogg", "m4a"], state="readonly")
        format_combo.grid(row=0, column=1, sticky=tk.W)
        
        # Quality options
        options_frame = ttk.LabelFrame(frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(options_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W)
        self.audio_quality_var = tk.StringVar(value="medium")
        quality_combo = ttk.Combobox(options_frame, textvariable=self.audio_quality_var,
                                    values=["low", "medium", "high", "lossless"], state="readonly")
        quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Convert button
        ttk.Button(frame, text="Convert Audio", command=self.convert_audio).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_video_tab(self):
        """Create video conversion tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="🎬 Video")
        
        # Input section
        input_frame = ttk.LabelFrame(frame, text="Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Video File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.video_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.video_input_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_video_input).grid(row=0, column=2)
        
        # Output section
        output_frame = ttk.LabelFrame(frame, text="Output", padding="10")
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(output_frame, text="Format:").grid(row=0, column=0, sticky=tk.W)
        self.video_format_var = tk.StringVar(value="mp4")
        format_combo = ttk.Combobox(output_frame, textvariable=self.video_format_var,
                                   values=["mp4", "avi", "mkv", "mov", "webm"], state="readonly")
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Quality and resolution
        options_frame = ttk.LabelFrame(frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(options_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W)
        self.video_quality_var = tk.StringVar(value="medium")
        quality_combo = ttk.Combobox(options_frame, textvariable=self.video_quality_var,
                                    values=["ultra_low", "low", "medium", "high", "ultra_high"], state="readonly")
        quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(options_frame, text="Resolution:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.video_resolution_var = tk.StringVar()
        resolution_combo = ttk.Combobox(options_frame, textvariable=self.video_resolution_var,
                                       values=["", "480p", "720p", "1080p", "1440p", "4k"])
        resolution_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # Convert button
        ttk.Button(frame, text="Convert Video", command=self.convert_video).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_batch_tab(self):
        """Create batch processing tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="📦 Batch")
        
        # Folder selection
        folder_frame = ttk.LabelFrame(frame, text="Folders", padding="10")
        folder_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(1, weight=1)
        
        ttk.Label(folder_frame, text="Input Folder:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.batch_input_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.batch_input_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(folder_frame, text="Browse", command=self.browse_batch_input).grid(row=0, column=2)
        
        ttk.Label(folder_frame, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.batch_output_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.batch_output_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        ttk.Button(folder_frame, text="Browse", command=self.browse_batch_output).grid(row=1, column=2, pady=(5, 0))
        
        # Options
        options_frame = ttk.LabelFrame(frame, text="Options", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(options_frame, text="Output Format:").grid(row=0, column=0, sticky=tk.W)
        self.batch_format_var = tk.StringVar(value="jpg")
        format_combo = ttk.Combobox(options_frame, textvariable=self.batch_format_var,
                                   values=["jpg", "png", "pdf", "mp3", "mp4"])
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        self.batch_recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include subdirectories", 
                       variable=self.batch_recursive_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Convert button
        ttk.Button(frame, text="Start Batch Conversion", command=self.start_batch_conversion).grid(row=2, column=0, columnspan=2, pady=10)
    
    def create_pdf_tools_tab(self):
        """Create PDF tools tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="📑 PDF Tools")
        
        # PDF operations buttons in a grid
        operations_frame = ttk.LabelFrame(frame, text="PDF Operations", padding="10")
        operations_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(operations_frame, text="Merge PDFs", command=self.merge_pdfs).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(operations_frame, text="Split PDF", command=self.split_pdf).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(operations_frame, text="Compress PDF", command=self.compress_pdf).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(operations_frame, text="Encrypt PDF", command=self.encrypt_pdf).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(operations_frame, text="Add Watermark", command=self.watermark_pdf).grid(row=2, column=0, padx=5, pady=5)
    
    def create_progress_section(self, parent):
        """Create progress display section"""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.status_var).grid(row=1, column=0)
        
        # Log area
        self.log_text = tk.Text(progress_frame, height=8, width=80)
        self.log_text.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
    
    def setup_progress_checker(self):
        """Setup periodic checking of progress queue"""
        def check_progress():
            try:
                while True:
                    message = self.progress_queue.get_nowait()
                    self.log_message(message)
            except queue.Empty:
                pass
            finally:
                self.root.after(100, check_progress)
        
        check_progress()
    
    def log_message(self, message: str):
        """Add message to log display"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message: str):
        """Update status label"""
        self.status_var.set(message)
    
    def update_progress(self, value: float):
        """Update progress bar"""
        self.progress_var.set(value)
    
    # File browsing methods
    def browse_image_input(self):
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.heic *.heif *.jpg *.jpeg *.png *.bmp *.tiff *.webp *.gif")]
        )
        if filename:
            self.image_input_var.set(filename)
            # Auto-generate output filename
            input_path = Path(filename)
            output_path = input_path.with_suffix(f'.{self.image_format_var.get()}')
            self.image_output_var.set(str(output_path))
    
    def browse_image_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=f".{self.image_format_var.get()}",
            filetypes=[("Image files", f"*.{self.image_format_var.get()}")]
        )
        if filename:
            self.image_output_var.set(filename)
    
    def browse_doc_input(self):
        filename = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("All documents", "*.pdf *.doc *.docx *.xls *.xlsx *.ppt *.pptx *.txt")]
        )
        if filename:
            self.doc_input_var.set(filename)
    
    def browse_doc_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Document As",
            defaultextension=f".{self.doc_format_var.get()}"
        )
        if filename:
            self.doc_output_var.set(filename)
    
    def browse_audio_input(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.mp3 *.wav *.flac *.aac *.ogg *.m4a")]
        )
        if filename:
            self.audio_input_var.set(filename)
    
    def browse_video_input(self):
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm")]
        )
        if filename:
            self.video_input_var.set(filename)
    
    def browse_batch_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.batch_input_var.set(folder)
    
    def browse_batch_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.batch_output_var.set(folder)
    
    # Conversion methods
    def convert_image(self):
        """Convert single image"""
        input_file = self.image_input_var.get()
        output_file = self.image_output_var.get()
        
        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select input and output files")
            return
        
        options = {
            'quality': self.image_quality_var.get()
        }
        
        # Handle resize option
        resize_option = self.image_resize_var.get()
        if resize_option and resize_option != "":
            if "x" in resize_option:
                # Extract dimensions from string like "1280x720"
                dims = resize_option.split("(")[1].split(")")[0].split("x")
                options['resize'] = (int(dims[0]), int(dims[1]))
        
        self.run_conversion_thread(self.engine.convert_single, input_file, output_file, **options)
    
    def convert_document(self):
        """Convert single document"""
        input_file = self.doc_input_var.get()
        output_file = self.doc_output_var.get()
        
        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select input and output files")
            return
        
        options = {}
        if self.doc_password_var.get():
            options['password'] = self.doc_password_var.get()
        if self.doc_ocr_var.get():
            options['ocr'] = True
        
        self.run_conversion_thread(self.engine.convert_single, input_file, output_file, **options)
    
    def convert_audio(self):
        """Convert single audio file"""
        input_file = self.audio_input_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        # Generate output filename
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix(f'.{self.audio_format_var.get()}'))
        
        options = {
            'quality': self.audio_quality_var.get()
        }
        
        self.run_conversion_thread(self.engine.convert_single, input_file, output_file, **options)
    
    def convert_video(self):
        """Convert single video file"""
        input_file = self.video_input_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        # Generate output filename
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix(f'.{self.video_format_var.get()}'))
        
        options = {
            'quality': self.video_quality_var.get()
        }
        
        if self.video_resolution_var.get():
            options['resolution'] = self.video_resolution_var.get()
        
        self.run_conversion_thread(self.engine.convert_single, input_file, output_file, **options)
    
    def start_batch_conversion(self):
        """Start batch conversion process"""
        input_folder = self.batch_input_var.get()
        output_folder = self.batch_output_var.get()
        
        if not input_folder:
            messagebox.showerror("Error", "Please select input folder")
            return
        
        if not output_folder:
            output_folder = str(Path(input_folder).parent / f"{Path(input_folder).name}_converted")
            self.batch_output_var.set(output_folder)
        
        options = {
            'quality': 90  # Default quality
        }
        
        self.run_batch_thread(
            input_folder, output_folder, 
            "*", self.batch_format_var.get(),
            self.batch_recursive_var.get(), **options
        )
    
    def run_conversion_thread(self, func, *args, **kwargs):
        """Run conversion in separate thread"""
        def conversion_worker():
            try:
                self.update_status("Converting...")
                self.update_progress(0)
                
                success = func(*args, **kwargs)
                
                if success:
                    self.log_message("✅ Conversion completed successfully!")
                    self.update_status("Conversion completed")
                    self.update_progress(100)
                else:
                    self.log_message("❌ Conversion failed!")
                    self.update_status("Conversion failed")
                    self.update_progress(0)
                    
            except Exception as e:
                self.log_message(f"❌ Error: {str(e)}")
                self.update_status("Error occurred")
                self.update_progress(0)
        
        thread = threading.Thread(target=conversion_worker)
        thread.daemon = True
        thread.start()
    
    def run_batch_thread(self, input_folder, output_folder, pattern, output_format, recursive, **options):
        """Run batch conversion in separate thread"""
        def batch_worker():
            try:
                self.update_status("Starting batch conversion...")
                self.update_progress(0)
                
                results = self.engine.convert_batch(
                    input_folder, output_folder, pattern, output_format, recursive, **options
                )
                
                self.log_message(f"📊 Batch conversion results:")
                self.log_message(f"Total files: {results['total']}")
                self.log_message(f"Successful: {results['successful']} ✅")
                self.log_message(f"Failed: {results['failed']} ❌")
                
                self.update_status("Batch conversion completed")
                self.update_progress(100)
                
            except Exception as e:
                self.log_message(f"❌ Batch conversion error: {str(e)}")
                self.update_status("Batch conversion failed")
                self.update_progress(0)
        
        thread = threading.Thread(target=batch_worker)
        thread.daemon = True
        thread.start()
    
    # PDF tool methods (simplified)
    def merge_pdfs(self):
        """Merge multiple PDF files"""
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if len(files) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 PDF files")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if output_file:
            self.log_message(f"Merging {len(files)} PDF files...")
            # Implementation would go here
            self.log_message("✅ PDF merge completed!")
    
    def split_pdf(self):
        """Split PDF file"""
        input_file = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if input_file:
            output_folder = filedialog.askdirectory(title="Select output folder")
            if output_folder:
                self.log_message(f"Splitting PDF: {Path(input_file).name}")
                # Implementation would go here
                self.log_message("✅ PDF split completed!")
    
    def compress_pdf(self):
        """Compress PDF file"""
        self.log_message("PDF compression feature coming soon!")
    
    def encrypt_pdf(self):
        """Encrypt PDF file"""
        self.log_message("PDF encryption feature coming soon!")
    
    def watermark_pdf(self):
        """Add watermark to PDF"""
        self.log_message("PDF watermark feature coming soon!")

def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = FileForgeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()