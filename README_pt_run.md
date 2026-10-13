# Summary of a local Pt-NP + CO KMC demo run

Upstream: https://github.com/mosp-catalysis/kmc_Pt_NP_CO

## What was run
kmc_Pt_NP_CO.exe after setting LD_LIBRARY_PATH to a Conda libgfortran.so.3.

## Numbers from this run (step_rec_00.dat / last_one.xyz)
- 100001 steps, final time ~3.6e-8 s
- 246 metal jumps
- CO ads / des / diff: 1325 / 1073 / 97357
- last_one: 738 bulk (5), 382 empty surface (0), 252 CO* (1)
- surface sites 634, theta_CO ~ 0.40

## Limits
- Demo binary. Formal version not released.
- Low-CN clustering on last_one is possible but facet IDs are not in the file; do not label peninsula vs island.
