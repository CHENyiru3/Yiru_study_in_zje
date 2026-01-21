#!/usr/bin/env python3
"""Generate Markdown pages for ZIP packages (contents pages + index).

Repo policy (2026-01): ZIP archives are NOT stored in git.
They should be uploaded externally (e.g. Google Drive / Zenodo), and the website
should only show links/status plus an optional contents listing.

This script supports an optional *local-only* staging folder:

    ZJE_Collection/_incoming_zips/

You may temporarily place ZIPs there to extract their file lists and generate
`ZJE_Collection/zip_contents/*.md`. Do not commit the ZIPs.

Run:
    python3 scripts/generate_zip_listings.py
"""
import os
import zipfile
import re

DOCS_DIR = 'ZJE_Collection'
INCOMING_DIR = os.path.join(DOCS_DIR, '_incoming_zips')
OUT_INDEX = os.path.join(DOCS_DIR, 'ZIPS_INDEX.md')
OUT_DIR = os.path.join(DOCS_DIR, 'zip_contents')

DRIVE_FOLDER_URL = 'https://drive.google.com/drive/folders/1_ttbZASdiHPW9xt0GSjVjFHF5MAPk2fv?usp=drive_link'

def find_zips(root):
    zips = []
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith('.zip'):
                full = os.path.join(dirpath, f)
                zips.append(full)
    return sorted(zips)

def infer_contributor(name):
    m = re.search(r'_([A-Za-z0-9]+(?:_[0-9]{4})?)\.zip$', name)
    if m:
        return m.group(1)
    m2 = re.search(r'_([^_]+)\.zip$', name)
    if m2:
        return m2.group(1)
    return 'unknown'

def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)

def write_listing(zip_path):
    name = os.path.basename(zip_path)
    base = os.path.splitext(name)[0]
    out_md = os.path.join(OUT_DIR, base + '.md')
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            entries = sorted(z.namelist())
    except zipfile.BadZipFile:
        entries = ['(invalid zip file)']

    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(f'# Contents of {name}\n\n')
        f.write(f'Download: hosted externally (see the Google Drive folder linked from [Zips Index](../ZIPS_INDEX.md)).\n\n')
        if not entries:
            f.write('_(zip is empty)_\n')
            return out_md

        # render as tree-like bullets
        prev_parts = []
        for e in entries:
            parts = e.split('/')
            # skip entries that are directory empty names
            if parts and parts[-1] == '':
                # directory entry
                continue
            indent = ''
            for i, p in enumerate(parts):
                if i < len(parts) - 1:
                    # directory
                    pass
                indent = '  ' * i
            f.write(f'- {e}\n')
    return out_md

def write_index(zips):
    ensure_out_dir()
    with open(OUT_INDEX, 'w', encoding='utf-8') as f:
        f.write('# ZIP contributions index\n\n')
        f.write('This file lists zip archives included in the collection, the inferred contributor, and a contents page.\n\n')
        f.write('All large ZIP archives are hosted externally (not stored in this Git repo).\n\n')
        f.write(f'Google Drive folder (all uploads): {DRIVE_FOLDER_URL}\n\n')
        f.write('## Quick index\n\n')
        f.write('| Package (Drive file name) | Contributor | Detail page |\n')
        f.write('|---|---|---|\n')
        for z in zips:
            name = os.path.basename(z)
            contrib = infer_contributor(name)
            base = os.path.splitext(name)[0]
            contents_page = f'zip_contents/{base}.md'
            # ensure contents page exists
            write_listing(z)
            f.write(f'| {name} | {contrib} | [{base}]({contents_page}) |\n')

def main():
    os.makedirs(INCOMING_DIR, exist_ok=True)
    zips = find_zips(INCOMING_DIR)
    if not zips:
        print('No ZIPs found in staging folder:', INCOMING_DIR)
        print('Nothing to do. (This repo does not store ZIPs in git.)')
        return
    write_index(zips)
    print(f'Processed {len(zips)} zip files from {INCOMING_DIR}.')
    print(f'Wrote {OUT_INDEX} and per-zip pages in {OUT_DIR}.')

if __name__ == '__main__':
    main()
