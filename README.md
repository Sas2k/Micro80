<h1 align="center">📺 Micro80</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/Sas2k/Micro80.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Sas2k/Micro80.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

<h3 align="center"> A 16-bit Console that **never** existed.
    <br> 
</h3>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
- [✨ Features ](#-features-)
  - [📃 To-Do](#-to-do)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🎈 Usage ](#-usage-)
- [⛏️ Built Using ](#️-built-using-)
- [✍️ Authors ](#️-authors-)

## 🧐 About <a name = "about"></a>

An Emulator for a 16-bit Console that never existed.

The Micro80 is a 16-bit Console with 9 Registers, 128Kib of Main Memory and a 128x128 Graphics Display.

To find out about on how to Contribute to the Project, Check out the [Contributing.md](CONTRIBUTING.md) File.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and Running Purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

## ✨ Features <a name = "features"></a>

- 16-bit CPU with 9 registers
- 128Kib of Main Memory.
- 16-bit Graphics with 128x128 Resolution.
- 74 Instructions.

### 📃 To-Do

- [ ] Make Character-Maps for the Graphics Display.
- [ ] Add Inputs.
- [ ] Add Sound Chips.
- [ ] Create a High-Level Language to Code in.
- [ ] Bring up the Clock Speed
- [ ] Create a Documentation.

### Prerequisites

- Python 3.10 or higher
- Cython
- PySDL2
- Virtualenv (Optional)
- Black (Code Formatting/Styling)

### Installing

A how-to guide that will help you get started with the project.

First off, Clone the repository on to your local machine.

```bash
git clone <http-repo-url>
```

then, navigate to the directory and create a virtual environment.

```bash
cd Micro80
python -m virtualenv venv
```

Activate the virtual environment

```bash
source venv/bin/activate #for linux
```
```powershell
.\venv\Scripts\activate #for windows
```

Install the required packages

```bash
pip install -r requirements.txt
```

Then, the project is Set-Up.

> If the *.pyd files are not present, or if you done any changes to the code. please build it using the following commands
> ```bash
> python setup.py build_ext --inplace
> ```
> Then, change the file names to have `name.pyd`
> `MainMemory.cp310-win_amd64.pyd` to `MainMemory.pyd`

## 🎈 Usage <a name="usage"></a>

Here is a simple example on how to run the project.

first create a `main.asm80` file with the following code.

```c
; main.asm80 <- this is a comment
WAdr 0x4400
WDir 0x0005 ; Go to Address 0x4400 (in variables) and set the value to 5
WAdr 0x4401
WDir 0x0006 ; Go to Address 0x4401 (in variables) and set the value to 6

LDA 0x4400 ; Load the value at 0x4400 into the Accumulator
ADD 0x4401 ; Add the value at 0x4401 to the Accumulator
STA 0x4402 ; Store the value in the Accumulator to 0x4402

HLT ; Halt the CPU
```

then, Assemble it to a ROM file.

```bash
python -m Micro90.Assembler -i main.asm80
```

Then, run in debug mode. to See changes in the memory and the CPU.

```bash
python -m Micro80 -f main.rom.m80 -d
```

And that's it! You have a simple program running on the Micro80 Emulator.

To find out more on the language (for now...) check out the [Instructions.txt](Micro80\instructions.txt) in the Main Folder and the Assembly Codes in the [Assembly-Programs](Micro80\Assembly-Programs) Folder.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Coded In
- [Cython](https://cython.org/) - Improved Performance
- [PySDL2](https://pysdl2.readthedocs.io/en/rel_0_9_7/) - Graphics Library

## ✍️ Authors <a name = "authors"></a>

- [@Sas2k](https://github.com/Sas2k) - Idea & Initial work

See also the list of [contributors](https://github.com/Sas2k/Micro80/contributors) who participated in this project.

