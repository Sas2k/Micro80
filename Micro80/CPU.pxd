""""
Micro80: CPU.pxd
Sas2k 2024

- Micro80 CPU Header File -
"""

from Micro80.MainMemory import MainMemory
from Micro80.Display import Display

from pathlib import Path

cimport sdl2
cimport sdl2.ext
import time

cdef class CPU:
    cdef public debug
    cdef public memory
    cdef public int programCounter, stackPointer, RunStatus, adr, sleepTimer, jumpCount
    cdef public curOpcode
    cdef public curOperand
    cdef public instructionTable
    cdef public dict instructions, registers, operations
    cdef public list List
    cdef public window
    cdef public display
    cdef public render

    cpdef runProgram(self)

    cpdef fetch(self)

    cpdef _handleEvents(self)

    cpdef execute(self, int opcode, operands)

    cpdef popAll(self)

    cpdef pushAll(self)

    cpdef pop(self, int operands)

    cpdef push(self, int operands)

    cpdef ret(self)

    cpdef call(self, int operands)

    cpdef increment(self, str register)

    cpdef decrement(self, str register)

    cpdef load(self, str register, int operands)

    cpdef store(self, str register, int operands)

    cpdef alu(self, str opcode, int operands, dict operations)

    cpdef jump(self, str opcode, int operands)

    cpdef Loader(self, ROMFile, int location=*)
