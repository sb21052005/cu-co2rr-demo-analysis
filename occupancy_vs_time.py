#!/usr/bin/env python3
"""Stream traj-demo.xyz (does not load the whole 1.2 GB) and write occupancy vs frame."""
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

XYZ = Path("traj-demo.xyz")
DAT = Path("traj-demo.dat")
STRIDE = 10
OUT_CSV = Path("occupancy_vs_time.csv")
OUT_PNG = Path("occupancy_vs_time.png")

def parse_comment_time(comment: str) -> float:
    for p in reversed(comment.split()):
        try:
            return float(p)
        except ValueError:
            continue
    return float("nan")

def sample(path: Path, stride: int):
    rows = []
    with path.open() as f:
        iframe = 0
        while True:
            line = f.readline()
            if not line:
                break
            natoms = int(line.strip())
            comment = f.readline()
            take = iframe % stride == 0
            st = Counter()
            for _ in range(natoms):
                parts = f.readline().split()
                if take and len(parts) >= 5:
                    st[parts[4]] += 1
            if take:
                bulk = st.get("5", 0)
                empty = st.get("0", 0)
                co = st.get("1", 0)
                h = st.get("2", 0)
                surf = empty + co + h
                t = parse_comment_time(comment)
                rows.append((
                    iframe + 1, t, natoms, bulk, surf, empty, co, h,
                    co / surf if surf else float("nan"),
                    h / surf if surf else float("nan"),
                ))
            iframe += 1
    return rows, iframe

rows, nframes = sample(XYZ, STRIDE)
header = "frame,time_s,natoms,bulk,surface,empty,co,h,theta_CO,theta_H"
with OUT_CSV.open("w") as f:
    f.write(header + "\n")
    for r in rows:
        f.write(",".join(str(x) for x in r) + "\n")

data = np.array(rows, dtype=float)
fig, ax = plt.subplots(2, 1, figsize=(7.2, 6.0), sharex=True)
ax[0].plot(data[:, 0], data[:, 4], color="0.15", lw=1.6)
ax[0].set_ylabel("surface sites")
ax[0].axvline(101, color="0.7", ls="--", lw=1)
ax[1].plot(data[:, 0], data[:, 8], color="0.15", lw=1.6, label="theta_CO")
ax[1].plot(data[:, 0], data[:, 9], color="0.55", lw=1.6, label="theta_H")
ax[1].axvline(101, color="0.7", ls="--", lw=1)
ax[1].set_ylabel("coverage")
ax[1].set_xlabel("xyz frame index (sampled every %d)" % STRIDE)
ax[1].legend(frameon=False)
fig.suptitle("Cu(100) eCO2RR demo — occupancy\n(dashed: comment-time reset around frame 101)", y=0.99)
fig.tight_layout()
fig.savefig(OUT_PNG, dpi=160)
print(f"total frames in xyz: {nframes}")
print(f"sampled: {len(rows)}")
print(f"wrote {OUT_CSV}")
print(f"wrote {OUT_PNG}")
