#!/usr/bin/env python3
import sys
import collections

# --- Shape Logic ---

def normalize_shape(grid):
    # Convert grid to set of (r, c)
    # And shift to (0,0)
    coords = set()
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == '#':
                coords.add((r, c))
    return coords

def get_dims(coords):
    if not coords:
        return 0, 0
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return max_r + 1, max_c + 1

def transform_shape(coords, method):
    # Methods: 0-3 rot90, 4-7 flip+rot90
    # method < 4: rotate 90 * method
    # method >= 4: flip then rotate
    
    # 0: 0 deg
    # 1: 90 deg
    # 2: 180 deg
    # 3: 270 deg
    # 4: flip H
    # 5: flip H + 90
    # ...
    
    curr = list(coords)
    
    # Flip
    if method >= 4:
        # Flip horizontal (around y-axis, invert c)
        # But we need to re-normalize later, so just negate c
        curr = [(r, -c) for r, c in curr]
        
    rotations = method % 4
    for _ in range(rotations):
        # Rotate 90 deg clockwise: (r, c) -> (c, -r)
        curr = [(c, -r) for r, c in curr]
        
    # Normalize to bounding box at 0,0
    if not curr:
        return set()
        
    min_r = min(r for r, c in curr)
    min_c = min(c for r, c in curr)
    
    final_set = set()
    for r, c in curr:
        final_set.add((r - min_r, c - min_c))
        
    return final_set

class Shape:
    def __init__(self, idx, grid_lines):
        self.idx = idx
        self.base_coords = normalize_shape(grid_lines)
        self.area = len(self.base_coords)
        
        # Precompute variations
        unique_vars = []
        seen = set()
        
        for m in range(8):
            var_coords = transform_shape(self.base_coords, m)
            # Create a canonical hashable representation (sorted tuple)
            canon = tuple(sorted(list(var_coords)))
            if canon not in seen:
                seen.add(canon)
                h, w = get_dims(var_coords)
                # Store as (h, w, coords_list)
                # coords_list sorted for consistent iteration or just list
                unique_vars.append({
                    'h': h,
                    'w': w,
                    'coords': list(var_coords)
                })
        
        # Sort variations by some criteria? Maybe largest dimension first?
        # Actually random order is fine, but fewer variations is better.
        self.variations = unique_vars

import multiprocessing
import signal

def solve_region_wrapper(args):
    W, H, pieces, shapes_data = args
    # Reconstruct shapes? No, we need fresh cache or something.
    # Just pass shapes.
    
    # Timeout logic: signal?
    # Or just simple backtracking step limit?
    # Signal only works in main thread usually.
    # We can use a step counter in backtracking.
    
    # Instantiate solver
    # We need to adapt solve_region to use a step limit
    pass 

# ... (Previous shape/bitmask code stays, we need to inject step limit)


def get_bitmask(coords, W):
    mask = 0
    for r, c in coords:
        # bit index: r*W + c
        mask |= (1 << (r * W + c))
    return mask

def solve_region_with_limit(W, H, pieces, shapes, max_steps=50000):
    # Same code as solve_region but with step decrement
    n_pieces = len(pieces)
    
    var_cache = {}
    piece_vars = []
    
    # ... (Re-implement precompute for isolation) ...
    for idx in pieces:
        if idx not in var_cache:
            vars_for_shape = []
            shape = shapes[idx]
            for var in shape.variations:
                if var['h'] <= H and var['w'] <= W:
                    mask = get_bitmask(var['coords'], W)
                    vars_for_shape.append({
                        'h': var['h'],
                        'w': var['w'],
                        'mask': mask
                    })
            var_cache[idx] = vars_for_shape
        piece_vars.append(var_cache[idx])
        
    board_full_mask = (1 << (W * H)) - 1
    
    min_remaining_area = [0] * n_pieces
    if n_pieces > 0:
        min_remaining_area[-1] = shapes[pieces[-1]].area
        for i in range(n_pieces - 2, -1, -1):
            min_remaining_area[i] = min(min_remaining_area[i+1], shapes[pieces[i]].area)
            
    # Flood fill helper
    left_edge_mask = 0
    right_edge_mask = 0
    for r in range(H):
        left_edge_mask |= (1 << (r * W))
        right_edge_mask |= (1 << (r * W + W - 1))
        
    def get_components_loss(current_grid_mask, min_size):
        empty = (~current_grid_mask) & board_full_mask
        if empty == 0: return 0
        visited = 0
        lost_area = 0
        while True:
            remaining = empty & (~visited)
            if remaining == 0: break
            start_bit = remaining & (-remaining)
            comp = start_bit
            while True:
                left = (comp >> 1) & (~right_edge_mask)
                right = (comp << 1) & (~left_edge_mask)
                up = comp >> W
                down = comp << W
                new_comp = comp | left | right | up | down
                new_comp &= empty
                if new_comp == comp: break
                comp = new_comp
            visited |= comp
            if bin(comp).count('1') < min_size:
                lost_area += bin(comp).count('1')
        return lost_area

    total_piece_area = sum(shapes[p].area for p in pieces)
    slack = (W * H) - total_piece_area
    
    steps = 0
    
    def backtrack(p_idx, grid_mask, start_pos=0):
        nonlocal steps
        steps += 1
        if steps > max_steps:
            return False # Timeout -> Fail
            
        if p_idx == n_pieces:
            return True
        
        # Check flood fill only periodically?
        if steps % 100 == 0:
            min_sz = min_remaining_area[p_idx]
            if get_components_loss(grid_mask, min_sz) > slack:
                return False
            
        vars_list = piece_vars[p_idx]
        current_start = 0
        if p_idx > 0 and pieces[p_idx] == pieces[p_idx-1]:
            current_start = start_pos
            
        limit = W * H
        for pos in range(current_start, limit):
            shifted_mask = 0 # Placeholder for scope
            
            # Inline vars iteration
            r, c = divmod(pos, W)
            for var in vars_list:
                if r + var['h'] > H: continue
                if c + var['w'] > W: continue
                
                shifted_mask = var['mask'] << pos
                if (grid_mask & shifted_mask) == 0:
                    if backtrack(p_idx + 1, grid_mask | shifted_mask, pos):
                        return True
        return False

    return backtrack(0, 0)

