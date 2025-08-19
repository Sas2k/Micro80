"""
Micro80: Assembler.py
Sas2k 2024

- Micro80 Assembler -

Args:
-i : Input file to assemble [required]
-m : Writing location to be stores when storing
-d : Debug Mode
"""

from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser("Micro80-Assembler")

parser.add_argument(
    "-i",
    "--input",
    dest="input",
    help="Input file to assemble",
    metavar="INPUT",
    required=True,
)
parser.add_argument(
    "-m",
    "--memory",
    dest="memory",
    help="Writing location of code",
    metavar="MEMORY",
    required=False,
    default=None
)
parser.add_argument(
    "-d",
    "--debug",
    dest="debug",
    help="Debug mode",
    action="store_true",
    required=False,
)
args = parser.parse_args()

inputFile = open(args.input, "r")
print(f"Assembling {args.input}...")

code = inputFile.read()
inputFile.close()

code = code.split("\n")
assembledCode = []

for line in code:
    if line == "":
        continue
    if line[0] == ":":
        line.replace(":", "")
        label = line.split(" ")[0]
        assembledCode.append([label])
        continue
    if line[0] == ";":
        continue
    if ";" in line:
        indx = line.index(";")
        line = line[:indx]
    instruction = line.split(" ", 1)
    opcode = instruction[0]
    if len(instruction) == 1:
        operands = None
    else:
        operands = instruction[1].split(";", 1)[0]
        operands = operands.replace(" ", "")
        operands = operands.split(",")
        if len(operands) == 1:
            operands = operands[0]
        if operands == "":
            operands = None
        if operands != None and type(operands) == list:
            for i in range(len(operands)):
                if operands[i] == "":
                    operands.pop(i)
                # check and ignore comments
                if ";" in operands[i]:
                    indx = operands[i].index(";")
                    operands[i] = operands[i][:indx]

    assembledCode.append([opcode, operands])

if args.debug:
    print(assembledCode)

# get the instructions.txt which is in the same directory as this file
instructionTable = open(Path(__file__).parent / "instructions.txt", "r")
instructions = instructionTable.readlines()
instructionTable.close()
instructionTable = {}

for instruction in instructions:
    instructionTable[instruction.split(" : ")[1].strip()] = (
        instruction.split(" : ")[0].replace("\n", "").strip()
    )


# --- PASS 1: build label table ---
memoryCounter = 0x0000
labels = {}

for instruction in assembledCode:
    # label definition
    if len(instruction) == 1:
        labels[instruction[0]] = (
            memoryCounter + int(args.memory, 16) if args.memory else memoryCounter
        )
        continue

    # opcode always takes 1 word
    memoryCounter += 1

    # each operand also takes 1 word
    if instruction[1] is not None:
        if isinstance(instruction[1], list):
            memoryCounter += len(instruction[1])
        else:
            memoryCounter += 1

if args.debug:
    print("Labels:", labels)

# --- PASS 2: generate code ---
memoryCounter = 0x0000
outputFile = open(args.input.replace("./", "").split(".")[0] + ".rom.m80", "w")

for instruction in assembledCode:
    # skip labels (already recorded)
    if len(instruction) == 1:
        continue

    # get opcode
    opcode = str(int(instructionTable[instruction[0]], 16))
    outputFile.write("/" + opcode)
    memoryCounter += 1

    if args.debug:
        print(memoryCounter, ":", instruction)

    # write operands
    if instruction[1] is not None:
        if isinstance(instruction[1], list):
            for operand in instruction[1]:
                if operand in labels:  # label reference
                    outputFile.write("/" + str(labels[operand]))
                else:
                    outputFile.write("/" + str(int(operand, 16)))
                memoryCounter += 1
        else:
            if instruction[1] in labels:
                outputFile.write("/" + str(labels[instruction[1]]))
            else:
                try:
                    outputFile.write("/" + str(int(instruction[1], 16)))
                except ValueError as e:
                    raise ValueError(f"Invalid Label: {instruction[1]}")
            memoryCounter += 1

if args.debug:
    print(labels)            

outputFile.close()
