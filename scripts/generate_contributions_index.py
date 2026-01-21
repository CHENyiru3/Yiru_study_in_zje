#!/usr/bin/env python3
"""Scan ZJE_Collection for .zip files and generate ZIPS_INDEX.md.
Run from repository root: `python3 scripts/generate_contributions_index.py`
"""
import os
import re

DOCS_DIR = 'ZJE_Collection'
OUT_FILE = os.path.join(DOCS_DIR, 'ZIPS_INDEX.md')

def find_zips(root):
    zips = []
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith('.zip'):
                rel = os.path.relpath(os.path.join(dirpath, f), start='.')
                zips.append(rel.replace('\\\\', '/'))
    return sorted(zips)

def infer_contributor(name):
    # Try to capture trailing handle like _lxrwyqlxf or _lxrwyalxf
    m = re.search(r'_([A-Za-z0-9]+(?:_[0-9]{4})?)\.zip$', name)
    if m:
        return m.group(1)
    # fallback: any token between last '_' and '.zip'
    m2 = re.search(r'_([^_]+)\.zip$', name)
    if m2:
        return m2.group(1)
    return 'unknown'

def write_index(zips):
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('# ZIP contributions index\n')
        f.write('\n')
        f.write('This file lists zip archives included in the collection and the inferred contributor.\n')
        f.write('\n')
        f.write('| File | Contributor | Location |\n')
        f.write('|---|---|---|\n')
        for z in zips:
            contrib = infer_contributor(z)
            # link path relative to docs
            link = z
            f.write(f'| [{os.path.basename(z)}]({link}) | {contrib} | {z} |\n')

def main():
    zips = find_zips(DOCS_DIR)
    write_index(zips)
    print(f'Wrote {OUT_FILE} with {len(zips)} entries')

if __name__ == '__main__':
    main()
