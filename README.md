# PyMolClaw

> A comprehensive molecular visualization and analysis skill powered by PyMOL. One description → publication-quality figure + analysis.

## What is it?

PyMolClaw turns natural language into publication-ready molecular graphics. Tell it what you want — a binding site comparison, an active site illustration, a Goodsell-style figure — and it generates the PyMOL script, renders it headlessly, and delivers the PNG, PML script, and PSE session.

It's built as a [Claude Code skill](https://github.com/anthropics/claude-code), so any agent that supports skills can use it. It can also be used standalone as Python scripts.

## Features

| Script | What it does |
|--------|-------------|
| `align.py` | Align two structures + RMSD |
| `overview.py` | General protein overview figure |
| `binding_site.py` | Ligand binding site with polar contacts |
| `ppi.py` | Protein-protein interaction interface |
| `goodsell.py` | Flat scientific illustration (Goodsell style) |
| `surface.py` | Molecular surface rendering |
| `mutation.py` | Mutation site analysis |
| `active_site.py` | Catalytic residues |
| `distance.py` | Distances & polar contacts |
| `spectrum.py` | B-factor / pLDDT coloring |
| `density.py` | Electron density / EM map |
| `ensemble.py` | NMR / MD trajectory ensemble |
| `animation.py` | Tween animation |

## Quick Start

### As a Claude Code Skill

```
Install the PyMolClaw skill from https://github.com/YOUR_HANDLE/PyMolClaw
```

Then ask:
```
align 1ubq with 4hhb and show me the RMSD
make a binding site figure of 1abc with ligand LIG
render 6m0j in Goodsell style
```

### Standalone Scripts

```bash
# Align two structures
python scripts/align.py --pdb1 1ubq --pdb2 4hhb --outdir /tmp/output

# Protein overview
python scripts/overview.py --pdb 1ubq --style cartoon --outdir /tmp/output

# Binding site
python scripts/binding_site.py --pdb 1abc --ligand LIG --outdir /tmp/output

# Goodsell style
python scripts/goodsell.py --pdb 6m0j --outdir /tmp/output
```

Every script outputs three files:
- `*.png` — Rendered figure
- `*.pse` — PyMOL session (open in GUI to keep editing)
- `*.pml` — Reproducible PyMOL script

## Prerequisites

PyMOL must be installed:

```bash
conda install -c conda-forge pymol-open-source
```

Verify:
```bash
pymol -c -q && echo "PyMOL ready"
```

## Skill Installation (Claude Code)

```bash
# Option 1: Clone directly
git clone https://github.com/YOUR_HANDLE/PyMolClaw.git ~/.claude/skills/pymol-claw

# Option 2: Ask an agent
# "Install the PyMolClaw skill from https://github.com/YOUR_HANDLE/PyMolClaw"
```

## Architecture

```
PyMolClaw/
├── SKILL.md              # Main skill entry (trigger words + dispatch table)
├── references/
│   ├── recipes.md        # PyMOL scene recipes (from ChatMol)
│   └── commands.md       # PyMOL command cheat sheet
├── scripts/
│   ├── align.py
│   ├── overview.py
│   ├── binding_site.py
│   └── ...
└── README.md
```

## Example Output

### Align 1ubq vs 4hhb

```
$ python scripts/align.py --pdb1 1ubq --pdb2 4hhb --outdir /tmp/output
RMSD: 5.760 Angstroms
Output: /tmp/output/aligned.png
```

### Protein Overview

```python
python scripts/overview.py --pdb 1ubq --style cartoon --outdir /tmp/output
```

## License

MIT
