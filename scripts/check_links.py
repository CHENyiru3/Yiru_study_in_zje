#!/usr/bin/env python3
"""Scan markdown files in ZJE_Collection and report broken relative links."""
import os
import re
import urllib.parse

ROOT = 'ZJE_Collection'

link_re = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def is_local_link(href):
    if href.startswith('http://') or href.startswith('https://'):
        return False
    if href.startswith('mailto:'):
        return False
    if href.startswith('data:'):
        return False
    if href.startswith('blob:'):
        return False
    if href.startswith('#'):
        return False
    return True

def check_file(path):
    missing = []
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    for m in link_re.findall(text):
        href = m[1].strip()
        if not is_local_link(href):
            continue
        # remove anchor
        href_clean = href.split('#')[0]
        href_clean = href_clean.strip()
        # allow Markdown <...> destinations
        if href_clean.startswith('<') and href_clean.endswith('>'):
            href_clean = href_clean[1:-1].strip()
        # decode URL-encoded paths so they can be checked on disk
        href_clean = urllib.parse.unquote(href_clean)
        # consider paths relative to current file
        target = os.path.normpath(os.path.join(os.path.dirname(path), href_clean))
        if not os.path.exists(target):
            missing.append((href, target))
    return missing

def main():
    all_missing = {}
    for dirpath, _, files in os.walk(ROOT):
        for f in files:
            if f.lower().endswith('.md'):
                path = os.path.join(dirpath, f)
                missing = check_file(path)
                if missing:
                    all_missing[path] = missing
    if not all_missing:
        print('No broken local links found.')
        return 0
    for src, items in all_missing.items():
        print('In', src)
        for href, target in items:
            print('  Missing:', href, '->', target)
    return 1

if __name__ == '__main__':
    exit(main())
