#!/usr/bin/env python3
import sys
from utils.inputs import read_text

def is_invalid(n):
    s = str(n)
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]

def solve_part1(input_str):
    ranges = input_str.strip().replace('\n', '').split(',')
    total_invalid_sum = 0
    
    for r in ranges:
        if not r: continue
        start, end = map(int, r.split('-'))
        for i in range(start, end + 1):
            if is_invalid(i):
                total_invalid_sum += i
                
    return total_invalid_sum

def is_invalid_part2(n):
    s = str(n)
    length = len(s)
    # Pattern length must be at least 1 and at most length/2
    # It must repeat at least twice (so length // pattern_len >= 2)
    for k in range(1, length // 2 + 1):
        if length % k == 0:
            repeats = length // k
            pattern = s[:k]
            if pattern * repeats == s:
                return True
    return False

def solve_part2(input_str):
    ranges = input_str.strip().replace('\n', '').split(',')
    total_invalid_sum = 0
    
    for r in ranges:
        if not r: continue
        start, end = map(int, r.split('-'))
        for i in range(start, end + 1):
            if is_invalid_part2(i):
                total_invalid_sum += i
                
    return total_invalid_sum

if __name__ == "__main__":
    print("--- Day 2: Gift Shop ---")
    input_data = read_text(2)
    
    print(f"Part 1 Answer: {solve_part1(input_data)}")
    print(f"Part 2 Answer: {solve_part2(input_data)}")
