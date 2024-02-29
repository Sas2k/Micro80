"""
Micro80: Setup.py
Sas2k 2024

- Micro80 Cython Compilation Setup -
"""

from setuptools import setup, find_packages
from Cython.Build import cythonize

import os

files = os.listdir("Micro80")
compile = []

options = input("Do you wish to compile all files? (y/n): ")

if options.lower() == "n":
    file = input("Enter the file names separated by a space: ")
    files = file.split(" ")
    for i in range(len(files)):
        if (
            files[i] != "__init__.py"
            and files[i] != "__main__.py"
            and files[i] != "Assembler.py"
            and files[i].endswith(".py")
        ):
            compile.append("Micro80/" + files[i])
else:
    for i in range(len(files)):
        if (
            files[i] != "__init__.py"
            and files[i] != "__main__.py"
            and files[i] != "Assembler.py"
            and files[i].endswith(".py")
        ):
            compile.append("Micro80/" + files[i])

print(compile)

setup(name="Micro80", ext_modules=cythonize(compile), packages=find_packages())
