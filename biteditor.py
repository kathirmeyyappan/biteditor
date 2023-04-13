"""
pygame application that runs a very simple bit editor.
created in CMSC 14200 Introduction to Computer Science II as a 
homework assignment
"""

import os
import sys
from typing import List, Tuple, Dict, Optional
from flood_fill import flood_fill, white_flood_fill

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # pylint: disable=wrong-import-position
sys.setrecursionlimit(1100) # bypassing flood_fill error for empty grid


class BitEdit:
    """
    Class for a GUI-based bitmap editor
    """

    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock
    tool_mode : str # 'black', 'white', 'fill', 'white_fill', 'blackout',
                    # 'whiteout', or 'checker'
    tool_dict : Dict[str, Tuple[int, int]] # maps tool to tool button location

    def __init__(self, window: int = 600, border: int = 10,
                 cells_side: int = 32):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            cells_side : int : number of cells on a side of a square bitmap grid
        """
        self.window = window
        self.border = border
        self.grid = [[False] * cells_side for i in range(cells_side)]
        self.tool_mode = "black"
        self.cells_side = cells_side
        self.tool_dict = {
            'black': self.black_tool_center,
            'white': self.white_tool_center,
            'fill': self.fill_tool_center,
            'white_fill': self.white_fill_tool_center,
            'blackout': self.blackout_tool_center,
            'whiteout': self.whiteout_tool_center,
            'checker': self.checker_tool_center
        }

        # Initialize Pygame
        pygame.init()
        # Set window title
        pygame.display.set_caption("BitEdit")
        # Set window size
        self.surface = pygame.display.set_mode((window + border + cells_side,
                                                window))
        self.clock = pygame.time.Clock()
        self.event_loop()

    @property
    def square(self) -> int:
        """
        property for each cell's side length
        """
        return (self.window - 2 * self.border) // self.cells_side

    @property
    def mini_left(self) -> int:
        """
        x-coord for minigrid
        """
        return 2 * self.border + self.square * self.cells_side

    @property
    def mini_top(self) -> int:
        """
        x-coord for minigrid
        """
        return (self.window - self.cells_side) // 2

    @property
    def black_tool_center(self) -> Tuple[int, int]:
        """
        location of black_tool
        """
        return (self.mini_left + self.cells_side // 2,
                self.border + self.cells_side // 2)

    @property
    def white_tool_center(self) -> Tuple[int, int]:
        """
        location of white_tool
        """
        return (self.mini_left + self.cells_side // 2,
                self.border + 3 * (self.cells_side // 2))

    @property
    def fill_tool_center(self) -> Tuple[int, int]:
        """
        location of fill_tool
        """
        return (self.mini_left + self.cells_side // 2,
                2 * self.border + 5 * (self.cells_side // 2))

    @property
    def white_fill_tool_center(self) -> Tuple[int, int]:
        """
        location of white_fill_tool
        """
        return (self.mini_left + self.cells_side // 2,
                2 * self.border + 7 * (self.cells_side // 2))

    @property
    def blackout_tool_center(self) -> Tuple[int, int]:
        """
        location of blackout_tool
        """
        return (self.mini_left + self.cells_side // 2,
                3 * self.border + 9 * (self.cells_side // 2))

    @property
    def whiteout_tool_center(self) -> Tuple[int, int]:
        """
        location of whiteout_tool
        """
        return (self.mini_left + self.cells_side // 2,
                3 * self.border + 11 * (self.cells_side // 2))

    @property
    def checker_tool_center(self) -> Tuple[int, int]:
        """
        location of checker_tool
        """
        return (self.mini_left + self.cells_side // 2,
                4 * self.border + 13 * (self.cells_side // 2))

    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        # background
        self.surface.fill((128, 128, 128))

        rect = (self.mini_left, self.mini_top, self.cells_side, self.cells_side)
        pygame.draw.rect(self.surface, color=(255, 255, 255),
                         rect=rect)

        # black button
        pygame.draw.circle(self.surface, color=(0, 0, 0),
                           center=self.black_tool_center,
                           radius=self.cells_side // 2)

        # white button
        pygame.draw.circle(self.surface, color=(255, 255, 255),
                           center=self.white_tool_center,
                           radius=self.cells_side // 2)
        pygame.draw.circle(self.surface, color=(0, 0, 0),
                           center=self.white_tool_center,
                           radius=self.cells_side // 2,
                           width=2)

        # fill button
        pygame.draw.circle(self.surface, color=(0, 0, 0),
                           center=self.fill_tool_center,
                           radius=self.cells_side // 2)
        pygame.draw.circle(self.surface, color=(255, 255, 255),
                           center=self.fill_tool_center,
                           radius=self.cells_side // 4, width=2)

        # white_fill button
        pygame.draw.circle(self.surface, color=(255, 255, 255),
                           center=self.white_fill_tool_center,
                           radius=self.cells_side // 2)
        pygame.draw.circle(self.surface, color=(0, 0, 0),
                           center=self.white_fill_tool_center,
                           radius=self.cells_side // 4, width=2)

        # blackout button
        pygame.draw.circle(self.surface, color=(0, 0, 0),
                           center=self.blackout_tool_center,
                           radius=self.cells_side // 2)
        x, y = self.blackout_tool_center
        pygame.draw.line(self.surface, color=(255, 0, 0), start_pos=(x, y-9),
                         end_pos=self.blackout_tool_center, width=3)
        pygame.draw.circle(self.surface, color=(255, 0, 0), radius=2,
                           center = (x, y + self.cells_side // 4))

        # whiteout button
        x, y = self.whiteout_tool_center
        pygame.draw.circle(self.surface, color=(255, 255, 255),
                           center=self.whiteout_tool_center,
                           radius=self.cells_side // 2)
        pygame.draw.line(self.surface, color=(255, 0, 0), start_pos=(x, y-9),
                         end_pos=self.whiteout_tool_center, width=3)
        pygame.draw.circle(self.surface, color=(255, 0, 0), radius=2,
                           center = (x, y + self.cells_side // 4))

        # checker button
        for r in range(2, self.cells_side // 2, 4):
            pygame.draw.circle(self.surface, color=(255, 255, 255),
                           center=self.checker_tool_center, radius=r, width=1)
        for r in range(0, self.cells_side // 2 + 2, 4):
            pygame.draw.circle(self.surface, color=(0, 0, 0),
                           center=self.checker_tool_center, radius=r, width=1)

        # tool highlight
        x, y = self.tool_dict[self.tool_mode]
        x += 8
        highlight_points = [(x, y), (x+14, y+7), (x+14, y-7)]
        pygame.draw.polygon(self.surface, (0, 240, 240), highlight_points)

        # grid and minigrid rendering
        for row in range(self.cells_side):
            for col in range(self.cells_side):
                rect = (self.border + col * self.square,
                        self.border + row * self.square,
                        self.square, self.square)
                if self.grid[row][col]:
                    fill = (0, 0, 0)
                    border = False
                    mrect = (self.mini_left + col, self.mini_top + row, 1, 1)
                    pygame.draw.rect(self.surface, color=(0, 0, 0),
                                     rect=mrect)
                else:
                    fill = (255, 255, 255)
                    border = True
                pygame.draw.rect(self.surface, color=fill,
                                 rect=rect)
                if border:
                    pygame.draw.rect(self.surface, color=(0, 0, 0),
                                     rect=rect, width=1)

    def get_grid_coord(self, pos: Tuple[int, int]) ->Optional[Tuple[int, int]]:
        """
        Takes click position and returns corresponding coordinates for grid

        Input:
            pos (Tuple(int, int): coordinate position of mouse in window

        Returns(Tuple(int, int): (row, col) in grid or none if out of range
        """
        side_len = (self.window - 2 * self.border) // len(self.grid)
        x, y = pos
        col = (x - self.border) // side_len
        row = (y - self.border) // side_len
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            return (row, col)
        return None

    def make_black(self, coord: Tuple[int, int]) -> None:
        """
        Darkens the cell in the grid that corresponds to the given coordinates

        Input:
            coord (Tuple(int, int): coordinate position in grid as (row, col)

        Returns: nothing
        """
        i, j = coord
        self.grid[i][j] = True

    def make_white(self, coord: Tuple[int, int]) -> None:
        """
        Whitens the cell in the grid that corresponds to the given coordinates

        Input:
            coord (Tuple(int, int): coordinate position in grid as (row, col)

        Returns: nothing
        """
        i, j = coord
        self.grid[i][j] = False

    def make_checkered(self) -> None:
        """
        Turns grid into a checkered pattern

        Inputs: None beyond self

        Returns: nothing
        """
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                if r % 2 == c % 2:
                    self.grid[r][c] = True
                else:
                    self.grid[r][c] = False

    def tool_change(self, pos: Tuple[int, int]) -> None:
        """
        Takes click position and changes tool if appropriate area was clicked

        Input:
            pos (Tuple(int, int): coordinate position of mouse in window

        Returns: nothing
        """
        for tool, center in self.tool_dict.items():
            if self.distance(pos, center) <= self.cells_side // 2:
                self.tool_mode = tool
                break

    def distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """
        Calculates the distance between two points

        Inputs:
            p1, p2 (Tuple(int)): pixel coordinates of the two points

        Returns (float): pixelwise distance between the two points
        """
        x1, y1 = p1
        x2, y2 = p2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Handle any other event types here
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    grid_pos = self.get_grid_coord(event.pos)

                    if grid_pos:
                        #change grid based on parameter
                        if self.tool_mode == 'black':
                            self.make_black(grid_pos)
                        elif self.tool_mode == 'white':
                            self.make_white(grid_pos)
                        elif self.tool_mode == 'fill':
                            flood_fill(self.grid, grid_pos)
                        elif self.tool_mode == 'white_fill':
                            white_flood_fill(self.grid, grid_pos)
                        elif self.tool_mode == 'blackout':
                            self.grid =  [[True] * self.cells_side \
                                          for i in range(self.cells_side)]
                        elif self.tool_mode == 'whiteout':
                            self.grid =  [[False] * self.cells_side \
                                          for i in range(self.cells_side)]
                        elif self.tool_mode == 'checker':
                            self.make_checkered()
                    else:
                        self.tool_change(event.pos)

            # Update the display
            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)


if __name__ == "__main__":
    BitEdit()
