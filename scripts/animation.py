#!/usr/bin/env python3
"""
animation.py — Tweened molecular animation
Usage: python animation.py --pdb 1ubq --frames 60 [--outdir /tmp]
"""

import argparse, os, subprocess, re

def run_pml(pml, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "animation.pml")
    with open(p, "w") as f: f.write(pml)
    r = subprocess.run(["pymol", "-c", "-q", p], capture_output=True, text=True, timeout=300)
    return r.stdout + r.stderr

def is_pdb_id(p): return bool(re.match(r"^[a-zA-Z0-9]{4}$", p))

def main():
    a = argparse.ArgumentParser(description="Generate tweened molecular animation")
    a.add_argument("--pdb", required=True)
    a.add_argument("--frames", type=int, default=60, help="Number of tween frames")
    a.add_argument("--chain", default="")
    a.add_argument("--outdir", default="/tmp/pymol_output")
    a.add_argument("--name", default="protein")
    a.add_argument("--style", default="cartoon", choices=["cartoon", "surface", "spheres"])
    args = a.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    load = f"fetch {args.pdb}, {args.name}, async=0" if is_pdb_id(args.pdb) else f"load {args.pdb}, {args.name}"
    sel = f"({args.name} and chain {args.chain})" if args.chain else args.name

    repr_cmd = {"cartoon": "show cartoon", "surface": "show surface", "spheres": "show spheres"}[args.style]

    pml = f"""
reinitialize
{load}
remove solvent; remove elem H; set valence, 0
bg_color white; space cmyk
set ray_shadow, 0; set ray_trace_mode, 1; set antialias, 3
set ambient, 0.5; set specular, 1; set reflect, 0.1
set orthoscopic, on; set opaque_background, off
dss

{repr_cmd}
util.cnc("all", _self=cmd)

# Set up states for tweening
# State 1: zoomed out overview
zoom {sel}, 0
orient {sel}
mview store, state=1

# State 2: rotate 120 degrees
turn z, 120
mview store, state=2

# State 3: zoom in
zoom {sel}, 2
mview store, state=3

# State 4: return to start
orient {sel}
mview store, state=4

# Tween between states
mview tween, frames={args.frames}, power, loop

# Render animation as PNG sequence
cmd.mset("1 x{args.frames}")

save {outdir}/animation.pse
mpng {outdir}/frame_, delay=50, quiet=1
quit
"""
    run_pml(pml, outdir)
    # Check for frame outputs
    frames = sorted([f for f in os.listdir(outdir) if f.startswith("frame_")])
    if frames:
        print(f"Generated {len(frames)} frames in {outdir}")
        # Also try to make a GIF if ImageMagick is available
        try:
            gif_path = os.path.join(outdir, "animation.gif")
            subprocess.run(
                ["convert", "-delay", "5"] + [os.path.join(outdir, f) for f in frames] + [gif_path],
                capture_output=True, timeout=60
            )
            print(f"GIF: {gif_path}")
        except Exception:
            pass
    print(f"Output frames: {outdir}/frame_*.png")
    print(f"Session: {outdir}/animation.pse")

if __name__ == "__main__":
    main()
