#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TODAY="$(date +%Y-%m-%d)"
SKILLS_DIR="$ROOT/skills"
INDEX="$ROOT/.ai/SKILLS.md"

[ -d "$SKILLS_DIR" ] || { echo "内置 skills 目录不存在: $SKILLS_DIR"; exit 1; }

mkdir -p "$ROOT/.ai"

installed=()
while IFS= read -r skill_file; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  installed+=("$skill_name")
done < <(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name SKILL.md -type f | sort)

{
  echo "# 项目已安装 Skills"
  echo ""
  echo "来源: 仓库内置 skills/（ai-harness-kit 自维护，不再依赖外部 00-Skills 汇总）"
  echo "维护日期: $TODAY"
  echo "技能数量: ${#installed[@]}"
  echo ""
  echo "| Skill | 本地路径 | 独立仓库 |"
  echo "|---|---|---|"
  for name in "${installed[@]}"; do
    echo "| $name | skills/$name | https://github.com/genapohub/$name |"
  done
} > "$INDEX"

echo "skills index refreshed: ${#installed[@]}"
