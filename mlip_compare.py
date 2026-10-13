#!/usr/bin/env python3
"""Side-by-side site-identity check: MACE-MP vs ASE EMT on the same Cu octahedron + CO.
Does not train. Inference only."""
import torch
from ase.cluster import Octahedron
from ase.build import molecule
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from ase.calculators.emt import EMT
from mace.calculators import mace_mp

device = "cuda" if torch.cuda.is_available() else "cpu"
print("device =", device)

np0 = Octahedron("Cu", length=4, latticeconstant=3.6149, cutoff=0.0)
n_cu = len(np0)

def cn_of(atoms, idx, cut=2.7, n_metal=None):
    if n_metal is None:
        n_metal = n_cu
    pos = atoms.positions[:n_metal]
    d = pos - pos[idx]
    r2 = (d ** 2).sum(axis=1)
    return int(((r2 > 1e-6) & (r2 <= cut ** 2)).sum())

site_vertex = next(i for i in range(n_cu) if cn_of(np0, i) == 4)
site_edge = next(i for i in range(n_cu) if cn_of(np0, i) == 7)

def place_co(slab, site_idx, height=1.90):
    atoms = slab.copy()
    co = molecule("CO")
    co.positions = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.13]]
    pos = atoms.positions[site_idx].copy()
    co.translate(pos + [0.0, 0.0, height])
    atoms += co
    return atoms

def run_one(name, calc, site_idx, label):
    atoms0 = place_co(np0, site_idx)
    bare = np0.copy()
    bare.calc = calc
    co_gas = molecule("CO")
    co_gas.calc = calc
    e_np = float(bare.get_potential_energy())
    e_co = float(co_gas.get_potential_energy())
    atoms0.calc = calc
    e0 = float(atoms0.get_potential_energy()) - e_np - e_co
    cn0 = cn_of(atoms0, site_idx)

    atoms1 = atoms0.copy()
    atoms1.set_constraint(FixAtoms(indices=list(range(n_cu))))
    atoms1.calc = calc
    opt = BFGS(atoms1, logfile=None)
    opt.run(fmax=0.05, steps=30)
    e1 = float(atoms1.get_potential_energy()) - e_np - e_co
    c_pos = atoms1.positions[-2]
    d = atoms1.positions[:n_cu] - c_pos
    closest = int((d ** 2).sum(axis=1).argmin())
    cn1 = cn_of(atoms1, closest)
    same_cu = closest == site_idx
    print(f"{name:8s} {label:8s} site={site_idx} CN0={cn0} closest={closest} CN1={cn1} "
          f"same_cu={same_cu} Eads0={e0:.3f} Eads1={e1:.3f}")

print("MLIP_COMPARE")
mace = mace_mp(model="small", device=device, default_dtype="float32")
emt = EMT()
run_one("MACE", mace, site_vertex, "vertex")
run_one("MACE", mace, site_edge, "edge")
run_one("EMT", emt, site_vertex, "vertex")
run_one("EMT", emt, site_edge, "edge")
print("LIMITS: bulk MACE-MP and ASE EMT. No support, no potential. One small NP. Frozen Cu.")
