#!/usr/bin/env python3
"""
binding_site.py — Ligand binding site visualization
Usage: python binding_site.py --pdb 1abc --ligand LIG [--cutoff 4.0] [--outdir /tmp]
"""

import argparse
import os
import subprocess
import re

def run_pml(pml_content, outdir):
    os.makedirs(outdir, exist_ok=True)
    pml_path = os.path.join(outdir, "binding_site.pml")
    with open(pml_path, "w") as f:
        f.write(pml_content)
    result = subprocess.run(
        ["pymol", "-c", "-q", pml_path],
        capture_output=True, text=True, timeout=120
    )
    return pml_path, result.stdout + result.stderr

def is_pdb_id(pdb):
    return bool(re.match(r"^[a-zA-Z0-9]{4}$", pdb))

def main():
    parser = argparse.ArgumentParser(description="Visualize ligand binding site")
    parser.add_argument("--pdb", required=True, help="PDB ID or local file path")
    parser.add_argument("--ligand", default="LIG", help="Ligand residue name (e.g., LIG, HEM, ATP)")
    parser.add_argument("--cutoff", type=float, default=4.0, help="Distance cutoff (Angstroms)")
    parser.add_argument("--chain", default="", help="Chain ID")
    parser.add_argument("--outdir", default="/tmp/pymol_output", help="Output directory")
    parser.add_argument("--name", default="protein", help="Object name")
    args = parser.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    if is_pdb_id(args.pdb):
        load_cmd = f"fetch {args.pdb}, {args.name}, async=0"
    else:
        load_cmd = f"load {args.pdb}, {args.name}"

    ligand_sel = f"resn {args.ligand}"
    if args.chain:
        ligand_sel += f" and chain {args.chain}"

    pml = f"""
reinitialize

# --- Load ---
{load_cmd}

# --- Clean ---
remove solvent
remove elem H
set valence, 0

# --- Selections ---
select ligand, {ligand_sel}
select binding, byres (ligand around {args.cutoff}) and not ligand
select protein, not ligand and not resn HOH

# --- Base look ---
bg_color white
space cmyk
set ray_shadow, 0
set ray_trace_mode, 1
set antialias, 3
set ambient, 0.5
set spec_count, 5
set shininess, 50
set specular, 1
set reflect, 0.1
set orthoscopic, on
set opaque_background, off
set cartoon_oval_length, 1
set cartoon_rect_length, 1
set cartoon_discrete_colors, on
dss

# --- Representation ---
hide everything

# semi-transparent cartoon for context
show cartoon, protein
set cartoon_transparency, 0.7

# binding residues as sticks
cmd.show("sticks", "((byres binding) & (sc. | (n. CA) | (n. N & r. PRO)))")
color gray70, binding and elem C
util.cnc("binding", _self=cmd)
set stick_radius, 0.2

# ligand as ball-and-stick
show sticks, ligand
show spheres, ligand
set sphere_scale, 0.25, ligand
set stick_radius, 0.15, ligand
set valence, 1, ligand
color marine, ligand and elem C
util.cnc("ligand", _self=cmd)

# polar contacts
dist hbonds, ligand, binding, mode=2
hide labels, hbonds
set dash_color, black, hbonds
set dash_gap, 0.3
set dash_radius, 0.06

# --- Camera ---
orient ligand
zoom ligand, 6

# --- Save session ---
save {outdir}/binding_site.pse

# --- Render ---
ray 2400, 1800
png {outdir}/binding_site.png, dpi=150
quit
"""

    pml_path, output = run_pml(pml, outdir)

    png_path = os.path.join(outdir, "binding_site.png")
    pse_path = os.path.join(outdir, "binding_site.pse")

    print(f"Output: {png_path}")
    print(f"Session: {pse_path}")

    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", png_path, desktop], capture_output=True)
        subprocess.run(["cp", pse_path, desktop], capture_output=True)
        print(f"Copied to Desktop")

if __name__ == "__main__":
    main()