def worker(task_data):
    W, H, counts, shapes_dict = task_data
    # Reconstruct pieces
    pieces = []
    req_area = 0
    for s_idx, cnt in enumerate(counts):
        if cnt > 0:
            pieces.extend([s_idx] * cnt)
            req_area += cnt * shapes_dict[s_idx].area
    
    if req_area > W * H:
        return False
        
    pieces.sort(key=lambda idx: shapes_dict[idx].area, reverse=True)
    return solve_region_with_limit(W, H, pieces, shapes_dict)


def parse_input(lines):
    shapes = {}
    current_idx = None
    current_grid = []
    
    split_idx = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if 'x' in line and ':' in line and not line.endswith(':'):
            split_idx = i
            break
            
    shape_lines = lines[:split_idx]
    query_lines = lines[split_idx:]
    
    # Parse Shapes
    for line in shape_lines:
        line = line.strip()
        if not line:
            if current_idx is not None:
                shapes[current_idx] = Shape(current_idx, current_grid)
                current_grid = []
                current_idx = None
            continue
            
        if line.endswith(':'):
            current_idx = int(line[:-1])
            continue
            
        if current_idx is not None:
            current_grid.append(line)
            
    if current_idx is not None and current_grid:
        shapes[current_idx] = Shape(current_idx, current_grid)
        
    return shapes, query_lines

def solve_all(input_data):
    shapes, queries = parse_input(input_data)
    
    tasks = []
    for line in queries:
        line = line.strip()
        if not line: continue
        parts = line.split(':')
        dims = parts[0].split('x')
        W, H = int(dims[0]), int(dims[1])
        counts = list(map(int, parts[1].strip().split()))
        tasks.append((W, H, counts, shapes))
        
    with multiprocessing.Pool() as pool:
        results = pool.map(worker, tasks)
        
    return sum(results)

if __name__ == "__main__":
    print("--- Day 12: Christmas Tree Farm ---")
    
    # ... (Examples) ... 
    example_shapes = {
        0: Shape(0, ["###", "##.", "##."]),
        1: Shape(1, ["###", "##.", ".##"]),
        2: Shape(2, [".##", "###", "##."]),
        3: Shape(3, ["##.", "###", "##."]),
        4: Shape(4, ["###", "#..", "###"]),
        5: Shape(5, ["###", ".#.", "###"]),
    }
    
    # Manual check examples using worker
    print(f"Example 1: {worker((4, 4, [0,0,0,0,2,0], example_shapes))}")
    print(f"Example 2: {worker((12, 5, [1,0,1,0,2,2], example_shapes))}")
    print(f"Example 3: {worker((12, 5, [1,0,1,0,3,2], example_shapes))}") # Should be False
    
    print("Running on input file...")
    from utils.inputs import read_lines
    input_lines = read_lines(12)
    # Filter blank lines - NO, parser depends on them!
    # input_lines = [l for l in input_lines if l.strip()]
    
    # Note: solve_all parses again, but that's fine.
    try:
        result = solve_all(input_lines)
        print(f"Result: {result}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {type(e).__name__}: {e}")
