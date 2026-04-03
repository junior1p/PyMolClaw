#!/usr/bin/env python3
"""
ppi.py — Protein-Protein Interaction interface
Usage: python ppi.py --pdb 6m0j --chain_a A --chain_b B [--cutoff 4.0] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "ppi.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--pdb", required=True)
    a.add_argument("--chain_a", required=True, help="First chain ID")
    a.add_argument("--chain_b", required=True, help="Second chain ID")
    a.add_argument("--cutoff", type=float, default=4.0)
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="complex")
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    pml = f"""
reinitialize
fetch {args.pdb}, {args.name}, async=0
remove solvent; remove elem H; set valence, 0

select chainA, chain {args.chain_a}
select chainB, chain {args.chain_b}
select iface_A, byres (chainA within {args.cutoff} of chainB)
select iface_B, byres (chainB within {args.cutoff} of chainA)

bg_color white; space cmyk
set ray_shadow, 0; set ray_trace_mode, 1; set antialias, 3
set ambient, 0.5; set specular, 1; set reflect, 0.1
set orthoscopic, on; set opaque_background, off
set cartoon_oval_length, 1; set cartoon_rect_length, 1
dss

hide everything; show cartoon
color lightblue, chainA and elem C; color lightorange, chainB and elem C
util.cnc("all", _self=cmd)

cmd.show("sticks", "((byres iface_A) & (sc. | n. CA))")
cmd.show("sticks", "((byres iface_B) & (sc. | n. CA))")

create surf_A, iface_A, zoom=0; show surface, surf_A
set transparency, 0.6, surf_A; color lightblue, surf_A
create surf_B, iface_B, zoom=0; show surface, surf_B
set transparency, 0.6, surf_B; color lightorange, surf_B

orient
zoom iface_A or iface_B, 8
save {outdir}/ppi.pse
ray 2400, 1800
png {outdir}/ppi.png, dpi=150
quit
"""
    run_pml(pml, outdir)
    print(f"Output: {outdir}/ppi.png")

if __name__ == "__main__":
    main()
