#!/usr/bin/env python3
"""
mutation.py — Mutation site structural analysis
Usage: python mutation.py --pdb 1ubq --residue 150 --chain A [--cutoff 5.0] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "mutation.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Visualize mutation site in structural context")
    a.add_argument("--pdb", required=True)
    a.add_argument("--residue", required=True, help="Residue number (e.g., 150)")
    a.add_argument("--chain", default="A")
    a.add_argument("--cutoff", type=float, default=5.0, help="Distance around mutation site")
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    a.add_argument("--mutant", default="ALA", help="Mutant residue to model (default ALA = Alanine scan)")
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"

    # Select the mutation site
    mut_sel = f"chain {args.chain} and resi {args.residue}"
    context_sel = f"(chain {args.chain} and resi {args.residue} around {args.cutoff})"

    pml = f"""
reinitialize
{load}
remove solvent; remove elem H; set valence, 0
bg_color white; space cmyk
set ray_shadow, 0; set ray_trace_mode, 1; set antialias, 3
set ambient, 0.5; set specular, 1; set reflect, 0.1
set orthoscopic, on; set opaque_background, off
dss

# Selections
select mut_site, {mut_sel}
select context, {context_sel} and not mut_site

hide everything

# Context as cartoon
show cartoon, context
util.cnc("context", _self=cmd)

# Mutation site highlighted as sticks + spheres
cmd.show("sticks", "sc. and ({mut_sel})")
cmd.show("spheres", "name CA and ({mut_sel})")

# Color mutation site distinctly (salmon = WT, red = mutation focus)
color lightorange, mut_site
color red, mut_site and elem C

# Label the mutation site
cmd.label(f"({mut_sel}) and name CA", f'\"%s%s\" % (resn, resi)')

# Surrounding surface
create mut_surf, mut_site, zoom=0
show surface, mut_surf
set transparency, 0.7, mut_surf
color lightblue, mut_surf

orient mut_site
zoom mut_site, 8
save {outdir}/mutation.pse
ray 2400, 1800
png {outdir}/mutation.png, dpi=150
quit
"""
    run_pml(pml, outdir)
    print(f"Output: {outdir}/mutation.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/mutation.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/mutation.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
