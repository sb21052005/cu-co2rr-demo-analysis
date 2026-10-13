# Side-by-side MLIP check

Same 44-atom Cu octahedron, same CO placement, short CO-only relax.
Two potentials: MACE-MP (small) and ASE EMT.

Question: does the starting site label (vertex CN=4 or edge CN=7) stay on the same Cu?

Result (one run):
  MACE  vertex  same_cu=True
  MACE  edge    same_cu=False
  EMT   vertex  same_cu=True
  EMT   edge    same_cu=True

Limits:
- Bulk MACE-MP and a simple EMT baseline. Not OC20/OC25.
- Frozen Cu, no support, no applied potential.
- One small nanoparticle.
- EMT is not trained for chemisorption; it is only a second, always-available calculator.
