#!/usr/bin/env python3
import sys
from utils.inputs import read_lines, read_text

def solve_part1(input_data):
    grid = [line.strip() for line in input_data if line.strip()]
    if not grid:
        return 0
        
    rows = len(grid)
    cols = len(grid[0])
    
    # Find start position S
    active_beams = set()
    start_row = -1
    for r in range(rows):
        if 'S' in grid[r]:
            c = grid[r].index('S')
            active_beams.add(c)
            start_row = r
            break
            
    if start_row == -1:
        return 0
        
    total_splits = 0
    current_row = start_row
    
    while current_row < rows - 1 and active_beams:
        next_row = current_row + 1
        next_beams = set()
        
        for c in active_beams:
            cell = grid[next_row][c]
            
            if cell == '.':
                next_beams.add(c)
            elif cell == '^':
                total_splits += 1
                if c - 1 >= 0:
                    next_beams.add(c - 1)
                if c + 1 < cols:
                    next_beams.add(c + 1)
            elif cell == 'S':
                next_beams.add(c)
            else:
                next_beams.add(c)
                
        active_beams = next_beams
        current_row += 1
        
    return total_splits

def solve_part2(input_data):
    grid = [line.strip() for line in input_data if line.strip()]
    if not grid:
        return 0
        
    rows = len(grid)
    cols = len(grid[0])
    
    # Timeline counts: col -> count
    timeline_counts = {}
    start_row = -1
    for r in range(rows):
        if 'S' in grid[r]:
            c = grid[r].index('S')
            timeline_counts[c] = 1
            start_row = r
            break
            
    if start_row == -1:
        return 0
        
    completed_timelines = 0
    current_row = start_row
    
    while current_row < rows - 1 and timeline_counts:
        next_row = current_row + 1
        next_counts = {}
        
        for c, count in timeline_counts.items():
            cell = grid[next_row][c]
            
            if cell == '.':
                # Beam continues
                next_counts[c] = next_counts.get(c, 0) + count
            elif cell == '^':
                # Splits
                # Left
                if c - 1 >= 0:
                    next_counts[c-1] = next_counts.get(c-1, 0) + count
                else:
                    # Exits left
                    completed_timelines += count
                    
                # Right
                if c + 1 < cols:
                    next_counts[c+1] = next_counts.get(c+1, 0) + count
                else:
                    # Exits right
                    completed_timelines += count
                    
            elif cell == 'S':
                next_counts[c] = next_counts.get(c, 0) + count
            else:
                next_counts[c] = next_counts.get(c, 0) + count
                
        timeline_counts = next_counts
        current_row += 1
        
    # Add timelines that reached the bottom
    completed_timelines += sum(timeline_counts.values())
    
    return completed_timelines

if __name__ == "__main__":
    print("--- Day 7: Laboratories ---")
    
    # Verification
    example_input = [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "..............."
    ]
    
    print("--- Verification ---")
    p1_ex = solve_part1(example_input)
    print(f"Part 1 Example: {p1_ex} (Expected 21)")
    
    p2_ex = solve_part2(example_input)
    print(f"Part 2 Example: {p2_ex} (Expected 40)")
    
    if p1_ex == 21 and p2_ex == 40:
        print("\n--- Solving Real Input ---")
        input_data = read_lines(7)
        print(f"Part 1 Answer: {solve_part1(input_data)}")
        print(f"Part 2 Answer: {solve_part2(input_data)}")
    else:
        print(f"Verification FAILED. Stopping.")
