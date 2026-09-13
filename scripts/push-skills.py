#!/usr/bin/env python3
"""Push each local role-skill repository separately."""

from __future__ import annotations

import argparse
import sys

from lib_harness import REPO_ROOT, current_branch, load_manifest, run


def main() -> int:
    parser = argparse.ArgumentParser(description="逐个推送 ai-harness-kit/skills 下的独立技能仓库")
    parser.add_argument("--dry-run", action="store_true", help="只检查，不实际 push")
    parser.add_argument("--allow-dirty", action="store_true", help="允许有未提交变更时仍尝试 push")
    parser.add_argument("skills", nargs="*", help="可选：只处理指定技能名")
    args = parser.parse_args()

    manifest = load_manifest()
    selected = set(args.skills)
    skills = [s for s in manifest["skills"] if not selected or s["name"] in selected]
    missing_names = selected - {s["name"] for s in skills}
    if missing_names:
        print("unknown skills: " + ", ".join(sorted(missing_names)))
        return 1

    failed = False
    for skill in skills:
        name = skill["name"]
        repo_dir = REPO_ROOT / skill["path"]
        if not (repo_dir / ".git").is_dir():
            failed = True
            print(f"FAIL {name}: not cloned, run python3 scripts/clone-skills.py first")
            continue

        status = run(["git", "status", "--porcelain"], cwd=repo_dir)
        dirty = bool(status.stdout.strip())
        if dirty and not args.allow_dirty:
            failed = True
            print(f"FAIL {name}: dirty working tree, commit skill changes first")
            continue

        branch = current_branch(repo_dir)
        if not branch:
            failed = True
            print(f"FAIL {name}: cannot determine branch")
            continue

        cmd = ["git", "push", "--dry-run" if args.dry_run else "origin", branch]
        if args.dry_run:
            cmd = ["git", "push", "--dry-run", "origin", branch]
        result = run(cmd, cwd=repo_dir)
        if result.returncode != 0:
            failed = True
            print(f"FAIL {name}: push failed")
            print((result.stderr or result.stdout).strip())
        else:
            print(f"OK {name}: {'dry-run ' if args.dry_run else ''}pushed {branch}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
