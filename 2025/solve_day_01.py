#!/usr/bin/env python3
import sys
from utils.inputs import read_lines

def solve_part1(lines):
    current_pos = 50
    zero_count = 0
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        direction = line[0]
        amount = int(line[1:])
        
        if direction == 'L':
            current_pos = (current_pos - amount) % 100
        elif direction == 'R':
            current_pos = (current_pos + amount) % 100
            
        if current_pos == 0:
            zero_count += 1
            
    return zero_count

def solve_part2(lines):
    current_pos = 50
    total_zeros = 0
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        direction = line[0]
        amount = int(line[1:])
        
        if direction == 'R':
            end_val = current_pos + amount
            zeros_passed = end_val // 100
            total_zeros += zeros_passed
            current_pos = end_val % 100
            
        elif direction == 'L':
            start_val = current_pos
            end_val = current_pos - amount
            B = start_val - 1
            A = end_val
            count = (B // 100) - ((A - 1) // 100)
            total_zeros += count
            current_pos = end_val % 100
            
    return total_zeros

if __name__ == "__main__":
    print("--- Day 1: Secret Entrance ---")
    input_data = read_lines(1)
    
    print(f"Part 1 Answer: {solve_part1(input_data)}")
    print(f"Part 2 Answer: {solve_part2(input_data)}")
