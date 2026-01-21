#!/usr/bin/env bash
set -euo pipefail

echo "Git LFS setup & migration helper for ZJE_Collection"

cat <<'USAGE'
Usage:
  ./scripts/setup_git_lfs.sh          # show dry-run commands
  ./scripts/setup_git_lfs.sh --execute  # perform actions (requires git-lfs installed)

This script does NOT push to remote. It will configure Git LFS tracking and (optionally)
run `git lfs migrate import` to convert existing .zip files into LFS objects (rewrites history).
Make a full mirror backup before running the migrate step.
USAGE

DRY_RUN=true
if [ "${1:-}" = "--execute" ]; then
    DRY_RUN=false
fi

if ! command -v git >/dev/null 2>&1; then
    echo "git not found in PATH. Aborting." >&2
    exit 1
fi

echo
echo "Planned commands:"
echo "-----------------"
echo "git lfs install"
echo "git lfs track 'ZJE_Collection/**/*.zip'"
echo "git add .gitattributes"
echo "git commit -m 'Track zip files with Git LFS'"
echo "git lfs migrate import --include='ZJE_Collection/**/*.zip' --include-ref=refs/heads/main"
echo

if [ "$DRY_RUN" = true ]; then
    echo "This is a dry run. Re-run with --execute to perform the changes."
    exit 0
fi

if ! command -v git-lfs >/dev/null 2>&1; then
    echo "git-lfs not found. Please install it first, e.g. on macOS: 'brew install git-lfs'" >&2
    exit 1
fi

read -p "Have you created a mirror backup of the repo? (yes/NO) " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Please create a backup mirror before proceeding. Aborting." >&2
    echo "Example backup command: git clone --mirror git@github.com:CHENyiru3/Yiru_study_in_zje.git repo-mirror.git"
    exit 1
fi

echo "Running: git lfs install"
git lfs install

echo "Tracking zip files: git lfs track 'ZJE_Collection/**/*.zip'"
git lfs track "ZJE_Collection/**/*.zip"

echo "Staging .gitattributes"
git add .gitattributes || true
if git diff --cached --quiet; then
    echo ".gitattributes already staged or no changes.";
else
    git commit -m "Track zip files with Git LFS"
fi

echo "About to run 'git lfs migrate import' which rewrites history for the included refs."
read -p "Proceed with migrate (this will rewrite history)? (yes/NO) " MIG
if [ "$MIG" != "yes" ]; then
    echo "Migration skipped. You can run: git lfs migrate import --include='ZJE_Collection/**/*.zip' --include-ref=refs/heads/main";
    exit 0
fi

echo "Running migration (may take time)..."
git lfs migrate import --include="ZJE_Collection/**/*.zip" --include-ref=refs/heads/main

echo "Migration complete. Review changes locally. To publish the rewritten history, push with --force after confirming you have backups and team awareness."
echo
echo "Recommended next steps:"
echo "  1) Verify locally (git log, git lfs ls-files)"
echo "  2) Push: git push --force origin main  (only after team confirmation)"
echo "  3) Inform collaborators to run 'git lfs install' before pulling"
