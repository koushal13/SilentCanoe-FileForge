#!/usr/bin/env python3
"""
SilentCanoe FileForge - Demo Version
Simple working demo of the file conversion toolkit
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import shutil

class FileForgeDemo:
    """Demo version of SilentCanoe FileForge with basic functionality."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔧 SilentCanoe FileForge - Demo")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        
        # Supported formats (demo version)
        self.supported_formats = {
            'image': ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff'],
            'text': ['txt', 'md', 'rtf', 'csv'],
            'other': ['pdf', 'docx', 'mp3', 'mp4']
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🔧 SilentCanoe FileForge", 
            font=('Arial', 20, 'bold'),
            fg='white', 
            bg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Universal File Conversion Toolkit - Demo Version",
            font=('Arial', 10),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # File Info Tab
        self.create_info_tab()
        
        # File Browser Tab
        self.create_browser_tab()
        
        # About Tab
        self.create_about_tab()
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, 
            text="Ready - Select a file to get started",
            relief=tk.SUNKEN,
            anchor='w',
            bg='#ecf0f1',
            font=('Arial', 9)
        )
        self.status_bar.pack(side='bottom', fill='x')
        
    def create_info_tab(self):
        """Create file information tab."""
        info_frame = ttk.Frame(self.notebook)
        self.notebook.add(info_frame, text="📋 File Info")
        
        # File selection
        select_frame = tk.Frame(info_frame, bg='white')
        select_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            select_frame, 
            text="Select a file to analyze:",
            font=('Arial', 12, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        button_frame = tk.Frame(select_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        self.select_button = tk.Button(
            button_frame,
            text="📁 Browse Files",
            command=self.select_file,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.select_button.pack(side='left')
        
        self.selected_file_label = tk.Label(
            button_frame,
            text="No file selected",
            bg='white',
            fg='#7f8c8d',
            font=('Arial', 10)
        )
        self.selected_file_label.pack(side='left', padx=(20, 0))
        
        # File info display
        self.info_text = tk.Text(
            info_frame,
            height=20,
            width=80,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#f8f9fa',
            border=1,
            relief='solid'
        )
        self.info_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.info_text)
        scrollbar.pack(side='right', fill='y')
        self.info_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.info_text.yview)
        
    def create_browser_tab(self):
        """Create file browser tab."""
        browser_frame = ttk.Frame(self.notebook)
        self.notebook.add(browser_frame, text="📁 File Browser")
        
        # Directory selection
        dir_frame = tk.Frame(browser_frame, bg='white')
        dir_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            dir_frame,
            text="Browse directory contents:",
            font=('Arial', 12, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        dir_button_frame = tk.Frame(dir_frame, bg='white')
        dir_button_frame.pack(fill='x', pady=(10, 0))
        
        self.dir_button = tk.Button(
            dir_button_frame,
            text="📂 Select Directory",
            command=self.select_directory,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.dir_button.pack(side='left')
        
        self.current_dir_label = tk.Label(
            dir_button_frame,
            text="No directory selected",
            bg='white',
            fg='#7f8c8d',
            font=('Arial', 10)
        )
        self.current_dir_label.pack(side='left', padx=(20, 0))
        
        # File list
        list_frame = tk.Frame(browser_frame, bg='white')
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Treeview for file listing
        columns = ('Name', 'Type', 'Size', 'Modified')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        
        # Configure columns
        self.file_tree.heading('#0', text='📁', anchor='w')
        self.file_tree.column('#0', width=50)
        
        for col in columns:
            self.file_tree.heading(col, text=col, anchor='w')
            self.file_tree.column(col, width=150)
        
        # Scrollbars for treeview
        tree_scroll_y = ttk.Scrollbar(list_frame, orient='vertical', command=self.file_tree.yview)
        tree_scroll_x = ttk.Scrollbar(list_frame, orient='horizontal', command=self.file_tree.xview)
        self.file_tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        # Pack treeview and scrollbars
        self.file_tree.pack(side='left', fill='both', expand=True)
        tree_scroll_y.pack(side='right', fill='y')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        # Bind double-click event
        self.file_tree.bind('<Double-1>', self.on_file_double_click)
        
    def create_about_tab(self):
        """Create about tab."""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="ℹ️ About")
        
        # About content
        about_content = """
🔧 SilentCanoe FileForge - Demo Version

Universal File Conversion and Manipulation Toolkit

🌟 Features (Demo):
• File information analysis
• Directory browsing
• Format detection
• User-friendly interface

🚀 Full Version Features:
• Universal image converter (HEIC, JPG, PNG, WebP, TIFF, BMP, GIF, ICO, etc.)
• PDF manipulation suite (merge, split, compress, encrypt, OCR)
• Audio/Video conversion with FFmpeg integration  
• Batch processing with parallel execution
• Command-line interface for automation
• Professional documentation and examples

💻 Technical Details:
• Built with Python and Tkinter
• Modular architecture for extensibility
• Cross-platform support (Windows, macOS, Linux)
• Open source with MIT License

🌐 Links:
• GitHub: https://github.com/koushal13/SilentCanoe-FileForge
• Website: https://silentcanoe.com
• Documentation: Comprehensive guides and examples

👨‍💻 Created by SilentCanoe
Making file conversion effortless and powerful!

📄 License: MIT License
Version: 1.0.0 Demo
"""
        
        about_text = tk.Text(
            about_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='white',
            border=0,
            padx=20,
            pady=20
        )
        about_text.pack(fill='both', expand=True)
        about_text.insert('1.0', about_content)
        about_text.config(state='disabled')  # Make read-only
        
    def select_file(self):
        """Select a file for analysis."""
        file_path = filedialog.askopenfilename(
            title="Select file to analyze",
            filetypes=[
                ("All files", "*.*"),
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.heic"),
                ("Document files", "*.pdf *.docx *.txt *.md"),
                ("Audio files", "*.mp3 *.wav *.flac *.aac"),
                ("Video files", "*.mp4 *.avi *.mkv *.mov")
            ]
        )
        
        if file_path:
            self.analyze_file(file_path)
            
    def analyze_file(self, file_path):
        """Analyze the selected file."""
        try:
            path = Path(file_path)
            
            # Update UI
            self.selected_file_label.config(text=path.name)
            self.status_bar.config(text=f"Analyzing: {path.name}")
            
            # Get file information
            file_info = self.get_file_info(path)
            
            # Display information
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert('1.0', file_info)
            
            self.status_bar.config(text=f"Analysis complete: {path.name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze file: {str(e)}")
            self.status_bar.config(text="Error occurred during analysis")
            
    def get_file_info(self, path: Path) -> str:
        """Get detailed file information."""
        try:
            stat = path.stat()
            
            # File type detection
            ext = path.suffix.lower().lstrip('.')
            file_type = self.detect_file_type(ext)
            
            # Format file size
            size_bytes = stat.st_size
            size_formatted = self.format_file_size(size_bytes)
            
            # Format timestamps
            import time
            created = time.ctime(stat.st_ctime)
            modified = time.ctime(stat.st_mtime)
            
            info = f"""📋 FILE ANALYSIS REPORT
═══════════════════════════════════════════════════

📁 Basic Information:
├─ Name: {path.name}
├─ Full Path: {path}
├─ Extension: .{ext}
├─ Type: {file_type.title()}
└─ Size: {size_formatted} ({size_bytes:,} bytes)

📅 Timestamps:
├─ Created: {created}
└─ Modified: {modified}

🔍 Format Details:
├─ Detected Category: {file_type}
├─ Extension: {ext.upper() if ext else 'None'}
└─ Supported: {'✅ Yes' if self.is_supported_format(ext) else '❌ No'}

📊 Technical Information:
├─ Readable: {'✅ Yes' if os.access(path, os.R_OK) else '❌ No'}
├─ Writable: {'✅ Yes' if os.access(path, os.W_OK) else '❌ No'}
└─ Executable: {'✅ Yes' if os.access(path, os.X_OK) else '❌ No'}

🛠️ Conversion Options:
"""
            
            # Add conversion suggestions
            if file_type == 'image':
                info += """├─ Available conversions: JPG, PNG, WebP, BMP, TIFF
├─ Recommended: JPG (for photos), PNG (for graphics)
└─ Features: Resize, enhance, watermark, batch processing
"""
            elif file_type == 'document':
                info += """├─ Available conversions: PDF, DOCX, TXT, HTML
├─ Recommended: PDF (for sharing), DOCX (for editing)
└─ Features: Merge, split, compress, encrypt
"""
            elif file_type == 'audio':
                info += """├─ Available conversions: MP3, WAV, FLAC, AAC
├─ Recommended: MP3 (for compatibility), FLAC (for quality)
└─ Features: Quality control, normalization, effects
"""
            elif file_type == 'video':
                info += """├─ Available conversions: MP4, AVI, MKV, WebM
├─ Recommended: MP4 (for compatibility)
└─ Features: Resolution scaling, compression, GIF creation
"""
            else:
                info += """├─ No specific conversions available in demo
├─ Full version supports many more formats
└─ Check documentation for complete format list
"""
                
            info += f"""
🎯 Demo Limitations:
├─ This is a demonstration version
├─ Actual conversion requires full implementation
├─ Real converters use specialized libraries
└─ See GitHub repository for complete solution

🔗 More Information:
├─ GitHub: https://github.com/koushal13/SilentCanoe-FileForge
├─ Documentation: Full API reference and examples
└─ SilentCanoe: https://silentcanoe.com

═══════════════════════════════════════════════════
Report generated by SilentCanoe FileForge Demo v1.0
"""
            
            return info
            
        except Exception as e:
            return f"Error analyzing file: {str(e)}"
            
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
        
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
        
    def select_directory(self):
        """Select a directory to browse."""
        dir_path = filedialog.askdirectory(title="Select directory to browse")
        
        if dir_path:
            self.browse_directory(dir_path)
            
    def browse_directory(self, dir_path):
        """Browse the selected directory."""
        try:
            path = Path(dir_path)
            self.current_dir_label.config(text=str(path))
            self.status_bar.config(text=f"Browsing: {path}")
            
            # Clear existing items
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
                
            # Add files and directories
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                
                for item in items:
                    if item.is_file():
                        icon = "📄"
                        item_type = self.detect_file_type(item.suffix.lower().lstrip('.'))
                        size = self.format_file_size(item.stat().st_size)
                    else:
                        icon = "📁"
                        item_type = "Directory"
                        size = "-"
                    
                    import time
                    modified = time.strftime("%Y-%m-%d %H:%M", time.localtime(item.stat().st_mtime))
                    
                    self.file_tree.insert('', 'end', text=icon, values=(
                        item.name,
                        item_type.title(),
                        size,
                        modified
                    ))
                    
                self.status_bar.config(text=f"Found {len(items)} items in {path.name}")
                
            except PermissionError:
                messagebox.showerror("Permission Error", "Cannot access this directory")
                self.status_bar.config(text="Permission denied")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to browse directory: {str(e)}")
            self.status_bar.config(text="Error browsing directory")
            
    def on_file_double_click(self, event):
        """Handle double-click on file in browser."""
        selection = self.file_tree.selection()
        if selection:
            item = self.file_tree.item(selection[0])
            file_name = item['values'][0]
            
            # Get current directory
            current_dir = self.current_dir_label.cget('text')
            if current_dir != "No directory selected":
                file_path = Path(current_dir) / file_name
                if file_path.is_file():
                    # Switch to info tab and analyze file
                    self.notebook.select(0)  # Select first tab (File Info)
                    self.analyze_file(str(file_path))
                    
    def run(self):
        """Run the application."""
        self.root.mainloop()

def main():
    """Main function to run the demo."""
    print("🔧 Starting SilentCanoe FileForge Demo...")
    print("📋 Demo Features:")
    print("   • File information analysis")
    print("   • Directory browsing")
    print("   • Format detection")
    print("   • User-friendly GUI")
    print()
    print("🚀 Full version features comprehensive conversion capabilities!")
    print("🌐 GitHub: https://github.com/koushal13/SilentCanoe-FileForge")
    print()
    
    try:
        app = FileForgeDemo()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Make sure you have Python with Tkinter support")

if __name__ == "__main__":
    main()