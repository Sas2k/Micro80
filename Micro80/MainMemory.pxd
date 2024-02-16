"""
Micro80: MainMemory.pxd
Sas2k - 2024

- Micro80 MainMemory Header File -
"""

cdef class MainMemory:
    cdef public list memory
    cdef public int curAddress, curData, stackPointer
    
    cpdef getMemory(self)

    cpdef getCurAddress(self)

    cpdef readAddress(self, int address)

    cpdef writeAddress(self, int address, int data)