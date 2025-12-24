#!/usr/bin/env python3
import sys
from utils.inputs import read_lines, read_text

def get_problem_blocks(lines):
    # Ensure all lines are equal length by padding with spaces
    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    
    # Identify empty columns (columns containing only spaces)
    empty_cols = []
    for c in range(max_len):
        is_empty = True
        for line in padded_lines:
            if line[c] != ' ':
                is_empty = False
                break
        if is_empty:
            empty_cols.append(c)
            
    # Group ranges of non-empty columns
    problem_ranges = []
    start = 0
    # Add a sentinel empty column at the end to close the last range
    boundaries = empty_cols + [max_len]
    
    current_start = 0
    unique_boundaries = sorted(list(set(boundaries)))
    
    blocks = []
    for boundary in unique_boundaries:
        if boundary > current_start:
            # We found a block from current_start to boundary
            # Extract block
            block_lines = [line[current_start:boundary] for line in padded_lines]
            blocks.append(block_lines)
        current_start = boundary + 1
    return blocks

def solve_part1(input_data):
    lines = [line.replace('\n', '') for line in input_data if line.strip('\n')]
    if not lines:
        return 0
        
    blocks = get_problem_blocks(lines)
    total_result = 0
    
    for block_lines in blocks:
        operator = None
        operator_row_idx = -1
        
        # Find operator (search from bottom up)
        for r in range(len(block_lines) - 1, -1, -1):
            row_content = block_lines[r].strip()
            if not row_content:
                continue
            if row_content in ['+', '*']:
                operator = row_content
                operator_row_idx = r
                break
        
        if operator:
            vals = []
            # Parse horizontal numbers above operator
            for nr in range(operator_row_idx):
                num_str = block_lines[nr].strip()
                if num_str:
                    try:
                        vals.append(int(num_str))
                    except ValueError:
                        pass
            
            if vals:
                res = vals[0]
                for v in vals[1:]:
                    if operator == '+':
                        res += v
                    elif operator == '*':
                        res *= v
                total_result += res
                
    return total_result

def solve_part2(input_data):
    lines = [line.replace('\n', '') for line in input_data if line.strip('\n')]
    if not lines:
        return 0
        
    blocks = get_problem_blocks(lines)
    total_result = 0
    
    for block_lines in blocks:
        operator = None
        operator_row_idx = -1
        
        # Find operator (search from bottom up)
        for r in range(len(block_lines) - 1, -1, -1):
            row_content = block_lines[r].strip()
            if not row_content:
                continue
            if row_content in ['+', '*']:
                operator = row_content
                operator_row_idx = r
                break
        
        if operator:
            vals = []
            # Parse vertical numbers above operator
            # Iterate columns
            width = len(block_lines[0])
            for c in range(width):
                col_str = ""
                for r in range(operator_row_idx):
                    char = block_lines[r][c]
                    if char != ' ':
                        col_str += char
                
                if col_str:
                    try:
                        vals.append(int(col_str))
                    except ValueError:
                        pass
            
            if vals:
                # Part 2 says "Reading the problems right-to-left one column at a time"
                # This affects the order of operations?
                # "The rightmost problem is 4 + 431 + 623 = 1058"
                # Addition is commutative, so order doesn't matter for +
                # Assume multiplication is also commutative/associative for these problems (all * or all +)?
                # "each problem has a group of numbers that need to be either added (+) or multiplied (*) together."
                # This implies a single operation type per problem. So order doesn't matter for * either.
                # Just collect all numbers and apply op.
                
                res = vals[0]
                for v in vals[1:]:
                    if operator == '+':
                        res += v
                    elif operator == '*':
                        res *= v
                total_result += res
                
    return total_result

if __name__ == "__main__":
    print("--- Day 6: Trash Compactor ---")
    
    # Verification
    example_input = [
        "123 328  51 64 ",
        " 45 64  387 23 ",
        "  6 98  215 314",
        "*   +   *   +  "
    ]
    
    print("--- Verification ---")
    p1_ex = solve_part1(example_input)
    print(f"Part 1 Example: {p1_ex} (Expected 4277556)")
    
    p2_ex = solve_part2(example_input)
    print(f"Part 2 Example: {p2_ex} (Expected 3263827)")
    
    if p1_ex == 4277556 and p2_ex == 3263827:
        print("\n--- Solving Real Input ---")
        input_data = read_lines(6)
        print(f"Part 1 Answer: {solve_part1(input_data)}")
        print(f"Part 2 Answer: {solve_part2(input_data)}")
    else:
        print(f"Verification FAILED.")
