#!/usr/bin/env python3
import sys
import collections
import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from utils.inputs import read_lines

def solve_machine(line):
    # Parse target: [...]
    match_target = re.search(r'\[([.#]+)\]', line)
    if not match_target:
        return 0
    target_str = match_target.group(1)
    num_lights = len(target_str)
    
    target_mask = 0
    for i, char in enumerate(target_str):
        if char == '#':
            target_mask |= (1 << i)
            
    # Parse buttons: (...)
    # There can be multiple buttons.
    # We can split by ')' to get chunks, then find (...) in each.
    # Or just find all (...) matches.
    
    # The format is [...] (...) (...) ... {...}
    # Let's extract all (...) parts.
    
    # Regex for buttons: \(([\d,]+)\)
    button_matches = re.findall(r'\(([\d,]+)\)', line)
    
    buttons = []
    for match in button_matches:
        parts = match.split(',')
        mask = 0
        for p in parts:
            if p.strip():
                try:
                    bit = int(p.strip())
                    if bit < num_lights:
                        mask |= (1 << bit)
                except ValueError:
                    pass
        buttons.append(mask)
        
    # BFS
    # State is current configuration (integer bitmask)
    start_state = 0
    queue = collections.deque([(start_state, 0)])
    visited = {start_state}
    
    while queue:
        state, steps = queue.popleft()
        
        if state == target_mask:
            return steps
        
        for btn_mask in buttons:
            next_state = state ^ btn_mask
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))
                
    return 0 # Should effectively not happen based on problem, or unsolvable
    
def solve_machine_part2(line):
    # Parse joltage target: {...}
    match_joltage = re.search(r'\{([\d,]+)\}', line)
    if not match_joltage:
        return 0
    target_parts = [int(p) for p in match_joltage.group(1).split(',')]
    b = np.array(target_parts)
    num_counters = len(b)
    
    # Parse buttons: (...)
    button_matches = re.findall(r'\(([\d,]+)\)', line)
    
    A_cols = []
    for match in button_matches:
        parts = match.split(',')
        col = np.zeros(num_counters)
        for p in parts:
            if p.strip():
                try:
                    idx = int(p.strip())
                    if idx < num_counters:
                        col[idx] = 1
                except ValueError:
                    pass
        A_cols.append(col)
        
    if not A_cols:
        return 0
        
    A = np.column_stack(A_cols)
    num_buttons = A.shape[1]
    
    # ILP: min sum(x) s.t. Ax = b, x >= 0, integer
    c = np.ones(num_buttons)
    
    # scipy.optimize.milp works with Bounds and Constraints
    # variable x
    
    # Constraints: Ax = b
    # LinearConstraint(A, lb=b, ub=b)
    
    # Bounds: x >= 0
    # Bounds(lb=0, ub=np.inf)
    bounds = Bounds(lb=np.zeros(num_buttons), ub=np.inf)
    
    # Integrality: 1 (integer)
    integrality = np.ones(num_buttons)
    
    res = milp(c=c, constraints=LinearConstraint(A, lb=b, ub=b), 
               integrality=integrality, bounds=bounds)
               
    if res.success:
        # Round the result since it's floating point, but should be integer close
        return int(np.round(res.x).sum())
    else:
        # Fallback? Maybe unfeasible.
        return 0

def solve(input_data):
    total_presses = 0
    machine_count = 0
    for line in input_data:
        line = line.strip()
        if not line:
            continue
        try:
            presses = solve_machine(line)
            total_presses += presses
            machine_count += 1
        except Exception as e:
            pass # Ignore errors for now
            
    return total_presses

def solve_part2(input_data):
    total_presses = 0
    for line in input_data:
        line = line.strip()
        if not line:
            continue
        try:
            presses = solve_machine_part2(line)
            total_presses += presses
        except Exception as e:
            print(f"Part 2 Error on line: {line}\n{e}")
            
    return total_presses

if __name__ == "__main__":
    print("--- Day 10: Factory ---")
    
    # Verification
    example_input = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    ]
    
    # Expected Part 1: 7
    # Expected Part 2: 33
    
    print(f"Part 1 Example: {solve(example_input)}")
    
    try:
        print(f"Part 2 Example: {solve_part2(example_input)}")
        
        input_data = read_lines(10)
        print(f"Part 1 Result: {solve(input_data)}")
        print(f"Part 2 Result: {solve_part2(input_data)}")
        
    except Exception as e:
        print(f"Execution Error: {e}")

