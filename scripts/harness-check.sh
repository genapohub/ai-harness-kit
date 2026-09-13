#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== Harness root check =="
for file in AGENTS.md project-tracker.md SECURITY.md .ai/SKILLS.md .ai/skills-manifest.json evals/runner.py evals/regression-cases.json; do
  if [ ! -f "$ROOT/$file" ]; then
    echo "missing: $file"
    exit 1
  fi
done

echo "== Skills check =="
MANIFEST_COUNT="$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["skills"]))' "$ROOT/.ai/skills-manifest.json" 2>/dev/null || echo 0)"
LOCAL_COUNT="$(find "$ROOT/skills" -mindepth 2 -maxdepth 2 -name SKILL.md -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "skills manifest: $MANIFEST_COUNT"
echo "skills cloned: $LOCAL_COUNT"
if [ "$LOCAL_COUNT" -lt "$MANIFEST_COUNT" ]; then
  echo "skills not fully cloned; run: python3 scripts/clone-skills.py"
fi

echo "== Evals =="
python3 "$ROOT/evals/runner.py" "$ROOT" --since HEAD~1

echo "all checks passed"
