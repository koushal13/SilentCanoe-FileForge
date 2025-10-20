#!/usr/bin/env python3
"""
SilentCanoe FileForge - Launcher Script
Easy launcher for all FileForge utilities
"""

import os
import sys
import subprocess
from pathlib import Path

def show_banner():
    """Show FileForge banner."""
    print("🔧" + "=" * 60 + "🔧")
    print("  ✨ SilentCanoe FileForge - Universal File Toolkit ✨")
    print("🔧" + "=" * 60 + "🔧")
    print()

def show_menu():
    """Show main menu."""
    print("📋 Available Utilities:")
    print()
    print("1. 🚀 Complete Converter - Full conversion utility with GUI")
    print("   • Image conversion with quality control") 
    print("   • Text format conversion")
    print("   • Batch processing")
    print("   • Multiple tabs and settings")
    print()
    print("2. 📋 File Analyzer - Simple analysis and info demo")
    print("   • File information analysis")
    print("   • Directory browsing")
    print("   • Format detection")
    print()
    print("3. 💻 CLI Tools - Command-line interface")
    print("   • Analyze files: fileforge_cli.py analyze <file>")
    print("   • List directories: fileforge_cli.py list <dir>")
    print("   • JSON output support")
    print()
    print("4. ℹ️  Show CLI Help - Display all CLI commands")
    print()
    print("5. 🌐 Open GitHub Repository")
    print()
    print("0. ❌ Exit")
    print()

def launch_complete_converter():
    """Launch the complete converter."""
    print("🚀 Launching Complete FileForge Converter...")
    print("   This utility has working conversion buttons!")
    try:
        subprocess.run([sys.executable, "fileforge_converter.py"])
    except FileNotFoundError:
        print("❌ fileforge_converter.py not found!")
    except Exception as e:
        print(f"❌ Error launching converter: {e}")

def launch_analyzer_demo():
    """Launch the analyzer demo."""
    print("📋 Launching File Analyzer Demo...")
    try:
        subprocess.run([sys.executable, "demo.py"])
    except FileNotFoundError:
        print("❌ demo.py not found!")
    except Exception as e:
        print(f"❌ Error launching demo: {e}")

def show_cli_help():
    """Show CLI help."""
    print("💻 CLI Commands Help:")
    print("-" * 40)
    try:
        subprocess.run([sys.executable, "fileforge_cli.py", "--help"])
    except FileNotFoundError:
        print("❌ fileforge_cli.py not found!")
    except Exception as e:
        print(f"❌ Error showing CLI help: {e}")

def open_github():
    """Open GitHub repository."""
    import webbrowser
    url = "https://github.com/koushal13/SilentCanoe-FileForge"
    print(f"🌐 Opening GitHub repository: {url}")
    webbrowser.open(url)

def main():
    """Main launcher function."""
    show_banner()
    
    while True:
        show_menu()
        
        try:
            choice = input("👉 Select an option (0-5): ").strip()
            print()
            
            if choice == "1":
                launch_complete_converter()
            elif choice == "2":
                launch_analyzer_demo()
            elif choice == "3":
                print("💻 CLI Tools Available:")
                print("python fileforge_cli.py analyze <file>")
                print("python fileforge_cli.py list <directory>")
                print("python fileforge_cli.py info")
                print("python fileforge_cli.py --help")
                print()
            elif choice == "4":
                show_cli_help()
            elif choice == "5":
                open_github()
            elif choice == "0":
                print("👋 Thanks for using SilentCanoe FileForge!")
                break
            else:
                print("❌ Invalid choice. Please select 0-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using SilentCanoe FileForge!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()