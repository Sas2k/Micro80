"""
Micro80: MainMemory.py
Sas2k 2024 ~ 2025

- Micro80 Main Memory -

"""

# 0x0000 - 0xFFFF : Total Memory      : 128kb
# -----------------:-------------------:-----------
# 0x0000 - 0x3FFF : Program Memory    : 32kb
# 0x4000 - 0x43FF : Reserved          :  4kb [0x4009 : Run Status] [0x400A : Render Status] [0x400B ~ 0x400D : Inputs]
# 0x4400 - 0x4BFF : Variable Memory   :  4kb
# 0x4C00 - 0x53FF : Character Memory  :  4kb
# 0x5400 - 0x5BFF : Stack Memory      :  4kb
# 0x5C00 - 0xBFFF : ROM               : 48kb
# 0xC000 - 0xFFFF : Video Memory      : 32kb


class MainMemory:
    """Micro80 Main Memory class"""

    def __init__(self):
        "Initialize the main memory"
        self.memory = [0x0000] * 1024 * 64
        self.curAddress = 0x0000
        self.curData = 0x0000
        self.stackPointer = 0x5400

    def getMemory(self):
        "Return the memory array"
        return self.memory

    def getCurAddress(self):
        "Return the current address"
        return self.curAddress

    def readAddress(self, address, readSize=1):
        "Read an address from the memory"
        if address < 0x0000 or address > 0xFFFF:
            raise ValueError(f"Memory address out of range: {address}")
        else:
            if readSize == 1:
                self.curAddress = address
                self.curData = self.memory[address]
                return self.memory[address]
            else:
                self.curAddress = address + readSize
                self.curData = self.memory[address]
                return self.memory[address:self.curAddress]

    def writeAddress(self, address, data):
        "Write data to an address in the memory"
        if address < 0x0000 or address > 0xFFFF:
            raise ValueError("Memory address out of range")
        else:
            self.curAddress = address
            self.curData = data
            self.memory[address] = data
