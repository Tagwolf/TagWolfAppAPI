import os
import sys
import shutil
from pathlib import Path

def install_requirements():
    print("Installiere Requirements...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    os.system(f"{sys.executable} -m pip install pyinstaller")

def create_exe():
    print("\nErstelle TagWolf.exe...")
    
    src_path = Path(__file__).parent.parent / "src"
    
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "TagWolf",
        "--icon", "NONE",
        "--add-data", f"{src_path}/gui.py;.",
        "--add-data", f"{src_path}/api_client.py;.",
        "--hidden-import", "requests",
        str(src_path / "main.py")
    ]
    
    os.system(" ".join(cmd))
    
    if os.path.exists("dist/TagWolf.exe"):
        shutil.copy("dist/TagWolf.exe", "../TagWolf.exe")
        print("\n✓ EXE wurde erstellt: ../TagWolf.exe")

def create_installer():
    installer_content = '''@echo off
echo ================================
echo       TAGWOLF INSTALLER
echo ================================
echo.
echo Installiere TagWolf App...
echo.

set "SOURCE=%~dp0TagWolf.exe"
set "DEST=%USERPROFILE%\\Desktop\\TagWolf.lnk"

if exist "%SOURCE%" (
    echo Erstelle Desktop-Verknüpfung...
    powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%DEST%'); $SC.TargetPath = '%SOURCE%'; $SC.Save()"
    echo.
    echo ================================
    echo    INSTALLATION ABGESCHLOSSEN!
    echo ================================
    echo.
    echo Die App wurde auf dem Desktop installiert.
    echo Starten Sie sie durch Doppelklick auf "TagWolf".
) else (
    echo Fehler: TagWolf.exe nicht gefunden!
    echo Bitte stellen Sie sicher, dass die EXE im gleichen Ordner ist.
)
echo.
pause
'''
    
    with open("../install_tagwolf.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✓ Installer erstellt: ../install_tagwolf.bat")

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    install_requirements()
    create_exe()
    create_installer()
    
    print("\n=== FERTIG! ===")
    print("1. TagWolf.exe wurde erstellt")
    print("2. Zum Installieren: install_tagwolf.bat ausführen")
