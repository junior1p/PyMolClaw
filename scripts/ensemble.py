#!/usr/bin/env python3
"""
ensemble.py — NMR / MD trajectory ensemble visualization
Usage: python ensemble.py --pdb 1r55 [--mode nmr|trajectory] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "ensemble.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=180)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Visualize NMR ensemble or MD trajectory")
    a.add_argument("--pdb", required=True)
    a.add_argument("--mode", default="nmr", choices=["nmr", "trajectory"])
    a.add_argument("--states", default="", help="Comma-separated state indices (e.g. '1,2,3') or empty for all")
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="ensemble")
    a.add_argument("--style", default="cartoon", choices=["cartoon", "lines", "spheres"])
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"

    # NMR ensemble: show all models as separate states
    # Trajectory: load frame by frame
    style_cmd = {"cartoon": "show cartoon", "lines": "show lines", "spheres": "show spheres"}[args.style]

    if args.mode == "nmr":
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
{style_cmd}

# NMR: color models differently using states
# Count states
count_states {args.name}

# Color by model index - use a gradient across models
cmd.spectrum("state", "rainbow", "{args.name}")

# Show all models with slight transparency
set transparency, 0.3

orient {args.name}
save {outdir}/ensemble.pse
ray 2400, 1800
png {outdir}/ensemble.png, dpi=150
quit
"""
    else:  # trajectory mode
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
{style_cmd}
util.cnc("{args.name}", _self=cmd)

# Trajectory: show frame 1 of the trajectory
frame 1
smooth

orient {args.name}
save {outdir}/ensemble.pse
ray 2400, 1800
png {outdir}/ensemble.png, dpi=150
quit
"""

    run_pml(pml, outdir)
    print(f"Output: {outdir}/ensemble.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/ensemble.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/ensemble.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
