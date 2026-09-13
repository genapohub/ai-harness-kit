#!/usr/bin/env python3
"""Check bundled skills against their same-name GitHub repositories."""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
from pathlib import Path

from lib_harness import REPO_ROOT, load_manifest, run, skill_repo


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


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="检查 ai-harness-kit/skills 与 GitHub 同名技能仓库是否一致"
    )
    parser.add_argument("--protocol", choices=("ssh", "https"), default=None)
    parser.add_argument(
        "--https",
        action="store_true",
        help="使用 HTTPS 克隆；等价于 --protocol https",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    protocol = "https" if args.https else (args.protocol or manifest.get("default_protocol", "ssh"))
    skills = manifest["skills"]

    failed = False
    with tempfile.TemporaryDirectory(prefix="ai-harness-skill-repos-") as tmp:
        tmpdir = Path(tmp)
        for skill in skills:
            name = skill["name"]
            local_dir = REPO_ROOT / skill["path"]
            repo = skill_repo(skill, protocol)
            if not (local_dir / "SKILL.md").is_file():
                failed = True
                print(f"FAIL {name}: local skill missing, run python3 scripts/clone-skills.py")
                continue
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
