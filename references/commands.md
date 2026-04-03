# PyMOL Command Reference

Quick reference of PyMOL commands used by PyMolClaw scripts.

## Loading Structures

```pymol
fetch 1ubq, async=0              # Fetch from PDB (async=0 = wait)
load /path/to/file.pdb, name      # Load local file
fetch 1ubq, 2lh5, async=0         # Fetch multiple
fetch Q9Y6K9, type=alphafold     # AlphaFold model
```

## Selections

```pymol
select name, selection_text
select binding, byres (ligand around 4.0)
select chainA, chain A
select iface, byres (chainA within 4.0 of chainB)
```

Selection keywords: `and`, `or`, `not`, `byres`, `around`, `expand`, `within`

## Visualization Modes

```pymol
show cartoon              # Cartoon (default for proteins)
show surface              # Molecular surface
show sticks               # Stick model
show spheres              # Sphere model
show ribbon               # Ribbon
show lines                # Line representation
hide everything
hide lines, not ligand
```

## Coloring

```pymol
color red, selection
color 0x7EB6D9, selection  # Hex color
util.color_chains("sele and elem C", _self=cmd)
util.cnc("all", _self=cmd) # Color by element (C=chain, N=blue, O=red)
util.chainbow("sele")       # Rainbow by chain
spectrum b, blue_white_red, selection  # B-factor coloring
```

## Geometry & Measurements

```pymol
dist hbonds, sel1, sel2, mode=2   # H-bond detection
dist contacts, sel1, sel2         # All contacts
measure loop, atom1, atom2       # Distance between two atoms
```

## Alignment

```pymol
align target, reference
align target and name CA, reference and name CA, cutoff=5.0
super target, reference            # Slower but more accurate
rmsd target, reference           # Quick RMSD
```

## Camera

```pymol
orient                         # Fit on screen
orient selection               # Fit selection to center
zoom selection, 8              # Zoom to selection (+ padding)
zoom center, 20                # Zoom to center
reset                          # Reset camera
```

## Quality & Rendering

```pymol
ray 2400, 1800                 # Ray trace (do BEFORE png)
png file.png, dpi=150          # Save image
save file.pse                  # Save session (do BEFORE ray)
```

## Settings

```pymol
set ray_trace_mode, 1          # 0=normal, 1=outline, 2=fill, 3=edge
set antialias, 3               # Anti-aliasing level
set opaque_background, off      # Transparent background
bg_color white                 # Background color
space cmyk                      # Print color space
```

## Surfaces

```pymol
set surface_quality, 1
set transparency, 0.5, object
cmd.color_deep("white", "surf", 0)
create surf_obj, selection, zoom=0
```

## Animation

```pymol
mpng frame_%%04d.png, first=1, last=60, modulus=4
mview store, 1
mview store, 60
mdo 1, turn x, 3
mplay
```

## Useful One-liners

```pymol
# Remove water and hydrogens
remove solvent; remove elem H

# Color by secondary structure
dss; color red, ss h; color yellow, ss s; color green, ss l+''

# Show only interface residues
select iface, byres (chain A within 4.0 of chain B)

# Ligand + surrounding residues
select ligand, resn LIG; select pocket, byres ligand around 4.0

# Bold cartoon for active site
set cartoon_rect_length, 1; set cartoon_oval_length, 1

# Spectrum coloring by B-factor
spectrum b, blue_white_red, all

# Good start for any figure
reinitialize; bg_color white; set opaque_background, off
```
