# How the public KMC binaries were run

These notes are for the demo binaries released by the mosp-catalysis group.
They are incomplete demos. Formal source is not released.

## Pt nanoparticle + CO

Repo: https://github.com/mosp-catalysis/kmc_Pt_NP_CO

The binary kmc_Pt_NP_CO.exe needs libgfortran.so.3.
On a recent Ubuntu this library is not in the default packages.

What worked (Conda env already present):

  conda activate cwola
  conda install -y -c conda-forge/label/cf201901 libgfortran
  export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:${LD_LIBRARY_PATH}"
  cd ~/kmc_Pt_NP_CO
  ./kmc_Pt_NP_CO.exe

After a short run the binary wrote step_rec_00.dat, last_one.xyz, and atom_str_00.xyz.

One local run produced (see README_pt_run.md):
- 100001 steps
- 246 metal jumps
- CO ads / des / diff: 1325 / 1073 / 97357
- last_one states: bulk 738, empty surface 382, CO* 252

## Cu(100) GCMC + EKMC

Repo: https://github.com/mosp-catalysis/kmc_Cu_100_CO_H

The binary in GCMC-EKMC-input-files looks for a file literally named input.
The supplied file is named input-forKMC1diff.

What was tried:

  cd ~/kmc_Pt_NP_CO/kmc_Cu_100_CO_H/GCMC-EKMC-input-files
  ln -sf input-forKMC1diff input
  ./kmc.exe

It exited with: Error: rtot is too small! rtot=0.00000000000000000000

This is recorded so others do not spend time on the same dead end.
The useful public artifact for Cu is the trajectory dump (traj-demo.xyz + traj-demo.dat),
which is parsed by occupancy_vs_time.py.

## Limits

- These are demo binaries. Runtime and input quirks are expected.
- The Pt notes are from one local run after the library path was set.
- The Cu binary was not made to complete a run.
- No claim is made about the physical correctness of either demo.
