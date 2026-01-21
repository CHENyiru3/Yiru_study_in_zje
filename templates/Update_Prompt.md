
# Repo update prompt (copy/paste)

You are updating the repo **Yiru_study_in_zje** (MkDocs Material). The website content is under `ZJE_Collection/`.

Important policies:
- **Do not commit ZIP files** (`.zip` are hosted externally on Google Drive / Zenodo).
- If ZIP packages exist, the repo only keeps **links + a contents/detail page**.

## What changed (fill in)

Date: YYYY-MM-DD

### Added
- Files/folders:
	- `<path>` (type: notes/pdf/other)
- External uploads (Drive/Zenodo):
	- `<package name>.zip` → `<share link or “in Drive folder”>`

### Removed
- Files/folders:
	- `<path>`

### Renamed / moved
- `<old path>` → `<new path>`

## Required repo updates

1) MkDocs nav
- Update `mkdocs.yml` only if a **new course folder** is added.

2) Course landing pages
- Ensure each course folder has `index.md` at:
	- `ZJE_Collection/<Course>/index.md`
- The landing page should link to contributor subfolders (`Yiru/`, `Yue/`, `Xiaoran_etal/`, etc.).

3) ZIP index + detail pages (only when relevant)
- Update `ZJE_Collection/ZIPS_INDEX.md`:
	- Add one row per external ZIP (no local zip paths).
- Update `ZJE_Collection/zip_contents/index.md`:
	- List the ZIP under the correct contributor (e.g. Yue / Xiaoran_etal / Yiru) and link to its detail page.
- Create/update the detail page at:
	- `ZJE_Collection/zip_contents/<zip base name>.md`
	- Include: where to download (Drive folder/link) + a file list / description.

4) Link sanity
- Run the local link checker: `python3 scripts/check_links.py` and fix broken relative links.

## Output expected

- A short summary of files edited/added.
- Any remaining broken links (if any) and where.

