"""
Fast2SMS Sender - EXE Builder Script
This script creates a standalone .exe file
"""

import subprocess
import sys
import os
import shutil

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {description} failed!")
        return False

def main():
    print("\n" + "="*60)
    print("  Fast2SMS Sender - EXE Builder")
    print("  M-SWASTH Team")
    print("="*60 + "\n")

    # Step 1: Remove problematic packages
    print("[1/5] Removing problematic packages...")
    run_command("pip uninstall pathlib pathlib2 -y", "Uninstalling pathlib")

    # Step 2: Upgrade pip
    print("\n[2/5] Upgrading pip...")
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("Warning: pip upgrade failed, continuing anyway...")

    # Step 3: Install dependencies
    print("\n[3/5] Installing dependencies...")
    if not run_command("pip install pandas openpyxl requests", "Installing packages"):
        print("\n[ERROR] Failed to install dependencies!")
        input("Press Enter to exit...")
        return False

    # Step 4: Install PyInstaller
    print("\n[4/5] Installing PyInstaller...")
    if not run_command("pip install pyinstaller", "Installing PyInstaller"):
        print("\n[ERROR] Failed to install PyInstaller!")
        input("Press Enter to exit...")
        return False

    # Step 5: Clean old builds
    print("\n[5/5] Cleaning old build files...")
    for path in ['build', 'dist', 'Fast2SMS_Sender.spec']:
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                print(f"  Removed: {path}")
            except Exception as e:
                print(f"  Warning: Could not remove {path}: {e}")

    # Build the executable
    print("\n" + "="*60)
    print("  Building executable...")
    print("  This may take 2-3 minutes, please wait...")
    print("="*60 + "\n")

    build_command = (
        "pyinstaller --onefile --windowed "
        "--name Fast2SMS_Sender "
        "--clean --noconfirm "
        "sms_sender_app.py"
    )

    if not run_command(build_command, "Building executable"):
        print("\n" + "="*60)
        print("  BUILD FAILED!")
        print("="*60)
        print("\nPossible solutions:")
        print("1. Run as Administrator")
        print("2. Try: pip uninstall pathlib -y")
        print("3. Try: pip install --upgrade pyinstaller")
        print("4. Check antivirus isn't blocking PyInstaller")
        input("\nPress Enter to exit...")
        return False

    # Clean up
    print("\nCleaning up build files...")
    for path in ['build', 'Fast2SMS_Sender.spec']:
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except:
                pass

    # Success!
    print("\n" + "="*60)
    print("  SUCCESS!")
    print("="*60)
    print("\nYour executable is ready!")
    print(f"\nLocation: {os.path.join(os.getcwd(), 'dist', 'Fast2SMS_Sender.exe')}")
    print("\nFile size: ~15-20 MB")
    print("\n" + "-"*60)
    print("  What to do next:")
    print("-"*60)
    print("1. Go to 'dist' folder")
    print("2. Copy 'Fast2SMS_Sender.exe'")
    print("3. Share with your team")
    print("4. They double-click to run (no Python needed)!")
    print("="*60 + "\n")

    # Try to open dist folder
    try:
        if os.path.exists('dist'):
            os.startfile('dist')
    except:
        pass

    input("Press Enter to exit...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        input("Press Enter to exit...")
