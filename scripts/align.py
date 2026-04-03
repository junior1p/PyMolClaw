#!/usr/bin/env python3
"""
align.py — Structure alignment with RMSD reporting
Usage: python align.py --pdb1 1ubq --pdb2 4hhb [--cutoff 5.0] [--outdir /tmp]
"""

import argparse
import os
import sys
import re
import subprocess

def run_pml(pml_content, outdir):
    os.makedirs(outdir, exist_ok=True)
    pml_path = os.path.join(outdir, "align.pml")
    with open(pml_path, "w") as f:
        f.write(pml_content)
    result = subprocess.run(
        ["pymol", "-c", "-q", pml_path],
        capture_output=True, text=True, timeout=120
    )
    return pml_path, result.stdout + result.stderr

def parse_rmsd(pml_output):
    """Extract RMSD from PyMOL align output."""
    # PyMOL align output format: "RMSD: 1.23 (N atoms: 100)"
    match = re.search(r"RMSD:\s+([\d.]+)", pml_output, re.IGNORECASE)
    if match:
        return float(match.group(1))
    # Try super output: "ExecutiveAlign: RMSD = 1.23 angstroms"
    match = re.search(r"RMSD\s*=\s*([\d.]+)", pml_output, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def main():
    parser = argparse.ArgumentParser(description="Align two structures and report RMSD")
    parser.add_argument("--pdb1", required=True, help="First PDB ID or local path")
    parser.add_argument("--pdb2", required=True, help="Second PDB ID or local path")
    parser.add_argument("--cutoff", type=float, default=5.0, help="Cutoff for align (Angstroms)")
    parser.add_argument("--outdir", default="/tmp/pymol_output", help="Output directory")
    parser.add_argument("--name1", default="struct1", help="Name for first structure")
    parser.add_argument("--name2", default="struct2", help="Name for second structure")
    args = parser.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    # Determine if PDB ID or local file
    pdb1_arg = args.pdb1
    pdb2_arg = args.pdb2
    pdb1_load = f"load {pdb1_arg}, {args.name1}" if not args.pdb1.startswith("fetch") and not re.match(r"^[a-zA-Z0-9]{4}$", args.pdb1) else f"fetch {args.pdb1}, {args.name1}, async=0"
    pdb2_load = f"load {pdb2_arg}, {args.name2}" if not args.pdb2.startswith("fetch") and not re.match(r"^[a-zA-Z0-9]{4}$", args.pdb2) else f"fetch {args.pdb2}, {args.name2}, async=0"

    if re.match(r"^[a-zA-Z0-9]{4}$", args.pdb1):
        pdb1_load = f"fetch {args.pdb1}, {args.name1}, async=0"
    else:
        pdb1_load = f"load {args.pdb1}, {args.name1}"

    if re.match(r"^[a-zA-Z0-9]{4}$", args.pdb2):
        pdb2_load = f"fetch {args.pdb2}, {args.name2}, async=0"
    else:
        pdb2_load = f"load {args.pdb2}, {args.name2}"

    pml = f"""
reinitialize

# --- Load structures ---
{pdb1_load}
{pdb2_load}

# --- Clean ---
remove solvent
remove elem H
set valence, 0

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

# --- Align ---
align {args.name2} and name CA, {args.name1} and name CA, cutoff={args.cutoff}

# --- Representation ---
hide everything
show cartoon

color lightblue, {args.name1} and elem C
color salmon, {args.name2} and elem C
util.cnc("{args.name1}", _self=cmd)
util.cnc("{args.name2}", _self=cmd)

# --- Camera ---
orient

# --- Save session ---
save {outdir}/aligned.pse

# --- Render ---
ray 2400, 1800
png {outdir}/aligned.png, dpi=150
quit
"""

    pml_path, output = run_pml(pml, outdir)
    rmsd = parse_rmsd(output)

    # Write RMSD report
    rmsd_path = os.path.join(outdir, "rmsd.txt")
    with open(rmsd_path, "w") as f:
        f.write(f"Alignment: {args.pdb1} vs {args.pdb2}\n")
        f.write(f"Cutoff: {args.cutoff} Angstroms\n")
        if rmsd is not None:
            f.write(f"RMSD: {rmsd:.3f} Angstroms\n")
        else:
            f.write("RMSD: Could not parse from output\n")
            f.write(f"\n--- PyMOL output ---\n{output}")

    png_path = os.path.join(outdir, "aligned.png")
    pse_path = os.path.join(outdir, "aligned.pse")

    print(f"RMSD: {rmsd:.3f}" if rmsd else "RMSD: not found")
    print(f"Output: {png_path}")
    print(f"Session: {pse_path}")
    print(f"RMSD report: {rmsd_path}")

    # Copy to desktop if possible
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", png_path, desktop])
        subprocess.run(["cp", pse_path, desktop])
        print(f"Copied to Desktop")

if __name__ == "__main__":
    main()
