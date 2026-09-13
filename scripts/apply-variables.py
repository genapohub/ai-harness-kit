#!/usr/bin/env python3
"""Render project variables into template files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from lib_harness import REPO_ROOT


DEFAULT_FILES = [
    "AGENTS.md",
    "project-tracker.md",
    "SECURITY.md",
    ".github/copilot-instructions.md",
    ".cursor/rules/harness.mdc",
    ".kiro/steering/harness.md",
]


TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def main() -> int:
    parser = argparse.ArgumentParser(description="用 .ai/harness.variables.json 渲染项目动态变量")
    parser.add_argument(
        "--vars",
        default=REPO_ROOT / ".ai" / "harness.variables.json",
        type=Path,
        help="变量文件，默认 .ai/harness.variables.json",
    )
    parser.add_argument("--check", action="store_true", help="只检查未填变量，不写文件")
    parser.add_argument("files", nargs="*", help="可选：指定要渲染的文件")
    args = parser.parse_args()

    if not args.vars.is_file():
        print(f"missing vars file: {args.vars}")
        print("copy .ai/harness.variables.example.json to .ai/harness.variables.json first")
        return 1

    values = json.loads(args.vars.read_text(encoding="utf-8"))
    files = args.files or DEFAULT_FILES
    missing: dict[str, list[str]] = {}

    for rel in files:
        path = REPO_ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        needed = sorted(set(TOKEN_RE.findall(text)) - set(values))
        if needed:
            missing[rel] = needed
            continue
        if not args.check:
            path.write_text(TOKEN_RE.sub(lambda m: str(values[m.group(1)]), text), encoding="utf-8")

    if missing:
        for rel, names in missing.items():
            print(f"missing values in {rel}: {', '.join(names)}")
        return 1

    print("variables check passed" if args.check else "variables applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
