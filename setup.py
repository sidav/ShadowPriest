# TO USE CX_FREEZE:
# type "python setup.py build" in terminal


import sys
from cx_Freeze import setup, Executable

additional_mods = ['numpy.core._methods', 'numpy.lib.format', "_cffi_backend"]
excluded_mods = ['scipy']#["concurrent", "ctypes", "curses", "dateutil", "distutils", "email", "html", "http",
                 # "importlib", "json", "lib2to3", "matplotlib", "multiprocessing", "pkg_resources", "pycparser",
                 # "pydoc_data", "pytz", "scipy", "setuptools", "urllib", "xml", "xmlrpc"]
setup(
    name = "Shadow Priest",
    version = "0.2.0",
    description = "A stealth-focused roguelike.",
    options = {'build_exe': {'includes': additional_mods, 'excludes': excluded_mods, 'optimize': 2}},
    executables = [Executable("ShadowPriest.py")]
)

# NEXT LINES ARE FOR py2exe!
# type "python setup.py py2exe" in terminal

# from distutils.core import setup
# import py2exe
# options={
#     "py2exe": {
#         "includes": "tdl"
#     }
# }
# setup(console=['ShadowPriest.py'])