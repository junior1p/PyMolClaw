#!/usr/bin/env python3
"""
distance.py — Distances and polar contacts measurement
Usage: python distance.py --pdb 1abc --sele1 "chain A and resi 100" --sele2 "chain B and resi 200" [--mode hbond] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "distance.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Measure distances and polar contacts")
    a.add_argument("--pdb", required=True)
    a.add_argument("--sele1", required=True, help="First selection (PyMOL syntax, e.g. 'chain A and resi 100')")
    a.add_argument("--sele2", required=True, help="Second selection")
    a.add_argument("--mode", default="hbond", choices=["hbond", "polar", "all"])
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    a.add_argument("--label", action="store_true", default=True, help="Show distance labels")
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"

    mode_cmd = {"hbond": "mode=2", "polar": "mode=1", "all": "mode=0"}[args.mode]

    pml = f"""
reinitialize
{load}
remove solvent; remove elem H; set valence, 0
bg_color white; space cmyk
set ray_shadow, 0; set ray_trace_mode, 1; set antialias, 3
set ambient, 0.5; set specular, 1; set reflect, 0.1
set orthoscopic, on; set opaque_background, off
set cartoon_oval_length, 1; set cartoon_rect_length, 1
dss

hide everything
show cartoon
util.cnc("all", _self=cmd)

# Selections
select s1, {args.sele1}
select s2, {args.sele2}

# Show selections as sticks
cmd.show("sticks", "sc. and (s1 or s2)")
cmd.show("spheres", "name CA and (s1 or s2)")

# Distance measurement
dist d1, s1, s2, {mode_cmd}
set dash_color, black
set dash_gap, 0.3
set dash_radius, 0.08

# Show polar contacts if mode supports
dist polars, s1, s2, mode=2
hide labels, polars
set dash_color, red, polars
set dash_gap, 0.2
set dash_radius, 0.05

# Label distance value
cmd.label("d1", f'\"%.2f A\" % dist')

orient s1
zoom s1 or s2, 12
save {outdir}/distance.pse
ray 2400, 1800
png {outdir}/distance.png, dpi=150
quit
"""
    output = run_pml(pml, outdir)

    # Parse distances from output
    dist_matches = re.findall(r"Distances:\s+(.*?)(?:\n\n|\Z)", output, re.IGNORECASE)
    print(f"Output: {outdir}/distance.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/distance.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/distance.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
