#!/usr/bin/env python3
"""Site-identity check: does the starting Cu CN stay the same after CO-only MACE relax?
CN counts only Cu–Cu pairs (adsorbate is ignored)."""
import torch
from ase.cluster import Octahedron
from ase.build import molecule
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from mace.calculators import mace_mp

device = "cuda" if torch.cuda.is_available() else "cpu"
print("device =", device)
calc = mace_mp(model="small", device=device, default_dtype="float32")

np_atoms = Octahedron("Cu", length=4, latticeconstant=3.6149, cutoff=0.0)
n_cu = len(np_atoms)
print("N_Cu", n_cu)

def cn_of(atoms, idx, cut=2.7, n_metal=None):
    """Coordination number among metal atoms only."""
    if n_metal is None:
        n_metal = sum(1 for s in atoms.get_chemical_symbols() if s == "Cu")
    pos = atoms.positions[:n_metal]
    d = pos - pos[idx]
    r2 = (d ** 2).sum(axis=1)
    return int(((r2 > 1e-6) & (r2 <= cut ** 2)).sum())

site_vertex = next(i for i in range(n_cu) if cn_of(np_atoms, i, n_metal=n_cu) == 4)
site_edge = next(i for i in range(n_cu) if cn_of(np_atoms, i, n_metal=n_cu) == 7)
print("vertex", site_vertex, "CN", cn_of(np_atoms, site_vertex, n_metal=n_cu))
print("edge  ", site_edge, "CN", cn_of(np_atoms, site_edge, n_metal=n_cu))

def place_co(slab, site_idx, height=1.90):
    atoms = slab.copy()
    co = molecule("CO")
    co.positions = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.13]]
    pos = atoms.positions[site_idx].copy()
    co.translate(pos + [0.0, 0.0, height])
    atoms += co
    return atoms

np_atoms.calc = calc
e_np = float(np_atoms.get_potential_energy())
co_gas = molecule("CO")
co_gas.calc = calc
e_co = float(co_gas.get_potential_energy())
print("E_NP", round(e_np, 4), "E_CO", round(e_co, 4))

def e_ads(atoms):
    atoms.calc = calc
    return float(atoms.get_potential_energy()) - e_np - e_co

def check_site(label, site_idx, height=1.90, max_steps=30):
    atoms0 = place_co(np_atoms, site_idx, height)
    e0 = e_ads(atoms0)
    cn0 = cn_of(atoms0, site_idx, n_metal=n_cu)

    atoms1 = atoms0.copy()
    atoms1.set_constraint(FixAtoms(indices=list(range(n_cu))))
    atoms1.calc = calc
    opt = BFGS(atoms1, logfile=None)
    opt.run(fmax=0.05, steps=max_steps)
    e1 = e_ads(atoms1)

    c_pos = atoms1.positions[-2]
    d = atoms1.positions[:n_cu] - c_pos
    closest = int((d ** 2).sum(axis=1).argmin())
    cn1 = cn_of(atoms1, closest, n_metal=n_cu)
    same_cu = closest == site_idx
    same_cn = cn1 == cn0
    print(
        f"{label:12s} site={site_idx} CN0={cn0} closest={closest} CN1={cn1} "
        f"same_cu={same_cu} same_cn={same_cn} "
        f"Eads0={e0:.3f} Eads1={e1:.3f} steps={opt.get_number_of_steps()}"
    )

print("SITE_IDENTITY_CHECK")
check_site("vertex", site_vertex)
check_site("edge", site_edge)
print("LIMITS: bulk MACE-MP, frozen Cu, no support, no potential, one small NP.")
print("CN counts only Cu-Cu neighbors.")
