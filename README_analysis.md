# Analysis of the public Cu(100) eCO2RR trajectory demo

Upstream: https://github.com/mosp-catalysis/kmc_Cu_100_CO_H

## What this is
Streaming parser for traj-demo.xyz (does not load the full ~1.2 GB).
Writes occupancy vs frame: surface sites, bulk, theta_CO, theta_H.

## Limits
- Demo dump only. Not a new simulation.
- Comment times reset around frame 101 (possible glued segments).
- Net rise in surface tags is two-way bulk-surface flips in the same z-range, not new islands.
- State column: 0 empty surface, 1 CO*, 2 H*, 5 bulk (from upstream README).

## Run
python3 occupancy_vs_time.py

Outputs: occupancy_vs_time.csv, occupancy_vs_time.png, occupancy_vs_frame.png.
