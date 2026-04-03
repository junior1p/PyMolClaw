#!/usr/bin/env python3
"""
goodsell.py — Goodsell-style scientific illustration
Usage: python goodsell.py --pdb 1ubq [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    pml_path = os.path.join(outdir, "goodsell.pml")
    with open(pml_path, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", pml_path], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--pdb", required=True)
    a.add_argument("--chain", default="")
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    a.add_argument("--style", default="spheres", choices=["spheres", "surface"])
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"
    sel = f"{args.name} and chain {args.chain}" if args.chain else args.name

    style_cmd = "show spheres" if args.style == "spheres" else "show surface"

    pml = f"""
reinitialize
{load}
remove solvent; remove elem H

# Goodsell style: flat, no shadows, pastel palette
bg_color white
set ray_trace_mode, 3
set ray_trace_color, black
unset specular
set ray_trace_gain, 0
unset depth_cue
set ambient, 1.0
set direct, 0.0
set reflect, 0.0
set ray_shadow, 0

# Goodsell-inspired pastel colors
set_color gs_blue,   [0.565, 0.714, 0.812]
set_color gs_red,    [0.855, 0.475, 0.427]
set_color gs_green,  [0.631, 0.792, 0.596]
set_color gs_tan,    [0.871, 0.812, 0.682]
set_color gs_orange, [0.871, 0.639, 0.376]

hide everything
{style_cmd}

# Color by chain
color gs_blue,   {sel} and chain A
color gs_red,    {sel} and chain B
color gs_green,  {sel} and chain C
color gs_tan,    {sel} and chain D
color gs_orange, {sel} and elem C and not chain A+B+C+D

orient
save {outdir}/goodsell.pse
ray 2400, 2400
png {outdir}/goodsell.png, dpi=150
quit
"""
    run_pml(pml, outdir)
    print(f"Output: {outdir}/goodsell.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/goodsell.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/goodsell.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
