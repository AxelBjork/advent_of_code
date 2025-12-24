#!/usr/bin/env python3
import sys
from utils.inputs import read_lines

def solve(input_data):
    coords = []
    for line in input_data:
        line = line.strip()
        if not line:
            continue
        try:
            x, y = map(int, line.split(','))
            coords.append((x, y))
        except ValueError:
            continue
            
    if not coords:
        return 0
        
    max_area = 0
    n = len(coords)
    
    # Iterate all pairs
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            
            # Opposing corners
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
                
    return max_area

def is_point_in_or_on_poly(pt, edges):
    px, py = pt
    # If point is on an edge, it's valid
    # Use small epsilon for float comparisons if needed, but we can stick to exact logic for axis-aligned
    # Actually, standard ray casting:
    # Ray to the right (y = py, x > px)
    # Count intersections with vertical edges
    
    inside = False
    for (x1, y1), (x2, y2) in edges:
        # Check if point is exactly on the segment
        if x1 == x2 == px:
             if min(y1, y2) <= py <= max(y1, y2):
                 return True
        if y1 == y2 == py:
             if min(x1, x2) <= px <= max(x1, x2):
                 return True

        # Ray casting for vertical edges
        if x1 == x2:
            # Edge is vertical. 
            # Check if our ray crosses it.
            # Ray y is py. Edge y range is y1..y2
            # Crosses if min(y1,y2) < py <= max(y1,y2) 
            # (Use half-open interval to avoid double counting vertices)
            if min(y1, y2) < py <= max(y1, y2):
                if x1 >= px: # Ray is to the right
                    inside = not inside
                    
    return inside

def solve_part2(input_data):
    coords = []
    for line in input_data:
        line = line.strip()
        if not line:
            continue
        try:
            x, y = map(int, line.split(','))
            coords.append((x, y))
        except ValueError:
            continue
            
    if not coords:
        return 0
        
    # Build edges
    edges = []
    n = len(coords)
    for i in range(n):
        p1 = coords[i]
        p2 = coords[(i + 1) % n]
        edges.append((p1, p2))
        
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            pairs.append((area, coords[i], coords[j]))
            
    # Sort by area desc
    pairs.sort(key=lambda x: x[0], reverse=True)
    
    for area, p1, p2 in pairs:
        x1, y1 = p1
        x2, y2 = p2
        
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        
        # Check 1: Interior Intersection
        # The INTERIOR is (xmin < x < xmax) AND (ymin < y < ymax)
        # Verify no polygon edge intersects this open rectangle
        
        has_intersection = False
        for (ex1, ey1), (ex2, ey2) in edges:
            if ex1 == ex2: # Vertical Polygon Edge
                # Intersects if xmin < ex1 < xmax AND interval overlap in Y
                # Edge Y interval: [min(ey1, ey2), max(ey1, ey2)]
                # Rect Y interval: (ymin, ymax)
                if xmin < ex1 < xmax:
                    edge_ymin, edge_ymax = min(ey1, ey2), max(ey1, ey2)
                    if not (edge_ymax <= ymin or edge_ymin >= ymax):
                        has_intersection = True
                        break
            else: # Horizontal Polygon Edge
                if ymin < ey1 < ymax:
                    edge_xmin, edge_xmax = min(ex1, ex2), max(ex1, ex2)
                    if not (edge_xmax <= xmin or edge_xmin >= xmax):
                        has_intersection = True
                        break
                        
        if has_intersection:
            continue
            
        # Check 2: Center Inside
        # Use midpoint. Ideally (xmin + xmax) / 2
        mid_x = (xmin + xmax) / 2
        mid_y = (ymin + ymax) / 2
        
        if is_point_in_or_on_poly((mid_x, mid_y), edges):
            return area
            
    return 0

if __name__ == "__main__":
    print("--- Day 9: Movie Theater ---")
    
    # Verification
    example_input = [
        "7,1",
        "11,1",
        "11,7",
        "9,7",
        "9,5",
        "2,5",
        "2,3",
        "7,3"
    ]
    
    print(f"Part 1 Example: {solve(example_input)}")
    print(f"Part 2 Example: {solve_part2(example_input)}")
    
    if solve_part2(example_input) == 24:
        input_data = read_lines(9)
        print(f"Part 1 Result: {solve(input_data)}")
        print(f"Part 2 Result: {solve_part2(input_data)}")
    else:
        print("Part 2 Example Verification FAILED")
