#!/usr/bin/env python3
"""Apply ai-harness-kit governance shell to a target project.

Two modes:
  --full  (default): copy the full governance asset set (constitution + multi-endpoint
                     adapters + evals + maintenance scripts). Render project variables
                     from <target>/.ai/harness.variables.json when present.
  --lite:           only lay down the governance three-piece (AGENTS.md /
                     project-tracker.md / SECURITY.md) + evals audit. Does NOT clone
                     the 14 role-skill repos, does NOT force-fill all variables — only
                     {{PROJECT_NAME}} is substituted when --name is given.

  --with-gate:      additionally drop a ready-to-use GitHub Actions PR gate
                    (.github/workflows/evals-gate.yml) that runs the evals runner.

This is the flexible replacement for the removed install.sh: lite-first for most
adopters, full when you want the whole harness surface.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from lib_harness import REPO_ROOT


# lite = 治理三件套 + evals 审计，不碰 .ai（技能清单/变量）/ 多端适配 / 维护脚本
LITE_DIRS = ["evals"]
LITE_FILES = ["AGENTS.md", "project-tracker.md", "SECURITY.md"]

# full = 完整治理壳 + 多端适配 + 维护脚本
FULL_DIRS = [".ai", "evals", ".claude", ".cursor", ".github", ".kiro", "scripts"]
FULL_FILES = ["AGENTS.md", "project-tracker.md", "SECURITY.md"]

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

# 复制治理资产时跳过的条目
SKIP_NAMES = {".DS_Store", "__pycache__", "reports"}
SKIP_DIRS = {".git"}

GATE_TEMPLATE = REPO_ROOT / "scripts" / "templates" / "evals-gate.yml"
GATE_DEST = Path(".github") / "workflows" / "evals-gate.yml"

TEXT_SUFFIXES = {".md", ".mdc", ".json", ".yml", ".yaml", ".py", ".txt", ""}


def render(text: str, values: dict[str, str]) -> str:
    if not values:
        return text
    return TOKEN_RE.sub(lambda m: str(values.get(m.group(1), m.group(0))), text)


def copy_file(src: Path, dst: Path, values: dict[str, str], force: bool) -> str:
    if dst.exists() and not force:
        return f"skip (exists): {dst}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(render(src.read_text(encoding="utf-8"), values), encoding="utf-8")
    return f"copy: {dst}"


def _copy_tree(src: Path, dst: Path, values: dict[str, str], force: bool, actions: list[str]) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in sorted(src.rglob("*")):
        rel = item.relative_to(src)
        # 跳过整个目录子树（reports / .git / .DS_Store 等）：任一层级命中即整支排除
        if any(part in SKIP_NAMES or part in SKIP_DIRS for part in rel.parts):
            continue
        if item.is_dir():
            (dst / rel).mkdir(parents=True, exist_ok=True)
            continue
        target_item = dst / rel
        if target_item.exists() and not force:
            actions.append(f"skip (exists): {dst.name}/{rel.as_posix()}")
            continue
        target_item.parent.mkdir(parents=True, exist_ok=True)
        if item.suffix in TEXT_SUFFIXES:
            target_item.write_text(render(item.read_text(encoding="utf-8"), values), encoding="utf-8")
        else:
            shutil.copyfile(item, target_item)
        actions.append(f"copy: {dst.name}/{rel.as_posix()}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="把 ai-harness-kit 治理壳应用到目标项目（lite/full 双形态）"
    )
    parser.add_argument("target", nargs="?", default=".", help="目标项目根目录，默认当前目录")
    parser.add_argument("--lite", action="store_true", help="只铺治理三件套 + evals，不克隆 14 仓、不强制填变量")
    parser.add_argument("--full", dest="lite", action="store_false",
                        help="完整治理壳 + 多端适配 + 维护脚本（默认）")
    parser.add_argument("--name", default=None,
                        help="项目名，用于替换 {{PROJECT_NAME}}（lite 模式唯一必填变量）")
    parser.add_argument("--vars", default=None, type=Path,
                        help="full 模式：变量 JSON 文件，默认 <target>/.ai/harness.variables.json")
    parser.add_argument("--with-gate", action="store_true", help="附带 GitHub Actions PR 门禁（evals-gate.yml）")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    parser.add_argument("--dry-run", action="store_true", help="只打印将要执行的动作，不写文件")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if target == REPO_ROOT:
        print("refuse: target 不能等于 kit 自身（REPO_ROOT），请指定目标项目目录")
        return 1

    # 按模式构造变量值
    values: dict[str, str] = {}
    if args.lite:
        if args.name:
            values["PROJECT_NAME"] = args.name
    else:
        vpath = args.vars or (target / ".ai" / "harness.variables.json")
        if vpath.is_file():
            try:
                values = json.loads(vpath.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                print(f"warn: 变量文件解析失败，按原始模板复制：{exc}")
        if args.name:
            values["PROJECT_NAME"] = args.name

    dirs = LITE_DIRS if args.lite else FULL_DIRS
    files = LITE_FILES if args.lite else FULL_FILES

    actions: list[str] = []
    for rel in dirs:
        src = REPO_ROOT / rel
        dst = target / rel
        if not src.exists():
            continue
        if args.dry_run:
            actions.append(f"[dry-run] sync dir: {rel}/ -> {dst}/")
            continue
        if dst.exists() and not args.force:
            actions.append(f"skip (exists): {rel}/")
            continue
        if dst.exists():
            shutil.rmtree(dst)
        _copy_tree(src, dst, values, args.force, actions)

    for rel in files:
        src = REPO_ROOT / rel
        dst = target / rel
        if not src.is_file():
            continue
        if args.dry_run:
            actions.append(f"[dry-run] copy file: {rel} -> {dst}")
            continue
        actions.append(copy_file(src, dst, values, args.force))

    gate_msg = ""
    if args.with_gate:
        if not GATE_TEMPLATE.is_file():
            gate_msg = "warn: 找不到门禁模板 scripts/templates/evals-gate.yml，跳过 --with-gate"
        else:
            gdst = target / GATE_DEST
            if args.dry_run:
                actions.append(f"[dry-run] write gate: {gdst}")
            elif gdst.exists() and not args.force:
                gate_msg = f"skip (exists): {GATE_DEST}"
            else:
                gdst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(GATE_TEMPLATE, gdst)
                gate_msg = f"gate: {GATE_DEST}"

    print(f"mode: {'lite' if args.lite else 'full'}")
    print(f"target: {target}")
    for a in actions:
        print("  " + a)
    if gate_msg:
        print("  " + gate_msg)

    if args.dry_run:
        print("(dry-run 结束，未写入任何文件)")
        return 0

    print("")
    if args.lite:
        print("下一步：")
        print("  1. 编辑 AGENTS.md / project-tracker.md / SECURITY.md 填项目信息")
        print("  2. 验收 AI 产出：python3 evals/runner.py . --since HEAD~1")
        if not args.with_gate:
            print("  3. 想要 PR 门禁：重新运行加 --with-gate")
    else:
        print("下一步：")
        print("  1. cp .ai/harness.variables.example.json .ai/harness.variables.json 并填值")
        print("  2. python3 scripts/apply-variables.py 渲染变量")
        print("  3. python3 scripts/clone-skills.py 按需拉取角色技能仓库")
        print("  4. python3 evals/runner.py . --since HEAD~1 验收")
    return 0


if __name__ == "__main__":
    sys.exit(main())
