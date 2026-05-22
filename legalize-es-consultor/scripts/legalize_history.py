#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> int:
    return subprocess.call(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Git history for a Legalize law file.")
    parser.add_argument("file", help="Path to the Markdown law file")
    parser.add_argument(
        "--repo",
        default=os.environ.get("LEGALIZE_ES_REPO", "."),
        help="Repository path; defaults to LEGALIZE_ES_REPO or current directory",
    )
    parser.add_argument("--limit", type=int, default=20, help="Number of log entries")
    parser.add_argument("--commit", help="Specific commit to inspect")
    parser.add_argument("--show-diff", action="store_true", help="Show the commit diff")
    args = parser.parse_args()

    repo = Path(args.repo)
    rel = Path(args.file)
    if rel.is_absolute():
        rel = rel.relative_to(repo)

    rc = run(["git", "-C", str(repo), "log", "--oneline", f"--max-count={args.limit}", "--", str(rel)])
    if rc != 0:
        return rc

    commit = args.commit
    if not commit and args.show_diff:
        proc = subprocess.run(
            ["git", "-C", str(repo), "log", "--format=%H", "-n", "1", "--", str(rel)],
            text=True,
            capture_output=True,
            check=False,
        )
        commit = proc.stdout.strip() or None

    if commit and args.show_diff:
        return run(["git", "-C", str(repo), "show", "--stat", "--summary", commit, "--", str(rel)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
