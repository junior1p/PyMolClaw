---
name: pymol-claw
description: >
  A comprehensive molecular visualization and analysis skill powered by PyMOL.
  Use this whenever the user wants to visualize, analyze, or compare protein/nucleic acid/small molecule structures.
  
  Triggers include ANY of:
  - PyMOL, molecular visualization, protein rendering, PDB, structure figure
  - protein, ligand, binding site, pocket, active site, catalytic residue
  - align, superimpose, RMSD, compare structures
  - surface, electrostatic, electrostatic potential, APBS
  - electron density, EM map, cryo-EM, NMR ensemble
  - mutation, variant, SNP
  - distance, polar contact, hydrogen bond, salt bridge
  - B-factor, pLDDT, confidence, spectrum coloring
  - cartoon, stick, sphere, ribbon, backbone, sidechain
  - protein-protein interaction, PPI, interface
  - Goodsell, scientific illustration, publication quality
  - fetch, load, open a structure
  - animate, animation, tween, trajectory, molecular dynamics
  - residue, atom, chain, secondary structure, helix, sheet, loop
---

# PyMolClaw

A comprehensive skill for molecular visualization, structure comparison, and analysis using PyMOL.

## Capabilities

1. **Structure Fetching** — PDB IDs, AlphaFold models, local files
2. **Align & Superimpose** — Multi-structure alignment with RMSD reporting
3. **Binding Site Analysis** — Ligand interactions, pocket visualization
4. **PPI Interface** — Protein-protein interaction analysis
5. **Active Site** — Catalytic residues and environment
6. **Surface & Electrostatics** — Molecular surface, APBS potential
7. **Mutation Analysis** — Variant sites and structural context
8. **Distance & Contacts** — H-bonds, salt bridges, polar contacts
9. **Spectrum Coloring** — B-factor, pLDDT, residue properties
10. **Goodsell Style** — Flat scientific illustration
11. **Density Maps** — Electron density, EM maps, Cryo-EM
12. **Ensemble Analysis** — NMR ensembles, MD trajectories
13. **Annotations** — Labels, arrows, sequence annotations
14. **Animation** — Tweening and trajectory rendering

## Quick Start

```
align 1ubq with 4hhb
show binding site of 1abc with ligand LIG
make a goodsell style figure of 6m0j
compare these two structures: 1ubq and 2流
show the active site with catalytic residues in chain A
render the surface of this protein with electrostatic potential
```

## Workflow

### Step 1: Identify Task Type

| User says... | Task | Script |
|---|---|---|
| align / compare / RMSD | Align two structures | `align.py` |
| binding site / ligand / pocket | Ligand interactions | `binding_site.py` |
| protein-protein / interface | PPI analysis | `ppi.py` |
| active site / catalytic | Catalytic residues | `active_site.py` |
| surface / electrostatics | Surface rendering | `surface.py` |
| mutation / variant | Mutation analysis | `mutation.py` |
| distance / contacts / hbond | Measurements | `distance.py` |
| spectrum / B-factor / pLDDT | Property coloring | `spectrum.py` |
| goodsell / illustration | Scientific art | `goodsell.py` |
| density / EM map / cryo-EM | Density visualization | `density.py` |
| ensemble / trajectory / MD | Ensemble analysis | `ensemble.py` |
| animate / animation / tween | Animation | `animation.py` |
| overview / cartoon / render | General figure | `overview.py` |

### Step 2: Execute Script

```bash
python /root/PyMolClaw/scripts/<script>.py --pdb1 1ubq --pdb2 4hhb [--outdir /path/to/output]
```

All scripts accept:
- `--pdb1` / `--pdb2` — PDB IDs or local file paths
- `--chain1` / `--chain2` — Optional chain ID
- `--outdir` — Output directory (default: /tmp/pymol_output)
- `--format` — Output format for PNG (default: png)

### Step 3: Deliver Output

Every task returns three files:
1. **PNG image** — Rendered figure
2. **PML script** — Reproducible script for tweaking
3. **PSE session** — Interactive PyMOL session

## Script Reference

### align.py — Structure Alignment & RMSD
```
python align.py --pdb1 1ubq --pdb2 4hhb [--cutoff 5.0] [--outdir /tmp]
```
Outputs: aligned.png, rmsd.txt, aligned.pse

### binding_site.py — Ligand Binding Site
```
python binding_site.py --pdb 1abc --ligand LIG [--cutoff 4.0] [--outdir /tmp]
```
Outputs: binding_site.png, binding_site.pse

### ppi.py — Protein-Protein Interface
```
python ppi.py --pdb 6m0j --chain_a A --chain_b B [--cutoff 4.0] [--outdir /tmp]
```
Outputs: ppi.png, ppi.pse

### active_site.py — Active Site / Catalytic Residues
```
python active_site.py --pdb 1abc --residues "100,150,200" --chain A [--cutoff 5.0] [--outdir /tmp]
```
Outputs: active_site.png, active_site.pse

### surface.py — Surface Rendering
```
python surface.py --pdb 1ubq [--style surface|mesh|dots] [--transparency 0.5] [--outdir /tmp]
```
Outputs: surface.png, surface.pse

### mutation.py — Mutation Site Analysis
```
python mutation.py --pdb 1ubq --residue 150 --chain A [--cutoff 5.0] [--outdir /tmp]
```
Outputs: mutation.png, mutation.pse

### distance.py — Distances and Polar Contacts
```
python distance.py --pdb 1abc --sele1 "chain A and resi 100" --sele2 "chain B and resi 200" [--mode hbond] [--outdir /tmp]
```
Outputs: distance.png, distance.pse

### spectrum.py — Spectrum Coloring
```
python spectrum.py --pdb 1ubq --property bfactor|plddt|occupancy [--palette blue_white_red] [--outdir /tmp]
```
Outputs: spectrum.png, spectrum.pse

### goodsell.py — Goodsell Style Illustration
```
python goodsell.py --pdb 1ubq [--outdir /tmp]
```
Outputs: goodsell.png, goodsell.pse

### density.py — Electron Density / EM Maps
```
python density.py --pdb 1abc --map 1abc_2fofc.ccp4 [--level 1.5] [--outdir /tmp]
```
Outputs: density.png, density.pse

### ensemble.py — NMR / Trajectory Ensemble
```
python ensemble.py --pdb 1r55 [--mode nmr|trajectory] [--outdir /tmp]
```
Outputs: ensemble.png, ensemble.pse

### animation.py — Tween Animation
```
python animation.py --pdb 1ubq --frames 60 [--outdir /tmp]
```
Outputs: animation.gif, animation.pse

### overview.py — General Protein Overview
```
python overview.py --pdb 1ubq [--style cartoon|surface|ribbon] [--chain A] [--outdir /tmp]
```
Outputs: overview.png, overview.pse

## Prerequisites

PyMOL must be installed:
```bash
conda install -c conda-forge pymol-open-source
# or
pip install pymol-open-source
```

Check installation:
```bash
pymol -c -q && echo "PyMOL ready"
```

## Key Rules

1. Always `space cmyk` for print-ready colors
2. Always `remove elem H` unless user needs hydrogens
3. Always `save .pse` BEFORE ray tracing
4. Use `async=0` with `fetch` — don't race the next command
5. End scripts with `quit` — otherwise PyMOL hangs in batch mode
6. Render large (2400×1800), downscale later for quality
7. Create separate objects for surface overlays — transparency is per-object
8. Use `util.color_chains` for molecule-agnostic carbon coloring
