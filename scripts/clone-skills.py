#!/usr/bin/env python3
"""Clone the 14 role-skill repositories listed in .ai/skills-manifest.json."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path

from lib_harness import REPO_ROOT, load_manifest, run, skill_repo


EXCLUDED_DIRS = {".git", "__pycache__"}
EXCLUDED_FILES = {".DS_Store"}


def iter_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            if filename in EXCLUDED_FILES:
                continue
            path = base / filename
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def main() -> int:
    parser = argparse.ArgumentParser(description="克隆 ai-harness-kit 的 14 个角色技能仓库")
    parser.add_argument("--protocol", choices=("ssh", "https"), default=None)
    parser.add_argument("--update", action="store_true", help="已存在 git 仓库时执行 pull --ff-only")
    parser.add_argument(
        "--adopt-existing",
        action="store_true",
        help="本地已有非 git 技能目录且内容与远程一致时，挂接远程 .git 元数据",
    )
    parser.add_argument("skills", nargs="*", help="可选：只处理指定技能名")
    args = parser.parse_args()

    manifest = load_manifest()
    protocol = args.protocol or manifest.get("default_protocol", "ssh")
    selected = set(args.skills)
    skills = [s for s in manifest["skills"] if not selected or s["name"] in selected]
    missing_names = selected - {s["name"] for s in skills}
    if missing_names:
        print("unknown skills: " + ", ".join(sorted(missing_names)))
        return 1

    failed = False
    for skill in skills:
        name = skill["name"]
        target = REPO_ROOT / skill["path"]
        repo = skill_repo(skill, protocol)

        if (target / ".git").is_dir():
            if args.update:
                result = run(["git", "pull", "--ff-only"], cwd=target)
                if result.returncode != 0:
                    failed = True
                    print(f"FAIL {name}: pull failed")
                    print((result.stderr or result.stdout).strip())
                else:
                    print(f"OK {name}: updated")
            else:
                print(f"OK {name}: already cloned")
            continue

        if target.exists() and any(target.iterdir()):
            if not args.adopt_existing:
                failed = True
                print(f"FAIL {name}: local directory exists, use --adopt-existing after checking content")
                continue
            with tempfile.TemporaryDirectory(prefix=f"ai-harness-adopt-{name}-") as tmp:
                tmp_repo = Path(tmp) / name
                clone = run(["git", "clone", "--quiet", repo, str(tmp_repo)])
                if clone.returncode != 0:
                    failed = True
                    print(f"FAIL {name}: clone failed")
                    print((clone.stderr or clone.stdout).strip())
                    continue
                if iter_hashes(target) != iter_hashes(tmp_repo):
                    failed = True
                    print(f"FAIL {name}: local content differs from remote, sync manually first")
                    continue
                shutil.move(str(tmp_repo / ".git"), str(target / ".git"))
                print(f"OK {name}: adopted existing directory")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        clone = run(["git", "clone", "--quiet", repo, str(target)])
        if clone.returncode != 0:
            failed = True
            print(f"FAIL {name}: clone failed")
            print((clone.stderr or clone.stdout).strip())
        else:
            print(f"OK {name}: cloned")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
