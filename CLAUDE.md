# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collaborative study notes repository for ZJE (Zhejiang University-University of Edinburgh Institute) students, published as a static website using MkDocs with the Material theme. The site contains course materials organized by year (Year 1-4) covering various courses like CHEM1, IBMS1, ADS2, MBE3, IID_4, etc.

## Commands

```bash
# Install dependencies
pip install mkdocs-material

# Start local development server (auto-reloads on changes)
mkdocs serve

# Build static site to output directory
mkdocs build --site-dir site

# Check links before committing
python3 scripts/check_links.py

# Generate ZIP package listings (auto-runs in CI)
python3 scripts/generate_zip_listings.py
```

## Architecture

- **Content**: `ZJE_Collection/` - Markdown files organized by course directories
- **Config**: `mkdocs.yml` - MkDocs configuration with Material theme and navigation
- **Scripts**: `scripts/` - Python utilities for link checking and ZIP listing generation
- **Templates**: `templates/` - Note templates for contributors

## Key Conventions

**Branch naming**: `notes/<course>-<yourname>-<year>` for contribution branches

**File naming**: `<Topic> (<course>) (<author_suffix>_<year>).md`

**ZIP files**: Never commit ZIP files to the repository. Host externally (Google Drive) and add entries to `ZJE_Collection/ZIPS_INDEX.md` with a detail page in `ZJE_Collection/zip_contents/`

**Contribution workflow**: Fork → create feature branch → add/edit files using `templates/note_template.md` → submit PR using `.github/PULL_REQUEST_TEMPLATE.md`

**Note template**: Use `templates/note_template.md` when adding new notes (includes required metadata: Author, Course, Year, Source)

## CI/CD

- GitHub Actions deploys to GitHub Pages on push to `main`
- `update-zip-listings.yml` runs daily and on PRs to auto-generate ZIP index pages
