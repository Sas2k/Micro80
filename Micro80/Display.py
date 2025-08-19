"""
Micro80: Display.py
Sas2k 2024 ~ 2025

- Micro80 Display -
"""

from Micro80.MainMemory import MainMemory
import sdl2
import sdl2.ext


class Display:
    "Micro80 Display class"

    def __init__(
        self,
        memory: MainMemory,
        startAddress: int,
        endAddress: int,
        renderer: sdl2.ext.Renderer,
        display: sdl2.ext.Window,
    ):
        """Initialize the display"""
        self.memory = memory
        self.startAddress = startAddress
        self.endAddress = endAddress
        self.curAddress = startAddress
        self.x = 0
        self.y = 0
        self.renderer = renderer
        self.display = display

    def render(self):
        """Render the display to the screen"""
        for y in range(0, 128):
            rowData = self.memory.readAddress(self.curAddress, readSize=128)
            for x in range(0, 128):
                color = rowData[x]
                r = ((color >> 11) & 0x1F) << 3
                g = ((color >> 5) & 0x3F) << 2
                b = (color & 0x1F) << 3
                self.renderer.draw_rect((2*x, 2*y, 2, 2), sdl2.ext.Color(r, g, b))
                self.curAddress += 1
        self.curAddress = self.startAddress

    def clear(self):
        """Clear the display"""
        self.renderer.clear(sdl2.ext.Color(0, 0, 0))
