# TO USE CX_FREEZE:
# type "python setup.py build" in terminal


import sys
from cx_Freeze import setup, Executable

additional_mods = ['numpy.core._methods', 'numpy.lib.format', "_cffi_backend"]
excluded_mods = ['scipy', 'http', 'html', 'email']#["concurrent", "ctypes", "curses", "dateutil", "distutils",
                 # "importlib", "json", "lib2to3", "matplotlib", "multiprocessing", "pkg_resources", "pycparser",
                 # "pydoc_data", "pytz", "scipy", "setuptools", "urllib", "xml", "xmlrpc"]
include_files = ['shadowpriest8x12_gs_ro.png', 'shadowpriest16x24_gs_ro.png', 'shadowpriest12x20.png']

setup(
    name = "Shadow Priest",
    version = "0.2.0",
    description = "A stealth-focused roguelike.",
    options = {'build_exe': {'build_exe': 'build/ShadowPriest', 'includes': additional_mods, 'excludes': excluded_mods,
                             'include_files': include_files, 'optimize': 2}},
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