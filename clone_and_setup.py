#!/usr/bin/env python3
"""
Clone a public GitHub repo, set repo-local git user, and run `pdm install`.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clone a public GitHub repo, set git user, and run `pdm install`."
    )
    parser.add_argument(
        "repo_url",
        help="Public GitHub repository URL (e.g., https://github.com/user/project.git)",
    )
    parser.add_argument(
        "--user-name",
        required=True,
        help="Git user.name to set locally in the cloned repo",
    )
    parser.add_argument(
        "--user-email",
        required=True,
        help="Git user.email to set locally in the cloned repo",
    )
    parser.add_argument(
        "--dest",
        help="Optional destination directory; defaults to the repo name from the URL",
    )
    return parser.parse_args()


def ensure_tool(tool: str) -> None:
    if shutil.which(tool) is None:
        raise RuntimeError(f"Required tool '{tool}' is not installed or not on PATH")


def derive_repo_dir(repo_url: str) -> Path:
    parsed = urlparse(repo_url)
    tail = Path(parsed.path.rstrip("/")).name
    if not tail:
        raise ValueError("Could not derive repository name from URL")
    if tail.endswith(".git"):
        tail = tail[:-4]
    if not tail:
        raise ValueError("Repository name resolved to empty after stripping .git")
    return Path(tail)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        msg = f"Command failed: {' '.join(cmd)}"
        if stdout:
            msg += f"\nstdout:\n{stdout}"
        if stderr:
            msg += f"\nstderr:\n{stderr}"
        raise RuntimeError(msg)


def clone_repo(repo_url: str, dest: Path) -> None:
    if dest.exists():
        raise FileExistsError(f"Destination already exists: {dest}")
    run(["git", "clone", repo_url, str(dest)])


def set_git_config(repo_dir: Path, user_name: str, user_email: str) -> None:
    run(["git", "config", "user.name", user_name], cwd=repo_dir)
    run(["git", "config", "user.email", user_email], cwd=repo_dir)


def run_pdm_install(repo_dir: Path) -> None:
    run(["pdm", "install"], cwd=repo_dir)


def main() -> int:
    args = parse_args()

    ensure_tool("git")
    ensure_tool("pdm")

    repo_dir = Path(args.dest) if args.dest else derive_repo_dir(args.repo_url)
    repo_dir = repo_dir.resolve()

    try:
        print(f"Cloning {args.repo_url} into {repo_dir} ...")
        clone_repo(args.repo_url, repo_dir)

        print("Setting local git user.name/email ...")
        set_git_config(repo_dir, args.user_name, args.user_email)

        print("Running `pdm install` ...")
        run_pdm_install(repo_dir)

        print("Done.")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

