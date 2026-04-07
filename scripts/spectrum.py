#!/usr/bin/env python3
"""
spectrum.py — B-factor / pLDDT / property spectrum coloring
Usage: python spectrum.py --pdb 1ubq --property bfactor|plddt|occupancy [--palette blue_white_red] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "spectrum.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Spectrum coloring by B-factor, pLDDT, or other properties")
    a.add_argument("--pdb", required=True)
    a.add_argument("--property", dest="prop", default="bfactor",
                   choices=["bfactor", "plddt", "occupancy", "charge"])
    a.add_argument("--palette", default="blue_white_red",
                   choices=["blue_white_red", "blue_green_red", "rainbow", "red_white_blue"])
    a.add_argument("--chain", default="")
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    a.add_argument("--style", default="cartoon", choices=["cartoon", "spheres", "sticks"])
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"
    sel = f"({args.name} and chain {args.chain})" if args.chain else args.name

    repr_cmd = {"cartoon": "show cartoon", "spheres": "show spheres", "sticks": "show sticks"}[args.style]

    pml = f"""
reinitialize
{load}
remove solvent; remove elem H; set valence, 0
bg_color white; space cmyk
set ray_shadow, 0; set ray_trace_mode, 1; set antialias, 3
set ambient, 0.5; set specular, 1; set reflect, 0.1
set orthoscopic, on; set opaque_background, off
dss

hide everything
{repr_cmd}

# Spectrum coloring
spectrum {args.prop}, {args.palette}, f"{sel}"

# Show CA atoms as spheres for better visibility
cmd.show("spheres", f"name CA and ({sel})")
set sphere_scale, 0.5

orient {sel}
save {outdir}/spectrum.pse
ray 2400, 1800
png {outdir}/spectrum.png, dpi=150
quit
"""
    run_pml(pml, outdir)
    print(f"Output: {outdir}/spectrum.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/spectrum.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/spectrum.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
