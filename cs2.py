'''
Script for updating and patching Adobe Photoshop CS2
'''
from shutil import move, copytree, copyfile, rmtree
from time import sleep
import ctypes
import os
import subprocess
import psutil


def is_admin():
    '''
    Check if the script is running as admin
    '''
    try:
        user = (os.getuid() == 0)
    except AttributeError:
        user = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return user

def check_process(process_name):
    '''
    Check if there is any running process that contains the given name process_name.
    '''
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

if __name__ == "__main__":

    if is_admin():

        path = os.path.dirname(os.path.realpath(__file__))
        appdata = os.getenv('APPDATA')
        drive = path.split("\\")[0]
        ps_dir = drive+"\\Program Files (x86)\\Adobe\\Adobe Photoshop CS2"

        # Run CS2 9.0.2 Update Installer
        # https://web.archive.org/web/20210506212649/https://helpx.adobe.com/photoshop/kb/legacy-version-updates.html
        # https://i.imgur.com/WQEJhmF.png
        subprocess.run([path+"\\res\\ps902.exe"], check=True)
        sleep(1)
        while check_process("setup.exe"):
            sleep(1)
            print("Waiting for 9.0.2 Update to be installed")

        # WebP extension install https://github.com/webmproject/WebPShop
        print("\nInstalling WebP File Format")
        try:
            copyfile(path+"\\res\\WebP.8bi", ps_dir+"\\Plug-Ins\\File Formats\\WebP.8bi")
        except FileNotFoundError:
            pass

        # Remove product registration popup
        print("Removing regscreen popup")
        try:
            move(ps_dir+"\\regsresen_US.dll", ps_dir+"\\regsresen_US.dll.bak")
        except FileNotFoundError:
            print("regscreen_US.dll not found. Likely already renamed.")

        # Apply configs for Photoshop and Updater
        print("Applying configs")
        copytree(path+"\\res\\Photoshop", appdata+"\\Adobe\\Photoshop", dirs_exist_ok=True)
        copytree(path+"\\res\\Updater", appdata+"\\Adobe\\Updater", dirs_exist_ok=True)

        # Cleanup install files
        print("Removing installation files")
        try:
            # Inflated installer
            rmtree(drive+"\\PhSp_CS2_UE_Ret")
            # Update files
            rmtree(drive+"\\Program Files\\PSCS2")
        except FileNotFoundError:
            print("No installation files to cleanup")

        print("\nDone")
    else:
        print("Please run as Administrator")

    input("Press [ENTER] to close")
