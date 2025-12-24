#!/usr/bin/env python3
import sys
import collections
from utils.inputs import read_lines

# Increase recursion depth just in case, though graph shouldn't be that deep
sys.setrecursionlimit(20000)

def solve(input_data):
    adj = collections.defaultdict(list)
    
    for line in input_data:
        line = line.strip()
        if not line:
            continue
        
        # format: "node: out1 out2 out3"
        parts = line.split(':')
        if len(parts) != 2:
            continue
            
        src = parts[0].strip()
        dests = parts[1].strip().split()
        
        for dst in dests:
            adj[src].append(dst)
            
    memo = {}
    
    def count_paths(node, target):
        # Base case
        if node == target:
            return 1
            
        # Check memo
        state = (node, target)
        if state in memo:
            return memo[state]
        
        # Dead end
        if node not in adj:
            return 0
            
        total = 0
        for neighbor in adj[node]:
            total += count_paths(neighbor, target)
            
        memo[state] = total
        return total

    # Part 1
    part1 = count_paths('you', 'out')
    
    # Part 2
    # svr -> out visiting dac and fft
    # Order 1: svr -> dac -> fft -> out
    # Order 2: svr -> fft -> dac -> out
    
    # Check if necessary nodes exist to avoid errors on example 1 which lacks them
    needed = ['svr', 'dac', 'fft', 'out']
    if not all(n in adj or any(n in v for v in adj.values()) for n in needed):
        return part1, 0

    # Calculate Path A: svr -> dac -> fft -> out
    p1_a = count_paths('svr', 'dac')
    p2_a = count_paths('dac', 'fft')
    p3_a = count_paths('fft', 'out')
    total_a = p1_a * p2_a * p3_a
    
    # Calculate Path B: svr -> fft -> dac -> out
    p1_b = count_paths('svr', 'fft')
    p2_b = count_paths('fft', 'dac')
    p3_b = count_paths('dac', 'out')
    total_b = p1_b * p2_b * p3_b
    
    return part1, total_a + total_b

if __name__ == "__main__":
    print("--- Day 11: Reactor ---")
    
    # Verification
    example_input = [
        "aaa: you hhh",
        "you: bbb ccc",
        "bbb: ddd eee",
        "ccc: ddd eee fff",
        "ddd: ggg",
        "eee: out",
        "fff: out",
        "ggg: out",
        "hhh: ccc fff iii",
        "iii: out"
    ]
    
    # Example 1 only has 'you' -> 'out' (Part 1)
    p1_ex1, p2_ex1 = solve(example_input)
    print(f"Example 1 Part 1 Result: {p1_ex1}")
    
    example_input_2 = [
        "svr: aaa bbb",
        "aaa: fft",
        "fft: ccc",
        "bbb: tty",
        "tty: ccc",
        "ccc: ddd eee",
        "ddd: hub",
        "hub: fff",
        "eee: dac",
        "dac: fff",
        "fff: ggg hhh",
        "ggg: out",
        "hhh: out"
    ]
    
    # Example 2 for Part 2
    # Verify Part 2 logic on Example 2
    # Note: Example 2 might not have 'you' -> 'out' path, so Part 1 result might be 0 or irrelevant
    _, p2_ex2 = solve(example_input_2)
    print(f"Example 2 Part 2 Result: {p2_ex2}") # Expected 2

    if p1_ex1 == 5 and p2_ex2 == 2:
        print("Examples Verified!")
        input_data = read_lines(11)
        p1, p2 = solve(input_data)
        print(f"Part 1 Result: {p1}")
        print(f"Part 2 Result: {p2}")
    else:
        print(f"Verification FAILED. Ex1 P1: {p1_ex1} (want 5), Ex2 P2: {p2_ex2} (want 2)")
