"""
Utility: convert_svg_to_png.py
Converts project SVG architecture diagrams to ultra high-quality PNGs
using Chromium/Edge headless rendering engine with CairoSVG fallback.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_ASSETS = PROJECT_ROOT / "docs" / "assets"
ARTIFACTS_DIR = Path(r"C:\Users\HELAL\.gemini\antigravity-ide\brain\caa94f56-4f88-4095-bb6c-cf7177e6c9bb")

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

def get_browser_exe():
    for p in EDGE_PATHS:
        if os.path.exists(p):
            return p
    return None

def convert_svg_to_png(svg_path: Path, png_path: Path, width: int = 2400, height: int = 1420):
    svg_abs = str(svg_path.resolve())
    png_abs = str(png_path.resolve())
    browser = get_browser_exe()

    if browser:
        print(f"Rendering via Chromium/Edge: {svg_path.name} -> {png_path.name} ({width}x{height})")
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={width},{height}",
            f"--screenshot={png_abs}",
            f"file:///{svg_abs}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and png_path.exists():
            print(f"[OK] Rendered with Edge Blink engine: {png_path} ({os.path.getsize(png_path)/1024:.1f} KB)")
            return True
        else:
            print(f"[WARN] Edge headless failed with code {result.returncode}, falling back to CairoSVG...")

    try:
        import cairosvg
        print(f"Rendering via CairoSVG: {svg_path.name} -> {png_path.name}")
        cairosvg.svg2png(url=svg_abs, write_to=png_abs, scale=1.0)
        print(f"[OK] Rendered with CairoSVG: {png_path} ({os.path.getsize(png_path)/1024:.1f} KB)")
        return True
    except Exception as e:
        print(f"[ERROR] CairoSVG rendering failed: {e}")
        return False

def main():
    svg_file = DOCS_ASSETS / "project_lifecycle_architecture.svg"
    png_file = DOCS_ASSETS / "project_lifecycle_architecture.png"

    if not svg_file.exists():
        print(f"SVG not found: {svg_file}")
        sys.exit(1)

    success = convert_svg_to_png(svg_file, png_file, width=2400, height=1440)
    if success:
        # Also copy to artifacts directory for interactive display
        if ARTIFACTS_DIR.exists():
            dest_artifact = ARTIFACTS_DIR / "project_lifecycle_architecture.png"
            shutil.copy(png_file, dest_artifact)
            print(f"[OK] Copied to conversation artifacts: {dest_artifact}")

    # Also convert enterprise galaxy architecture if available
    galaxy_svg = DOCS_ASSETS / "enterprise_galaxy_architecture.svg"
    galaxy_png = DOCS_ASSETS / "enterprise_galaxy_architecture.png"
    if galaxy_svg.exists():
        success_galaxy = convert_svg_to_png(galaxy_svg, galaxy_png, width=2400, height=1440)
        if success_galaxy and ARTIFACTS_DIR.exists():
            shutil.copy(galaxy_png, ARTIFACTS_DIR / "enterprise_galaxy_architecture.png")
            print(f"[OK] Copied to conversation artifacts: {ARTIFACTS_DIR / 'enterprise_galaxy_architecture.png'}")

if __name__ == "__main__":
    main()
