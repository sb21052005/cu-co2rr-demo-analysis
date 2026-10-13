#!/usr/bin/env python3
"""CN histogram and low-CN cluster sizes for an xyz from MOSP examples or OUTPUT.
Counts only metal-metal neighbors. Does not claim peninsula vs island."""
from collections import Counter
from pathlib import Path
import sys
import numpy as np

CUT = 2.9
LOW = 6

def load_xyz(path):
    lines = Path(path).read_text().splitlines()
    n = int(lines[0].split()[0])
    rows = []
    for line in lines[2:2 + n]:
        p = line.split()
        if len(p) < 4:
            continue
        rows.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return rows

def main(path):
    rows = load_xyz(path)
    if not rows:
        print("no atoms")
        return
    symbols = [r[0] for r in rows]
    pos = np.array([[r[1], r[2], r[3]] for r in rows], dtype=float)
    n = len(rows)
    print("file", path)
    print("n", n, "symbols", dict(Counter(symbols)))
    inv = 1.0 / CUT
    keys = np.floor(pos * inv).astype(int)
    buckets = {}
    for i, k in enumerate(keys):
        buckets.setdefault((int(k[0]), int(k[1]), int(k[2])), []).append(i)
    cn = np.zeros(n, dtype=int)
    c2 = CUT * CUT
    for i, p in enumerate(pos):
        k = keys[i]
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in buckets.get((int(k[0]) + dx, int(k[1]) + dy, int(k[2]) + dz), ()):
                        if j <= i:
                            continue
                        d = pos[i] - pos[j]
                        if float(d @ d) <= c2:
                            cn[i] += 1
                            cn[j] += 1
    print("CN histogram", dict(sorted(Counter(cn.tolist()).items())))
    low = cn <= LOW
    print("atoms with CN<=%d" % LOW, int(low.sum()))
    low_idx = np.where(low)[0]
    parent = {int(i): int(i) for i in low_idx}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    for a in range(len(low_idx)):
        for b in range(a + 1, len(low_idx)):
            d = pos[low_idx[a]] - pos[low_idx[b]]
            if float(d @ d) <= c2:
                union(int(low_idx[a]), int(low_idx[b]))
    if low_idx.size:
        sizes = Counter(find(int(i)) for i in low_idx)
        print("low-CN cluster sizes", dict(sorted(Counter(sizes.values()).items())))
    print("CUT", CUT, "NOTE: no facet IDs; do not label peninsula/island.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 mosp_cn_helper.py path/to/file.xyz")
        sys.exit(1)
    main(sys.argv[1])
