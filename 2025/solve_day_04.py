#!/usr/bin/env python3
import sys
from utils.inputs import read_lines, read_text

def count_neighbors(r, c, grid, rows, cols):
    count = 0
    # 8 directions
    deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] == '@':
                count += 1
    return count

def solve_part1(input_data):
    grid = [list(line.strip()) for line in input_data if line.strip()]
    if not grid:
        return 0
        
    rows = len(grid)
    cols = len(grid[0])
    
    accessible_count = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                # Check neighbors
                neighbors = count_neighbors(r, c, grid, rows, cols)
                if neighbors < 4:
                    accessible_count += 1
                    
    return accessible_count

def solve_part2(input_data):
    # Create a fresh grid for Part 2 simulation
    grid = [list(line.strip()) for line in input_data if line.strip()]
    if not grid:
        return 0
        
    rows = len(grid)
    cols = len(grid[0])
    
    total_removed = 0
    
    while True:
        to_remove = []
        
        # Identify all accessible paper rolls in current state
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    neighbors = count_neighbors(r, c, grid, rows, cols)
                    if neighbors < 4:
                        to_remove.append((r, c))
        
        if not to_remove:
            break
            
        # Remove them
        total_removed += len(to_remove)
        for r, c in to_remove:
            grid[r][c] = '.' # Mark as empty
            
    return total_removed

if __name__ == "__main__":
    print("--- Day 4: Printing Department ---")
    
    # Verification with example
    example_input = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@."
    ]
    
    print("--- Verification ---")
    p1_ex = solve_part1(example_input)
    print(f"Part 1 Example: {p1_ex} (Expected 13)")
    
    p2_ex = solve_part2(example_input)
    print(f"Part 2 Example: {p2_ex} (Expected 43)")
    
    if p1_ex == 13 and p2_ex == 43:
        print("\n--- Solving Real Input ---")
        input_data = read_lines(4)
        print(f"Part 1 Answer: {solve_part1(input_data)}")
        print(f"Part 2 Answer: {solve_part2(input_data)}")
    else:
        print("\nVerification FAILED. Stopping.")
