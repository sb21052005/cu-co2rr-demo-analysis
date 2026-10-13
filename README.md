# Analysis of public Cu and Pt KMC demos + a site-identity check

Small, inspectable scripts that sit next to the public demos from the mosp-catalysis group.
Not a new model. Not a new simulation.

## Contents

- occupancy_vs_time.py: Streams the public Cu(100) eCO2RR trajectory (traj-demo.xyz, ~1.2 GB) and writes occupancy vs frame. Does not load the whole file.
- README_analysis.md: Limits and how to run the Cu parser.
- summarize_pt_run.py: Prints event counts and final coverage from a local run of the Pt nanoparticle + CO KMC demo.
- README_pt_run.md: Numbers from one local Pt run and limits.
- site_identity_check.py: ASE + MACE-MP on a 44-atom Cu octahedron. Places CO on a vertex (CN=4) and an edge (CN=7), does a short CO-only relax, and reports whether the closest Cu stayed the same. CN counts only Cu-Cu neighbors.
- site_identity_result.txt: Saved output of the site-identity check.

## Upstream demos

- Cu(100) GCMC+EKMC: https://github.com/mosp-catalysis/kmc_Cu_100_CO_H
- Pt nanoparticle + CO: https://github.com/mosp-catalysis/kmc_Pt_NP_CO
- MOSP package: https://github.com/mosp-catalysis/MOSP

## Quick start

Cu parser (needs traj-demo.xyz from the upstream repo):
  python3 occupancy_vs_time.py

Pt summary (needs the output files from a local run of the binary):
  python3 summarize_pt_run.py

Site-identity check (needs ase and mace-torch; GPU optional):
  python3 site_identity_check.py

## Site-identity result (one run)

vertex  site=0  CN0=4  closest=0  CN1=4  same_cu=True   same_cn=True
edge    site=1  CN0=7  closest=3  CN1=7  same_cu=False  same_cn=True

Vertex kept its Cu. Edge hopped to a different Cu that also has CN=7.

## Limits

- Demo dumps and a bulk MACE-MP potential only.
- No support, no applied potential, no open-system atom exchange.
- Cu trajectory comment times reset around frame 101.
- Net rise in surface tags in the Cu dump is two-way bulk-surface flips, not new islands.
- Pt demo is a binary; formal source not released.
- Site-identity check is one small nanoparticle and a short frozen-Cu relax.
- Do not treat these as peninsula/island results or as a new method.

## Environment notes

- Pt binary needs an older libgfortran.so.3 on the library path.
- Cu binary looks for a file named input and can exit with rtot=0 if the input is incomplete.
- MACE-MP model is downloaded on first use of the site-identity script.
