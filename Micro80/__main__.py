"""
Micro80: __main__.py
Sas2k - 2024

- Micro80 Runner -

Args:
-d : runs the ROM file in debug mode
-f : the location of the ROM file to run [required]
-m : the memory location to store the ROM file
"""

from argparse import ArgumentParser
from pathlib import Path

from Micro80.CPU import CPU
from Micro80.MainMemory import MainMemory

from timeit import timeit

import sys

__version__ = "1.0-Alpha"

parser = ArgumentParser(description="Micro80")

parser.add_argument("-d", "--debug", help="Debug Mode", action="store_true")
parser.add_argument("-f", "--file", help="ROM File to load", type=str)
parser.add_argument("-m", "--memory", help="location to load ROM File", type=str)

args = parser.parse_args()

memory = MainMemory()
cpu = CPU(memory, args.debug)

if args.debug:
    print("Debug Mode Enabled")
    print("Python Version: ", sys.version)

if args.file:
    if args.debug:
        print("ROM File: ", args.file)
    file = Path(args.file)
    if args.memory:
        if args.debug:
            print("Memory Location: ", args.memory)
        cpu.Loader(file, args.memory)
    else:
        cpu.Loader(file)

    cpu.runProgram()
