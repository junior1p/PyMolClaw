#!/usr/bin/env python3
"""
active_site.py — Catalytic/active site analysis
Usage: python active_site.py --pdb 1abc --residues "100,150,200" --chain A [--cutoff 5.0] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "active_site.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Visualize active site / catalytic residues")
    a.add_argument("--pdb", required=True)
    a.add_argument("--residues", required=True, help="Comma-separated residue numbers (e.g., '100,150,200')")
    a.add_argument("--chain", default="A")
    a.add_argument("--cutoff", type=float, default=5.0)
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"

    # Parse residues
    resi_list = [r.strip() for r in args.residues.split(",")]
    resi_sel = "+".join(resi_list)
    cat_sel = f"chain {args.chain} and resi {resi_sel}"

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
select catalytic, {cat_sel}
select cat_env, byres (catalytic around {args.cutoff}) and not catalytic

hide everything

# Environment as semi-transparent cartoon
show cartoon, cat_env
set cartoon_transparency, 0.7
util.cnc("cat_env", _self=cmd)

# Catalytic residues as sticks + ball-and-stick
cmd.show("sticks", "sc. and ({cat_sel})")
cmd.show("ball", "n. CA and ({cat_sel})")

# Label catalytic residues
cmd.label(f"({cat_sel}) and name CA", f'\"%s%s\" % (resn, resi)')

# Polar contacts between catalytic residues
dist cat_contacts, catalytic, catalytic, mode=2
hide labels, cat_contacts
set dash_color, black
set dash_gap, 0.3
set dash_radius, 0.06

# Surface around active site
create cat_surf, catalytic, zoom=0
show surface, cat_surf
set transparency, 0.6, cat_surf

orient catalytic
zoom catalytic, 10
save {outdir}/active_site.pse
ray 2400, 1800
png {outdir}/active_site.png, dpi=150
quit
"""
    run_pml(pml, outdir)
    print(f"Output: {outdir}/active_site.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/active_site.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/active_site.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
