"""
Micro80: Display.pxd
Sas2k 2024

- Micro80 Display Header File -
"""

from Micro80.MainMemory import MainMemory
cimport sdl2
cimport sdl2.ext

cdef class Display:
    cdef public memory
    cdef public int startAddress, endAddress, x, y, curAddress
    cdef public renderer
    cdef public display
    
    cpdef render(self)
