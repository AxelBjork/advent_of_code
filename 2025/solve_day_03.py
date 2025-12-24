#!/usr/bin/env python3
import os

def find_max_subsequence(line, target_length):
    line = line.strip()
    if len(line) < target_length:
        return 0 # Or handle error appropriately
        
    current_idx = 0
    result = ""
    
    # We need to build a number of 'target_length' digits.
    # For each position k (from target_length down to 1):
    for k in range(target_length, 0, -1):
        # We must leave at least (k - 1) digits after the one we pick now.
        # So we can search up to index: len(line) - k
        # In Python slice [start:end], end is exclusive, so we use len(line) - (k - 1)
        search_end = len(line) - (k - 1)
        
        # Search range
        chunk = line[current_idx : search_end]
        
        # Find max digit - strictly looking for '9' first is optimization
        # We want the First occurrence of the maximum digit in this chunk.
        max_d = '0'
        max_rel_idx = -1
        
        for i, char in enumerate(chunk):
            if char > max_d:
                max_d = char
                max_rel_idx = i
                if char == '9': # Optimization
                    break
                    
        result += max_d
        current_idx += max_rel_idx + 1
        
    return int(result)

def solve_part1(input_path):
    total = 0
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                total += find_max_subsequence(line, 2)
    return total

def solve_part2(input_path):
    total = 0
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                total += find_max_subsequence(line, 12)
    return total

def test_examples():
    examples_p1 = [
        ("987654321111111", 98),
        ("811111111111119", 89),
        ("234234234234278", 78),
        ("818181911112111", 92)
    ]
    
    print("--- Testing Part 1 Examples ---")
    for line, expected in examples_p1:
        res = find_max_subsequence(line, 2)
        print(f"Input: {line[:15]}... -> Got: {res}, Expected: {expected}")
        if res != expected:
            print(f"FAIL: Expected {expected}, got {res}")

    examples_p2 = [
        ("987654321111111", 987654321111),
        ("811111111111119", 811111111119),
        ("234234234234278", 434234234278),
        ("818181911112111", 888911112111)
    ]
    print("\n--- Testing Part 2 Examples ---")
    p2_total = 0
    for line, expected in examples_p2:
        res = find_max_subsequence(line, 12)
        print(f"Input: {line[:15]}... -> Got: {res}, Expected: {expected}")
        if res != expected:
            print(f"FAIL: Expected {expected}, got {res}")
        p2_total += res
    
    expected_p2_total = 3121910778619
    if p2_total == expected_p2_total:
        print(f"Part 2 Example Total Verified: {p2_total}")
    else:
        print(f"Part 2 Example Total FAIL: Expected {expected_p2_total}, got {p2_total}")

if __name__ == "__main__":
    input_path = 'inputs/day_03.txt'
    
    test_examples()
    
    if os.path.exists(input_path):
        print("\n--- Solving Real Input ---")
        p1 = solve_part1(input_path)
        print(f"Part 1 Total: {p1}")
        p2 = solve_part2(input_path)
        print(f"Part 2 Total: {p2}")
    else:
        print(f"\n{input_path} not found, skipping real input.")
