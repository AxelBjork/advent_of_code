#!/usr/bin/env python3
import sys
from utils.inputs import read_lines, read_text

def parse_input(input_data):
    ranges = []
    ids = []
    parsing_ranges = True
    
    for line in input_data:
        line = line.strip()
        if not line:
            if parsing_ranges:
                parsing_ranges = False
            continue
            
        if parsing_ranges:
            try:
                start, end = map(int, line.split('-'))
                ranges.append((start, end))
            except ValueError:
                continue
        else:
            try:
                ids.append(int(line))
            except ValueError:
                continue
    return ranges, ids

def solve_part1(input_data):
    ranges, ids = parse_input(input_data)
    
    fresh_count = 0
    for ingredient_id in ids:
        is_fresh = False
        for start, end in ranges:
            if start <= ingredient_id <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1
            
    return fresh_count

def merge_intervals(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    for current_start, current_end in intervals[1:]:
        last_start, last_end = merged[-1]
        
        if current_start <= last_end + 1: # +1 because intervals are inclusive e.g. 3-5 and 6-10 are contiguous
            # Technically the problem says "overlapping", usually that means intersection.
            # But "fresh ranges" could be contiguous.
            # If 3-5 (3,4,5) and 6-8 (6,7,8), then 3-8 is one block?
            # Question says: "ranges can also overlap".
            # Standard interval merging: overlap if start <= last_end.
            # However, for integer ranges count, if we have 3-5 and 6-8, that's 3,4,5,6,7,8.
            # If we don't merge them, we sum lengths: (5-3+1) + (8-6+1) = 3 + 3 = 6. Correct.
            # So standard merge is fine for overlap. 
            # If we interpret "overlapping" strictly:
            # 3-5 and 5-7 -> merge to 3-7.
            # 3-5 and 6-8 -> discrete.
            
            # Let's stick to strict overlap logic for merging: current_start <= last_end.
            # BUT, wait. If we have 1-2 and 3-4. Total count is 4.
            # If we don't merge, sum is 2+2=4.
            # If we have 1-3 and 2-4. Merge to 1-4. Count is 4.
            # Unmerged sum would be 3+3=6 (double counting).
            # So we MUST merge overlaps.
            
            # What about 1-2 and 3-4? These are adjacent.
            # Should we merge them?
            # 1-2 covers {1, 2}. 3-4 covers {3, 4}.
            # Union is {1, 2, 3, 4}. Count 4.
            # Merged 1-4 covers {1, 2, 3, 4}. Count 4.
            # So merging adjacent intervals is safe and efficient for counting.
            # Overlap condition: current_start <= last_end + 1
            
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))
            
    return merged

def solve_part2(input_data):
    ranges, _ = parse_input(input_data)
    merged_ranges = merge_intervals(ranges)
    
    total_count = 0
    for start, end in merged_ranges:
        total_count += (end - start + 1)
        
    return total_count

if __name__ == "__main__":
    print("--- Day 5: Cafeteria ---")
    
    # Verification
    example_input = [
        "3-5",
        "10-14",
        "16-20",
        "12-18",
        "",
        "1",
        "5",
        "8",
        "11",
        "17",
        "32"
    ]
    
    print("--- Verification ---")
    p1_ex = solve_part1(example_input)
    print(f"Part 1 Example: {p1_ex} (Expected 3)")
    
    p2_ex = solve_part2(example_input)
    print(f"Part 2 Example: {p2_ex} (Expected 14)")
    
    if p1_ex == 3 and p2_ex == 14:
        print("\n--- Solving Real Input ---")
        input_data = read_lines(5)
        print(f"Part 1 Answer: {solve_part1(input_data)}")
        print(f"Part 2 Answer: {solve_part2(input_data)}")
    else:
        print(f"Verification FAILED.")
