# Git LFS migration plan

This document explains how to safely migrate existing large ZIP files under `ZJE_Collection` to Git LFS.

1) Backup (mandatory)

- Create a mirror backup of the repository before changing history:

```bash
git clone --mirror git@github.com:CHENyiru3/Yiru_study_in_zje.git repo-mirror.git
```

2) Install Git LFS

- macOS (Homebrew):

```bash
brew install git-lfs
git lfs install
```

3) Dry-run & preview (recommended)

- The helper script `scripts/setup_git_lfs.sh` prints the planned commands by default.

```bash
./scripts/setup_git_lfs.sh
```

4) Execute migration (rewrites history)

- After backup, run:

```bash
./scripts/setup_git_lfs.sh --execute
```

- The script will ask you to confirm you have a backup and confirm running the migrate step.

5) Push rewritten history (manual, careful)

- After migration, verify locally. If everything is correct, force-push the branch:

```bash
git push --force origin main
```

Warning: rewriting history and force-pushing will require collaborators to re-clone or follow recovery steps. Coordinate with any co-contributors.

6) Alternative: host large zips externally

- If you prefer not to use Git LFS, upload the ZIPs to external storage (Drive/Dropbox/GitHub Releases) and remove them from repo history instead.
