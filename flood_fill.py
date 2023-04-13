"""
helper functions for flooding in biteditor
"""

from typing import List, Tuple, Dict, Optional

def flood_fill(grid: List[List[bool]], start: Tuple[int, int]) -> None:
    """
    "Flood fill" (the paint-bucket tool) a grid of booleans
    Changes a cell in the grid to black (True) and its neighboring cell, and
    their neighbors, stopping when encountering an already-black (True) cell in
    a given direction
    Directions are N, E, S, and W, but not diagonal

    Inputs:
        grid (List[List[bool]]): two-dimensional grid of boolean cells
        start (Tuple[int, int]): the coordinates of the starting cell
    
    Returns: nothing
        """
    i, j = start
    if grid[i][j]:
        return
    else:
        grid[i][j] = True

    if i > 0:
        flood_fill(grid, (i - 1, j))
    if j > 0:
        flood_fill(grid, (i, j - 1))
    if i < len(grid) - 1:
        flood_fill(grid, (i + 1, j))
    if j < len(grid[0]) - 1:
        flood_fill(grid, (i, j + 1))


def white_flood_fill(grid: List[List[bool]], start: Tuple[int, int]) -> None:
    """
    same as flood_fill, but with reversed color scheme
    
    Inputs:
        grid (List[List[bool]]): two-dimensional grid of boolean cells
        start (Tuple[int, int]): the coordinates of the starting cell
    
    Returns: nothing
    """
    i, j = start
    if not grid[i][j]:
        return
    else:
        grid[i][j] = False

    if i > 0:
        white_flood_fill(grid, (i - 1, j))
    if j > 0:
        white_flood_fill(grid, (i, j - 1))
    if i < len(grid) - 1:
        white_flood_fill(grid, (i + 1, j))
    if j < len(grid[0]) - 1:
        white_flood_fill(grid, (i, j + 1))