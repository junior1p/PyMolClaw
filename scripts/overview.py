#!/usr/bin/env python3
"""
overview.py — General protein structure overview
Usage: python overview.py --pdb 1ubq [--style cartoon|surface|ribbon] [--chain A] [--outdir /tmp]
"""

import argparse
import os
import subprocess
import re

def run_pml(pml_content, outdir):
    os.makedirs(outdir, exist_ok=True)
    pml_path = os.path.join(outdir, "overview.pml")
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
    parser = argparse.ArgumentParser(description="Generate protein overview figure")
    parser.add_argument("--pdb", required=True, help="PDB ID or local file path")
    parser.add_argument("--style", default="cartoon", choices=["cartoon", "surface", "ribbon", "sticks"], help="Visualization style")
    parser.add_argument("--chain", default="", help="Chain ID to focus on")
    parser.add_argument("--outdir", default="/tmp/pymol_output", help="Output directory")
    parser.add_argument("--name", default="protein", help="Object name")
    parser.add_argument("--width", type=int, default=2400, help="Ray width")
    parser.add_argument("--height", type=int, default=1800, help="Ray height")
    args = parser.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    # Load command
    if is_pdb_id(args.pdb):
        load_cmd = f"fetch {args.pdb}, {args.name}, async=0"
    else:
        load_cmd = f"load {args.pdb}, {args.name}"

    selection = args.name
    if args.chain:
        selection = f"({args.name} and chain {args.chain})"

    # Representation settings
    repr_map = {
        "cartoon": "show cartoon",
        "surface": "show surface",
        "ribbon": "show ribbon",
        "sticks": "show sticks; show cartoon, not elem C",
    }
    repr_cmd = repr_map.get(args.style, "show cartoon")

    pml = f"""
reinitialize

# --- Load ---
{load_cmd}

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

# --- Representation ---
hide everything
{repr_cmd}

# --- Color ---
util.color_chains("(all) and elem C", _self=cmd)
util.cnc("all", _self=cmd)

# --- Camera ---
orient {selection}

# --- Save session ---
save {outdir}/overview.pse

# --- Render ---
ray {args.width}, {args.height}
png {outdir}/overview.png, dpi=150
quit
"""

    pml_path, output = run_pml(pml, outdir)

    png_path = os.path.join(outdir, "overview.png")
    pse_path = os.path.join(outdir, "overview.pse")

    print(f"Output: {png_path}")
    print(f"Session: {pse_path}")

    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", png_path, desktop], capture_output=True)
        subprocess.run(["cp", pse_path, desktop], capture_output=True)
        print(f"Copied to Desktop")

if __name__ == "__main__":
    main()
