# Requires cx_freeze
# build command: python build.py build
import shutil, os
from cx_Freeze import setup, Executable
from shutil import copytree

build_exe_options = {
    "packages": [
        "os",
        "ctypes",
        "subprocess",
        "psutil",
        "time",
        "shutil"
    ],
    "excludes": [
        "tkinter",
        "PyQt4.QtSql",
        "sqlite3",
        "scipy.lib.lapack.flapack",
        "PyQt4.QtNetwork",
        "PyQt4.QtScript",
        "numpy.core._dotblas",
        "PyQt5",
        "email",
        "asyncio",
        "http",
        "unittest"
    ],
    "optimize": 2,
    "build_exe": "dist"
    }

target = Executable(
    script="cs2.py"
    #icon="lib\\icon.ico"
    )

setup(
    name="CS2 Patcher",
    version="1.0",
    description="Patch Photoshop CS2",
    author="downthecrop",
    options={"build_exe": build_exe_options},
    executables=[target]
    )

path = os.path.dirname(os.path.realpath(__file__))
copytree(path+"\\res", path+"\\dist\\res", dirs_exist_ok=True)