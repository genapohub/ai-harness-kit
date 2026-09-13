#!/usr/bin/env bash
set -euo pipefail

TODAY="$(date +%Y-%m-%d)"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$ROOT/.ai/skills-manifest.json"
INDEX="$ROOT/.ai/SKILLS.md"

python3 - "$MANIFEST" "$INDEX" "$TODAY" <<'PY'
import json
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
index_path = Path(sys.argv[2])
today = sys.argv[3]
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
skills = manifest["skills"]

lines = [
    "# 项目 Skills 清单",
    "",
    "来源: `.ai/skills-manifest.json`",
    "维护方式: 初始克隆不包含 `skills/` 内容；按需运行 `python3 scripts/clone-skills.py` 拉取 14 个独立技能仓库。",
    f"维护日期: {today}",
    f"技能数量: {len(skills)}",
    "",
    "| Skill | 本地路径 | 独立仓库 |",
    "|---|---|---|",
]
for skill in skills:
    lines.append(f"| {skill['name']} | {skill['path']} | {skill['repo_https'][:-4]} |")

index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"skills index refreshed from manifest: {len(skills)}")
PY
