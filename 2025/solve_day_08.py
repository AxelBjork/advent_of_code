#!/usr/bin/env python3
import sys
import math
from utils.inputs import read_lines, read_text

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_sets = n
        
    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
        
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.num_sets -= 1
            return True
        return False

def parse_input(input_data):
    coords = []
    for line in input_data:
        line = line.strip()
        if not line:
            continue
        try:
            x, y, z = map(int, line.split(','))
            coords.append((x, y, z))
        except ValueError:
            continue
    return coords

def solve_part1(input_data, limit):
    coords = parse_input(input_data)
    n = len(coords)
    edges = []
    
    # Calculate all pairwise distances
    for i in range(n):
        for j in range(i + 1, n):
            p1 = coords[i]
            p2 = coords[j]
            dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
            edges.append((dist_sq, i, j))
            
    # Sort edges by distance (ascending)
    edges.sort(key=lambda x: x[0])
    
    uf = UnionFind(n)
    
    # Process top `limit` edges
    count_limit = min(limit, len(edges))
    
    for k in range(count_limit):
        _, i, j = edges[k]
        uf.union(i, j)
        
    # Get all component sizes
    component_sizes = []
    seen_roots = set()
    for i in range(n):
        root = uf.find(i)
        if root not in seen_roots:
            component_sizes.append(uf.size[root])
            seen_roots.add(root)
            
    component_sizes.sort(reverse=True)
    
    if len(component_sizes) < 3:
        result = 1
        for s in component_sizes:
            result *= s
        return result
    
    return component_sizes[0] * component_sizes[1] * component_sizes[2]

def solve_part2(input_data):
    coords = parse_input(input_data)
    n = len(coords)
    edges = []
    
    # Calculate all pairwise distances
    for i in range(n):
        for j in range(i + 1, n):
            p1 = coords[i]
            p2 = coords[j]
            dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
            edges.append((dist_sq, i, j))
            
    # Sort edges by distance (ascending)
    edges.sort(key=lambda x: x[0])
    
    uf = UnionFind(n)
    
    # Connect until fully connected
    for _, i, j in edges:
        if uf.union(i, j):
            if uf.num_sets == 1:
                # This was the last edge needed
                p1 = coords[i]
                p2 = coords[j]
                return p1[0] * p2[0]
                
    return 0

if __name__ == "__main__":
    print("--- Day 8: Playground ---")
    
    # Verification
    example_input = [
        "162,817,812",
        "57,618,57",
        "906,360,560",
        "592,479,940",
        "352,342,300",
        "466,668,158",
        "542,29,236",
        "431,825,988",
        "739,650,466",
        "52,470,668",
        "216,146,977",
        "819,987,18",
        "117,168,530",
        "805,96,715",
        "346,949,466",
        "970,615,88",
        "941,993,340",
        "862,61,35",
        "984,92,344",
        "425,690,689"
    ]
    
    print("--- Verification ---")
    p1_ex = solve_part1(example_input, 10)
    print(f"Part 1 Example: {p1_ex} (Expected 40)")
    
    p2_ex = solve_part2(example_input)
    print(f"Part 2 Example: {p2_ex} (Expected 25272)")
    
    if p1_ex == 40 and p2_ex == 25272:
        print("\n--- Solving Real Input ---")
        input_data = read_lines(8)
        print(f"Part 1 Answer: {solve_part1(input_data, 1000)}")
        print(f"Part 2 Answer: {solve_part2(input_data)}")
    else:
        print(f"Verification FAILED.")
