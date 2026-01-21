#!/usr/bin/env python3
"""Create zips for all `Yiru` folders under `ZJE_Collection`.

Creates per-section zips named `<SECTION>_Yiru.zip` and a combined
`Yiru_collection.zip` in `ZJE_Collection/zip_contents/Yiru/`.

Usage:
  python3 scripts/pack_yiru_zips.py

This script does NOT add or commit generated zip files. The target
folder is added to `.gitignore` by default to avoid pushing large files.
"""
import os
import zipfile
from pathlib import Path

ROOT = Path('ZJE_Collection')
OUT_DIR = ROOT / 'zip_contents' / 'Yiru'

def find_yiru_dirs(root: Path):
    ydirs = []
    for dirpath, dirnames, _ in os.walk(root):
        parts = Path(dirpath).parts
        if parts and parts[-1] == 'Yiru':
            ydirs.append(Path(dirpath))
    return sorted(ydirs)

def make_zip_for_dir(yiru_dir: Path, out_dir: Path):
    # section name: parent of Yiru dir
    section = yiru_dir.parent.name
    out_name = f'{section}_Yiru.zip'
    out_path = out_dir / out_name
    print(f'Creating {out_path} from {yiru_dir}')
    with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(yiru_dir):
            for f in files:
                fp = Path(root) / f
                arc = os.path.join(section, fp.relative_to(yiru_dir))
                z.write(fp, arcname=arc)
    return out_path

def make_combined_zip(yiru_dirs, out_dir: Path):
    out_path = out_dir / 'Yiru_collection.zip'
    print(f'Creating combined archive {out_path}')
    with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for y in yiru_dirs:
            section = y.parent.name
            for root, _, files in os.walk(y):
                for f in files:
                    fp = Path(root) / f
                    arc = os.path.join(section, fp.relative_to(y))
                    z.write(fp, arcname=arc)
    return out_path

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ydirs = find_yiru_dirs(ROOT)
    if not ydirs:
        print('No `Yiru` directories found under', ROOT)
        return
    created = []
    for y in ydirs:
        created.append(make_zip_for_dir(y, OUT_DIR))
    created.append(make_combined_zip(ydirs, OUT_DIR))
    print('Created', len(created), 'archives in', OUT_DIR)

if __name__ == '__main__':
    main()
