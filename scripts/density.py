#!/usr/bin/env python3
"""
density.py — Electron density / EM map / Cryo-EM visualization
Usage: python density.py --pdb 1abc --map 1abc_2fofc.ccp4 [--level 1.5] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "density.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Visualize electron density or EM maps")
    a.add_argument("--pdb", required=True, help="PDB ID or local file")
    a.add_argument("--map", default="", help="Density map file (CCP4/MRC format). If omitted, fetches from Uppsala ED server.")
    a.add_argument("--level", type=float, default=1.5, help="Contour level (sigma for EM, usually 1.0-2.0)")
    a.add_argument("--map_type", default="2fofc", choices=["2fofc", "fofc", "em"])
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    a.add_argument("--map_color", default="gray70", help="Density mesh color")
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    if is_pdb_id(args.pdb):
        load_cmd = f"fetch {args.pdb}, {args.name}, async=0"
        if not args.map:
            # Auto-fetch from Uppsala Electron Density server
            fetch_map = f"fetch {args.pdb}_2fofc, type=2fofc, dest={args.name}_2fofc, object={args.name}_map, state=1"
        else:
            fetch_map = f"load {args.map}, {args.name}_map"
    else:
        load_cmd = f"load {args.pdb}, {args.name}"
        fetch_map = f"load {args.map}, {args.name}_map" if args.map else ""

    pml = f"""
reinitialize
{load_cmd}

# Load density map
{fetch_map}

remove solvent; remove elem H; set valence, 0
bg_color white; space cmyk
set ray_shadow, 0; set ray_trace_mode, 1; set antialias, 3
set ambient, 0.5; set specular, 1; set reflect, 0.1
set orthoscopic, on; set opaque_background, off
dss

hide everything

# Protein representation
show cartoon, {args.name}
util.cnc("{args.name}", _self=cmd)

# Density map as mesh
cmd.isomesh({args.name}_mesh, {args.name}_map, {args.level})
cmd.color("{args.map_color}", {args.name}_mesh)

orient {args.name}
save {outdir}/density.pse
ray 2400, 1800
png {outdir}/density.png, dpi=150
quit
"""
    run_pml(pml, outdir)
    print(f"Output: {outdir}/density.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/density.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/density.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
