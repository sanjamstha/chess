"""
Chessly - Executable Builder
---------------------------
Standalone build script for packaging the Chessly desktop application.
Target OS: Windows, Mac, Linux
"""

import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path

def build_add_data_arg(source, destination):
    """Use the correct PyInstaller data separator for the current OS."""
    separator = ';' if os.name == 'nt' else ':'
    return f'--add-data={source}{separator}{destination}'

def clean_previous_builds():
    """Remove old build artifacts"""
    print("Cleaning previous builds...")
    
    folders_to_clean = ['build', 'dist', '__pycache__']
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Removed {folder}/")
    
    if os.path.exists('Chessly.spec'):
        os.remove('Chessly.spec')
        print("   Removed Chessly.spec")

def check_dependencies():
    """Verify all required files exist"""
    print("\nVerifying project dependencies...")
    
    required_files = [
        'ChessMain.py',
        'ChessEngine.py',
        'SmartMoveFinder.py',
        'ChessOpenings.py',
    ]
    
    required_folders = [
        'images',
        'database',
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(f"File: {file}")
    
    for folder in required_folders:
        if not os.path.exists(folder):
            missing.append(f"Folder: {folder}/")
    
    if missing:
        print("\nError: Missing required project components:")
        for item in missing:
            print(f"   • {item}")
        sys.exit(1)
    
    # Check for core asset integrity
    image_files = [
        'wp.png', 'wR.png', 'wN.png', 'wB.png', 'wQ.png', 'wK.png',
        'bp.png', 'bR.png', 'bN.png', 'bB.png', 'bQ.png', 'bK.png'
    ]
    
    missing_images = [img for img in image_files if not os.path.exists(f'images/{img}')]
    if missing_images:
        print(f"\nWarning: {len(missing_images)} asset files are missing.")
        response = input("Continue build anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("   All core dependencies found.")

def create_folders():
    """Ensure required runtime folders exist"""
    print("\nEnsuring folder structure...")
    folders = ['database', 'ui', 'auth', 'admin']
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        init_file = os.path.join(folder, '__init__.py')
        if not os.path.exists(init_file):
            Path(init_file).touch()
    
    print("   Folders ready.")

def build_executable():
    """Execute PyInstaller build process"""
    print("\nStarting build process...")
    
    icon_file = 'images/chessly.png' if os.path.exists('images/chessly.png') else None
    
    build_args = [
        'ChessMain.py',
        '--name=Chessly',
        '--onefile',
        '--windowed',
        build_add_data_arg('images', 'images'),
        build_add_data_arg('database', 'database'),
        '--hidden-import=pygame',
        '--hidden-import=bcrypt',
        '--hidden-import=sqlite3',
        '--hidden-import=login_screen',
        '--hidden-import=admin_panel',
        '--hidden-import=db',
        '--hidden-import=auth',
        '--hidden-import=session',
        '--noconfirm',
    ]
    
    if icon_file:
        build_args.append(f'--icon={icon_file}')
    
    try:
        PyInstaller.__main__.run(build_args)
        return True
    except Exception as e:
        print(f"\nInternal Build Error: {e}")
        return False

def print_success_message():
    """Print final build status"""
    print("\n" + "="*60)
    print("BUILD COMPLETED SUCCESSFULLY")
    print("="*60)
    
    if sys.platform == 'win32':
        exe_name = 'Chessly.exe'
    elif sys.platform == 'darwin':
        exe_name = 'Chessly.app'
    else:
        exe_name = 'Chessly'
    
    exe_path = f'dist/{exe_name}'
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"Location: {exe_path}")
        print(f"Size:     {size_mb:.2f} MB")
    
    print("="*60 + "\n")

def main():
    """Main Orchestration"""
    print("Chessly Build Utility")
    print("---------------------")
    
    try:
        clean_previous_builds()
        check_dependencies()
        create_folders()
        
        if build_executable():
            print_success_message()
        else:
            print("\nBuild failed. Check the logs above for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nBuild interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()