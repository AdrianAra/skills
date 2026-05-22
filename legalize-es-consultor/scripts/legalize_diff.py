#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> int:
    return subprocess.call(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Git diff for a Legalize law file.")
    parser.add_argument("file", help="Path to the Markdown law file")
    parser.add_argument("left", help="Left revision")
    parser.add_argument("right", nargs="?", help="Right revision; defaults to left^")
    parser.add_argument(
        "--repo",
        default=os.environ.get("LEGALIZE_ES_REPO", "."),
        help="Repository path; defaults to LEGALIZE_ES_REPO or current directory",
    )
    parser.add_argument("--stat", action="store_true", help="Show stat only")
    args = parser.parse_args()

    repo = Path(args.repo)
    rel = Path(args.file)
    if rel.is_absolute():
        rel = rel.relative_to(repo)

    right = args.right or f"{args.left}^"
    cmd = ["git", "-C", str(repo), "diff"]
    if args.stat:
        cmd.append("--stat")
    cmd.extend([f"{right}..{args.left}", "--", str(rel)])
    return run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
