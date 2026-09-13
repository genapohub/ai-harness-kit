#!/usr/bin/env python3
"""Check bundled skills against their same-name GitHub repositories."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path


EXCLUDED_DIRS = {".git", "__pycache__"}
EXCLUDED_FILES = {".DS_Store"}


def iter_files(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            if filename in EXCLUDED_FILES:
                continue
            path = base / filename
            rel = path.relative_to(root).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            files[rel] = digest
    return files


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查 ai-harness-kit/skills 与 GitHub 同名技能仓库是否一致"
    )
    parser.add_argument("--owner", default="genapohub", help="GitHub owner，默认 genapohub")
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="ai-harness-kit 仓库根目录",
    )
    parser.add_argument(
        "--https",
        action="store_true",
        help="使用 HTTPS 克隆；默认使用 SSH，适合私有仓库",
    )
    args = parser.parse_args()

    root = args.repo_root.resolve()
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        print(f"missing skills dir: {skills_dir}")
        return 1

    skill_dirs = sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").is_file())
    if not skill_dirs:
        print("no skills found")
        return 1

    failed = False
    with tempfile.TemporaryDirectory(prefix="ai-harness-skill-repos-") as tmp:
        tmpdir = Path(tmp)
        for local_dir in skill_dirs:
            name = local_dir.name
            repo = (
                f"https://github.com/{args.owner}/{name}.git"
                if args.https
                else f"git@github.com:{args.owner}/{name}.git"
            )
            remote_dir = tmpdir / name
            clone = run(["git", "clone", "--depth", "1", "--quiet", repo, str(remote_dir)])
            if clone.returncode != 0:
                failed = True
                reason = (clone.stderr or clone.stdout).strip().splitlines()[-1:]
                print(f"FAIL {name}: remote inaccessible {reason[0] if reason else ''}")
                continue

            local_files = iter_files(local_dir)
            remote_files = iter_files(remote_dir)
            missing = sorted(set(remote_files) - set(local_files))
            extra = sorted(set(local_files) - set(remote_files))
            changed = sorted(
                path
                for path in set(local_files) & set(remote_files)
                if local_files[path] != remote_files[path]
            )

            if missing or extra or changed:
                failed = True
                print(
                    f"FAIL {name}: missing={len(missing)} extra={len(extra)} changed={len(changed)}"
                )
                for label, values in (
                    ("missing_local", missing[:5]),
                    ("extra_local", extra[:5]),
                    ("changed", changed[:5]),
                ):
                    if values:
                        print(f"  {label}: {', '.join(values)}")
            else:
                print(f"OK {name}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
