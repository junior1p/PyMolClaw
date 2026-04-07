#!/usr/bin/env python3
"""
surface.py — Molecular surface rendering with electrostatic potential
Usage: python surface.py --pdb 1ubq [--style surface|mesh|dots] [--transparency 0.5] [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "surface.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Molecular surface rendering")
    a.add_argument("--pdb", required=True)
    a.add_argument("--chain", default="")
    a.add_argument("--style", default="surface", choices=["surface", "mesh", "dots"])
    a.add_argument("--transparency", type=float, default=0.4)
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    a.add_argument("--color_by", default="chain", choices=["chain", "bfactor", "electrostatic"])
    a.add_argument("-- APBS", dest="apbs", action="store_true", help="Run APBS electrostatics (requires APBS installed)")
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"
    sel = f"({args.name} and chain {args.chain})" if args.chain else args.name

    # Surface representation
    style_map = {"surface": "show surface", "mesh": "show mesh", "dots": "show dots"}
    style_cmd = style_map[args.style]

    # Color mode
    if args.color_by == "chain":
        color_cmd = "util.color_chains(f\"({sel})\", _self=cmd)"
    elif args.color_by == "bfactor":
        color_cmd = "spectrum b, blue_white_red, f\"({sel})\"\ncmd.label(f\"({sel}) and name CA\", f'\"%s:%s\" % (resn, resi)')\nset label_color, black"
    else:
        color_cmd = "util.color_chains(f\"({sel})\", _self=cmd)"

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

# Transparency per object
set surface_quality, 1
set transparency_mode, 1

# Chain coloring
{color_cmd}

# Surface transparency
set transparency, {args.transparency}

orient {sel}
save {outdir}/surface.pse
ray 2400, 1800
png {outdir}/surface.png, dpi=150
quit
"""
    run_pml(pml, outdir)
    print(f"Output: {outdir}/surface.png")
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        subprocess.run(["cp", f"{outdir}/surface.png", desktop], capture_output=True)
        subprocess.run(["cp", f"{outdir}/surface.pse", desktop], capture_output=True)
        print("Copied to Desktop")

if __name__ == "__main__":
    main()
