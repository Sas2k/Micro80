"""
Micro80: CPU.py
Sas2k 2024 ~ 2025

- Micro80 CPU -
"""

from Micro80.MainMemory import MainMemory
from Micro80.Display import Display

from pathlib import Path

import sdl2
import sdl2.ext
import time
import os

class CPU:
    """The CPU class for the Micro80 Emulator"""

    def __init__(self, memory: MainMemory, debug: bool):
        "Initializes the CPU, Registers, pointers and the instruction set."
        self.debug = debug
        self.memory = memory
        self.programCounter = 0x0000
        self.stackPointer = memory.stackPointer
        self.RunStatus = 0x4009
        self.instructionTable = open(
            Path(__file__).parent / "instructions.txt", "r")
        self.instructions = {}
        self.List = self.instructionTable.read().split("\n")
        for i in self.List:
            self.instructions[int(i.split(":")[0].strip(), base=16)] = i.split(":")[
                1
            ].strip()
        self.instructionTable.close()
        self.registers = {
            "A": 0x0000,
            "B": 0x0000,
            "C": 0x0000,
            "D": 0x0000,
            "E": 0x0000,
            "F": 0x0000
        }
        self.operations = {
            "ADD": lambda x, y: x + y,
            "SUB": lambda x, y: x - y,
            "MUL": lambda x, y: x * y,
            "DIV": lambda x, y: x / y,
            "MOD": lambda x, y: x % y,
            "AND": lambda x, y: x & y,
            "OR": lambda x, y: x | y,
            "XOR": lambda x, y: x ^ y,
            "NOT": lambda x, y: ~x,
            "SHL": lambda x, y: x << y,
            "SHR": lambda x, y: x >> y,
            "CMP": lambda x, y: x - y
        }
        self.adr = 0x0000
        self.sleepTimer = 0
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Micro80", (128, 128))
        self.render = sdl2.ext.Renderer(self.window)
        self.display = Display(self.memory, 0xC000,
                               0xFFFF, self.render, self.window)
        self.window.show()
        print("CPU Initialized...")
        if self.debug:
            print("Debug Mode Enabled...")

    def runProgram(self):
        "Runs the program stores in memory"
        debug = self.debug
        renderLocations = []
        renderAmount = 0
        ticks = 0
        self.jumpCount = 0
        if self.debug:
            for x in range(0x0000, 0x003F):
                (
                    print(x, self.instructions[self.memory.readAddress(x)])
                    if self.memory.readAddress(x) <= 0x004A
                    else print(x, self.memory.readAddress(x))
                )
        print("Program Running....")
        while self.memory.readAddress(self.RunStatus) == 0x0000:
            if self.sleepTimer != 0:
                self.sleepTimer -= 1
                continue
            self._handleEvents()
            self.fetch()
            self.execute(self.curOpcode, self.curOperand)
            if self.memory.readAddress(0x400A) == 1:
                self.display.render()
                self.render.present()
                self.window.refresh()
                self.memory.writeAddress(0x400A, 0)
                renderLocations.append(self.programCounter)
                renderAmount += 1
            ticks += 1
        if debug:
            print(f"Jump Count: {self.jumpCount}")
            print(f"Render Count: {renderAmount}")
            print(f"Ticks: {ticks}")
            print(
                f"Accumulator: {self.registers["A"]}, B: {self.registers["B"]}, C: {self.registers["C"]}, D: {
                    self.registers["D"]}, E: {self.registers["E"]}, F: {self.registers["F"]}"
            )
            print(
                f"Program Counter: {self.programCounter}, Stack Pointer: {
                    self.stackPointer}, Address: {self.adr}"
            )
            print(
                f"Input: {self.memory.readAddress(0x400B)}, {self.memory.readAddress(0x400C)}, {
                    self.memory.readAddress(0x400D)}"
            )
            print(f"Variables: {self.memory.memory[0x4400:0x440F]}")
            print(f"Display: {self.memory.memory[0xC000:0xC00F]}")
            print(f"Current Address: {self.adr}, Current Data: {
                  self.memory.curData}" )
        print("Program End.")

    def fetch(self):
        "Fetches the current opcode and operand from memory."
        self.curOpcode = self.memory.readAddress(self.programCounter)
        if self.programCounter <= 0x3FFF:
            self.programCounter += 1
        else:
            raise ValueError("Memory Overflow")
        singleOpcode = (
            [0x0000, 0x002D] +
            [x for x in range(0x0035, 0x0046)] + [0x0049, 0x004A]
        )
        if self.curOpcode not in singleOpcode:
            self.curOperand = self.memory.readAddress(self.programCounter)
            if self.curOpcode == 0x0047:
                self.curOperand = [
                    self.memory.readAddress(self.programCounter)]
                self.programCounter += 1
                self.curOperand.append(
                    self.memory.readAddress(self.programCounter))
            self.programCounter += 1
        else:
            self.curOperand = None

    def _handleEvents(self):
        "Handles the SDL2 events"
        events = sdl2.ext.get_events()
        DPadKeys = {
            sdl2.SDLK_UP: 1,
            sdl2.SDLK_DOWN: 2,
            sdl2.SDLK_LEFT: 3,
            sdl2.SDLK_RIGHT: 4,
            sdl2.SDLK_w: 1,
            sdl2.SDLK_s: 2,
            sdl2.SDLK_a: 3,
            sdl2.SDLK_d: 4,
        }
        ActionKeys = {
            sdl2.SDLK_j: 1,
            sdl2.SDLK_k: 2,
            sdl2.SDLK_z: 3,
            sdl2.SDLK_x: 4,
            sdl2.SDLK_RETURN: 5,
            sdl2.SDLK_BACKSPACE: 6,
        }
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self.memory.writeAddress(self.RunStatus, 0x0001)
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    self.memory.writeAddress(self.RunStatus, 0x0001)
                    break
                elif event.key.keysym.sym in DPadKeys:
                    if self.memory.readAddress(0x400B) == 0x0000:
                        self.memory.writeAddress(
                            0x400B, DPadKeys[event.key.keysym.sym])
                    else:
                        self.memory.writeAddress(
                            0x400C, DPadKeys[event.key.keysym.sym])
                elif event.key.keysym.sym in ActionKeys:
                    self.memory.writeAddress(
                        0x400D, ActionKeys[event.key.keysym.sym])
            if event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in DPadKeys:
                    if (
                        self.memory.readAddress(0x400B)
                        == DPadKeys[event.key.keysym.sym]
                    ):
                        self.memory.writeAddress(0x400B, 0x0000)
                    else:
                        self.memory.writeAddress(0x400C, 0x0000)
                if event.key.keysym.sym in ActionKeys:
                    self.memory.writeAddress(0x400D, 0x0000)
        if self.debug:
            print(self.memory.memory[0x400B:0x400D])

    def execute(self, opcode, operands):
        "Executes the code"
        instructions = self.instructions
        if opcode not in instructions:
            raise ValueError(f"Invalid Opcode, {hex(opcode)}: Memory. {self.memory.curAddress}")
        if self.debug:
            print(instructions[opcode], operands)
            print(self.programCounter, opcode, operands)
            print(self.memory.memory[0x4400:0x4410])
            print(self.registers)
        if instructions[opcode] == "NOP":
            pass
        elif instructions[opcode] == "HLT":
            self.memory.writeAddress(self.RunStatus, 0x0001)
        elif instructions[opcode][0:2] == "LD":
            self.load(instructions[opcode][2:], operands)
        elif instructions[opcode][0:2] == "ST":
            self.store(instructions[opcode][2:], operands)
        elif instructions[opcode] in self.operations.keys():
            self.alu(instructions[opcode], operands, self.operations)
        elif instructions[opcode][0] == "J":
            self.jump(instructions[opcode][1:], operands)
        elif instructions[opcode] == "CALL":
            self.call(operands)
        elif instructions[opcode] == "RET":
            self.ret()
        elif instructions[opcode] == "PUSH":
            self.push(operands)
        elif instructions[opcode] == "POP":
            self.pop(operands)
        elif instructions[opcode] == "PUSHA":
            self.pushAll()
        elif instructions[opcode] == "POPA":
            self.popAll()
        elif instructions[opcode] == "SLP":
            time.sleep(operands)
        elif instructions[opcode] == "WDir":
            self.memory.writeAddress(self.adr, operands)
        elif instructions[opcode] == "RDir":
            self.memory.readAddress(operands)
        elif instructions[opcode] == "WAdr":
            self.adr = operands
            self.memory.curData = self.memory.readAddress(operands)
        elif instructions[opcode] == "MOV":
            data = self.memory.readAddress(operands[0])
            location = self.memory.readAddress(operands[1])
            self.memory.writeAddress(location, data)
        elif instructions[opcode][0:3] == "INC" or instructions[opcode][0:2] == "IC":
            if instructions[opcode][0:3] == "INC":
                self.increment(instructions[opcode][3:])
            else:
                if instructions[opcode][2:] == "Ad":
                    self.adr += 1
                else:
                    raise ValueError("Invalid Opcode")
        elif instructions[opcode][0:3] == "DEC" or instructions[opcode][0:2] == "DC":
            if instructions[opcode][0:3] == "DEC":
                self.decrement(instructions[opcode][3:])
            else:
                if instructions[opcode][2:] == "Ad":
                    self.adr -= 1
                else:
                    raise ValueError("Invalid Opcode")
        elif instructions[opcode] == "CLS":
            self.display.clear()
            self.render.present()
            self.window.refresh()
        else:
            raise ValueError(f"Invalid Opcode, {hex(opcode)}")

    def popAll(self):
        "Pops off all of the registers from the stack."
        self.pop(self.stackPointer)
        self.pop(self.programCounter)
        for key in self.registers.keys()[::-1]:
            self.pop(self.registers[key])

    def pushAll(self):
        "Pushes all of the registers onto the stack."
        for key in self.registers.keys():
            self.pop(self.registers[key])
        self.push(self.programCounter)
        self.push(self.stackPointer)

    def pop(self, operands):
        "Pops off the top of the stack and stores it in the given address."
        self.stackPointer -= 1
        if operands is not None:
            self.memory.writeAddress(
                operands, self.memory.readAddress(self.stackPointer)
            )
        else:
            self.memory.writeAddress(self.stackPointer + 1, 0)

    def push(self, operands):
        "Pushes the given data onto the stack."
        self.memory.writeAddress(self.stackPointer, operands)
        self.stackPointer += 1

    def ret(self):
        "Returns to the address on the top of the stack."
        self.stackPointer -= 1
        self.programCounter = self.memory.readAddress(self.stackPointer)

    def call(self, operands):
        "Calls the given address."
        self.memory.writeAddress(self.stackPointer, self.programCounter)
        self.stackPointer += 1
        self.programCounter = operands

    def increment(self, register):
        "Increments a given register."
        if register in self.registers.keys():
            self.registers[register] += 1
        elif register == "SP":
            self.stackPointer += 1
        elif register == "P":
            self.programCounter += 1
        else:
            raise ValueError("Invalid Register")

    def decrement(self, register):
        "Decrements a given register."
        if register in self.registers.keys():
            self.registers[register] -= 1
        elif register == "SP":
            self.stackPointer -= 1
        elif register == "P":
            self.programCounter -= 1
        else:
            raise ValueError("Invalid Register")

    def load(self, register, operands):
        "Loads a value from an address to a register."
        if register in self.registers.keys():
            self.registers[register] = self.memory.readAddress(operands)
        elif register == "Ad":
            self.adr = self.memory.readAddress(operands)
        elif register == "SP":
            self.memory.stackPointer = self.memory.readAddress(operands)
        elif register == "PC":
            self.programCounter = self.memory.readAddress(operands)
        elif register == "ST":
            self.stackPointer = self.memory.readAddress(operands)
        else:
            raise ValueError("Invalid Register")

    def store(self, register, operands):
        "Stores a value from a register to an address."
        if operands is None:
            operands = self.adr
        if register in self.registers.keys():
            self.memory.writeAddress(operands, self.registers[register])
        elif register == "ST":
            self.memory.writeAddress(operands, self.stackPointer)
        elif register == "Ad":
            self.memory.writeAddress(operands, self.adr)
        elif register == "PC":
            self.memory.writeAddress(operands, self.programCounter)
        else:
            raise ValueError("Invalid Register")

    def alu(self, opcode, operands, operations):
        "Performs an ALU operation."
        if opcode in operations.keys():
            self.registers["A"] = operations[opcode](
                self.registers["A"], self.memory.readAddress(operands))
        else:
            raise ValueError("Invalid Opcode")

    def jump(self, opcode, operands):
        """Jumps to a given address based on the condition."""
        self.jumpCount += 1
        A = self.registers["A"]
        B = self.memory.curData  # shorthand

        # Map opcodes to their conditions
        conditions = {
            "Z":   lambda: A == 0,
            "NZ":  lambda: A != 0,
            "GZ":  lambda: A > 0,
            "LEZ": lambda: A <= 0,
            "GEZ": lambda: A >= 0,
            "LZ":  lambda: A < 0,

            "GT":  lambda: A > B,
            "LT":  lambda: A < B,
            "GE":  lambda: A >= B,
            "LE":  lambda: A <= B,
            "EQ":  lambda: A == B,
            "NE":  lambda: A != B,
        }

        if opcode == "MP":  # unconditional jump
            self.programCounter = operands
            return

        if opcode not in conditions:
            self.jumpCount -= 1
            raise ValueError(f"Invalid Opcode: {hex(opcode)}")

        if conditions[opcode]():
            self.programCounter = operands

    def Loader(self, ROMFile, location=0x0000):
        "Loads the ROM file into memory."
        file = open(ROMFile, "r")
        ROM = file.read()
        file.close()
        programCode = ROM.split("\n")[0]
        programCode = programCode.split("/")[1:]
        for i in programCode:
            self.memory.writeAddress(location, int(i))
            location += 1
        if self.debug:
            print(f"Loaded {ROMFile} into memory...")
