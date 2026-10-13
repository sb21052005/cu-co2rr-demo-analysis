# MOSP notes

Upstream: https://github.com/mosp-catalysis/MOSP

MOSP is a GUI package (main.py, OpenGL) for multiscale structure reconstruction + KMC.
The data/ folder contains Windows DLLs and main.exe, so the full GUI is intended for Windows.
On Linux/WSL the usable pieces are the example xyz files and any OUTPUT that a Windows run writes.

mosp_cn_helper.py reads an xyz (MOSP examples or OUTPUT) and prints:
- atom count and symbols
- CN histogram (metal-metal only)
- count and cluster-size distribution of atoms with CN <= 6

Limits:
- No facet IDs are present, so low-CN clusters are not peninsula vs island.
- This does not run the MOSP reconstruction or KMC; it only post-processes structures.
