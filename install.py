
### enter  python install.py
import os
import sys
import subprocess

def install_venv():
    """instalation sequence inicialization...   instal go brrrrrr."""
    venv_dir = "venv"
    requirements_file = "requirements.txt"
    
    # Vytvoření virtuálního prostředí
    if not os.path.exists(venv_dir):
        print("create a virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir])
    else:
        print("virtual environment creation failed")
    
    # Instalace požadovaných knihoven
    pip_executable = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    print("installing libraries from requirements.txt")
    subprocess.run([pip_executable, "install", "-r", requirements_file])
    
    print("Installation complete")

if __name__ == "__main__":
    install_venv()
