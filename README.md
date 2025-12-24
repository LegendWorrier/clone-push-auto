# Clone and set up a repo with PDM

`clone_and_setup.py` clones a public GitHub repo, sets repo-local `git user.name` / `user.email`, and runs `pdm install` to create or refresh the virtual environment.

## Prerequisites
- Git installed and on `PATH`
- PDM installed and on `PATH`
- Python 3.8+ (for running the script)

## Usage
```bash
python clone_and_setup.py https://github.com/org/repo.git \
  --user-name "Your Name" \
  --user-email "you@example.com"
```

Optional: provide a destination directory instead of the default repo name:
```bash
python clone_and_setup.py https://github.com/org/repo.git \
  --user-name "Your Name" \2
  --user-email "you@example.com" \
  --dest /tmp/repo-copy
```

On success the script will:
1. Clone the repo into the target directory
2. Set `git config user.name` and `git config user.email` locally in that repo
3. Run `pdm install` in the repo

