@echo off
REM Kontrola, zda je Python nainstalován
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python není nainstalován. Instalace Pythonu...
    REM Stáhněte Python z oficiálního webu (zde je příklad pro verzi 3.10.9)
    powershell -Command "& {Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe -OutFile python-installer.exe}"
    REM Spusťte instalátor Pythonu (tichá instalace)
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    REM Odstranění instalátoru po instalaci
    del python-installer.exe
)

REM Kontrola, zda je Python nyní dostupný
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python se nepodařilo nainstalovat. Zkontrolujte instalaci ručně.
    pause
    exit /b 1
)

REM Spuštění install.py pro vytvoření venv a instalaci závislostí
echo Vytvářím virtuální prostředí a instaluji závislosti...
python install.py

REM Aktivace virtuálního prostředí
echo Aktivace virtuálního prostředí...
call venv\Scripts\activate.bat

REM Spuštění run.py
echo Spouštění aplikace...
python run.py

REM Deaktivace virtuálního prostředí
deactivate

pause
