#!/usr/bin/env python3
import os
import sys
import urllib.request
import json
import zipfile
import subprocess

# Configuración del repositorio y las rutas de instalación
REPO = "adri22235/azahar-hotfix-2026"
INSTALL_DIR = os.path.expanduser("~/AzaharVanguard")
SDMC_DIR = os.path.expanduser("~/.local/share/azahar-emu/sdmc")

def print_title():
    print("=========================================")
    print("        AZAHAR VANGUARD INSTALLER        ")
    print("=========================================")

def check_latest_release():
    print("[*] Conectando con la API de GitHub para buscar lanzamientos...")
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            tag = data["tag_name"]
            assets = data["assets"]
            print(f"[+] ¡Lanzamiento más reciente localizado!: {tag}")
            return assets
    except Exception as e:
        print(f"[-] Error al consultar la API de GitHub: {e}")
        sys.exit(1)

def download_asset(assets):
    download_url = None
    filename = None
    for asset in assets:
        if "linux" in asset["name"].lower() and asset["name"].endswith(".zip"):
            download_url = asset["browser_download_url"]
            filename = asset["name"]
            break
    
    if not download_url:
        print("[-] No se encontró ningún archivo .zip para Linux en la Release.")
        sys.exit(1)

    print(f"[*] Descargando {filename} usando curl...")
    os.makedirs(INSTALL_DIR, exist_ok=True)
    dest_path = os.path.join(INSTALL_DIR, filename)
    
    # Invocamos a curl de forma directa tal como especificaste
    cmd = ["curl", "-L", "-o", dest_path, download_url]
    try:
        subprocess.run(cmd, check=True)
        print(f"[+] Archivo descargado con éxito en: {dest_path}")
        return dest_path
    except subprocess.CalledProcessError as e:
        print(f"[-] La descarga con curl falló: {e}")
        sys.exit(1)

def extract_asset(zip_path):
    print(f"[*] Extrayendo el emulador en {INSTALL_DIR}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(INSTALL_DIR)
        print(f"[+] ¡Extracción completada con éxito!")
        # Dar permisos de ejecución al emulador
        binary_path = os.path.join(INSTALL_DIR, "azahar")
        if os.path.exists(binary_path):
            os.chmod(binary_path, 0o755)
    except Exception as e:
        print(f"[-] Falló la extracción del archivo: {e}")

def setup_sdmc():
    print("[  0%] Built target sdmc_directories")
    mkdir_path = os.path.join(SDMC_DIR, "3ds/ctrQuake/id1")
    os.makedirs(mkdir_path, exist_ok=True)
    print(f"[100%] Built target sdmc_directories en: {mkdir_path}")

if __name__ == "__main__":
    print_title()
    assets = check_latest_release()
    zip_path = download_asset(assets)
    extract_asset(zip_path)
    setup_sdmc()
    print("\n=========================================")
    print("[+] ¡Instalación y puesta a punto de Vanguard completada!")
    print(f"    Ya puedes ejecutar tu emulador en: {os.path.join(INSTALL_DIR, 'azahar')}")
    print("=========================================")
