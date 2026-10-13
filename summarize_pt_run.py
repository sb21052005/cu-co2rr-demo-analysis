#!/usr/bin/env python3
"""Summarize a Pt KMC run from step_rec_00.dat and last_one.xyz (if present)."""
from collections import Counter
from pathlib import Path
import numpy as np

STEP = Path("step_rec_00.dat")
LAST = Path("last_one.xyz")

if STEP.exists():
    raw = np.loadtxt(STEP, skiprows=0)
    # columns: time, steps, atom_jumps, CO_ads, CO_des, CO_diff (from README)
    print("step_rec rows:", len(raw))
    print("final time (s):", raw[-1, 0])
    print("final steps:", int(raw[-1, 1]))
    print("final metal jumps:", int(raw[-1, 2]))
    print("final CO ads / des / diff:", int(raw[-1, 3]), int(raw[-1, 4]), int(raw[-1, 5]))
else:
    print("no step_rec_00.dat")

if LAST.exists():
    st = Counter()
    with LAST.open() as f:
        n = int(f.readline().split()[0])
        f.readline()
        for _ in range(n):
            p = f.readline().split()
            if len(p) >= 5:
                st[p[4]] += 1
    print("last_one states:", dict(st))
    surf = st.get("0", 0) + st.get("1", 0)
    print("surface sites:", surf)
    print("theta_CO:", st.get("1", 0) / surf if surf else None)
else:
    print("no last_one.xyz")
print("NOTE: low-CN clustering needs facet IDs we do not have; do not call peninsula/island.")
