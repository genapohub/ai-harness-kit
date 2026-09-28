#!/usr/bin/env python3
"""Initialize or check an ai-harness-kit project root.

This tool is intentionally conservative:
- it creates missing standard directories and .ai memory files;
- it never overwrites existing business files unless --force is used;
- --preview prints actions without writing;
- --check reports missing required files/directories and unresolved {{VARS}}.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

ROOT_FILES = ["AGENTS.md", "project-tracker.md", "SECURITY.md"]
STANDARD_DIRS = [
    "01-竞品分析",
    "02-产品文档",
    "03-技术文档",
    "04-品牌设计",
    "05-UIUX设计",
    "06-项目编码",
    "07-测试用例",
    "08-其它文档",
]
AI_DIRS = [".ai", ".ai/任务日志", ".ai/归档"]
AI_FILES = {
    ".ai/当前状态.md": """# 当前状态

> 跨会话恢复入口。每次任务收尾更新，默认不超过 200 行。

## 项目概况

- 项目名：{{PROJECT_NAME}}
- 当前阶段：{{CURRENT_STAGE}}
- 开发模式：{{DELIVERY_MODE}}
- UI产出方式：{{UI_OUTPUT_MODE}}

## 最近完成

- 待记录

## 进行中

- 待记录

## 风险与阻塞

- 待记录

## 下一步

- 待记录
""",
    ".ai/决策记录.md": """# 决策记录

| 日期 | 决策 | 原因 | 影响 | 来源 |
|---|---|---|---|---|
| {{TODAY}} | 初始化项目记忆 | 建立跨会话恢复入口 | 后续任务按本文件沉淀关键决策 | init_project.py |
""",
    ".ai/经验候选.md": """# 经验候选

> 项目特有经验留在项目内；可复用经验先写入本文件，经确认后再进入 WorkBuddy 主规范或技能仓库。

## 候选模板

- 经验标题：
- 适用条件：
- 来源任务：
- 验证案例：
- 不适用场景：
- 建议去向：继续留在项目 / 确认后进入 WorkBuddy 主规范 / 确认后进入对应技能仓库
""",
}
STARTUP_DOC = """# {{PROJECT_NAME}}_本地启动说明_v1.0

## 结论

本项目采用 PyCharm 整项目窗口启动：直接打开项目根目录，在同一个窗口中管理文档、后端 API、后台前端和小程序/移动端代码。

## 启动配置

| 配置名 | 工作目录 | 启动方式 | 验证 |
|---|---|---|---|
| API FastAPI 8010 | 06-项目编码/<api项目>/ | python -m uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload | http://127.0.0.1:8010/healthz |
| 后台前端 5173 | 06-项目编码/<admin前端项目>/ | npm install 后运行 npm run dev | Vite 端口 5173，代理到 http://127.0.0.1:8010 |
| 小程序/移动端调试 | 06-项目编码/<miniapp或mobile项目>/ | 小程序用微信开发者工具导入；移动端按项目工具链启动 | 开发环境请求后端 8010 或明确测试域名 |

## 启动顺序

1. 打开项目根目录，先读 AGENTS.md、project-tracker.md 和本文件。
2. 启动 API FastAPI 8010，确认 /healthz 健康。
3. 启动 后台前端 5173，确认 Vite proxy 能转发到后端。
4. 再调小程序/移动端。
5. 端口、代理或启动方式变化时，同步更新 AGENTS.md、本文件、前端代理配置、小程序/移动端环境配置和测试说明。

## 排查顺序

先后端 /healthz，再前端代理，再小程序/移动端请求地址。不要在 API 未健康时排查前端或小程序问题。
"""
TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
DEFAULT_VARIABLES = {
    "PROJECT_NAME": "待填写",
    "PROJECT_GOAL": "待填写",
    "TARGET_USERS": "待填写",
    "TECH_STACK": "待决策",
    "REPOSITORY_URL": "待填写",
    "MAIN_BRANCH": "main",
    "DEV_BRANCH": "develop",
    "CURRENT_STAGE": "MVP",
    "DELIVERY_MODE": "待决策",
    "UI_OUTPUT_MODE": "待决策",
    "MVP_SCOPE": "待填写",
    "OUT_OF_SCOPE": "待填写",
    "NORTH_STAR_METRIC": "待填写",
    "AI_TRIGGER_SCOPE": "所有改动",
    "P0_ROLES": "tech-lead-guide / frontend-dev-guide / backend-dev-guide / qa-testing-guide / devops-guide / team-orchestrator",
    "P1_ROLES": "product-plan-guide / ui-designer-guide / data-analyst-guide",
    "P2_ROLES": "growth-guide / monetization-guide / operations-guide / graphic-design-guide / project-mgmt-guide",
    "OWNER_NAME": "待填写",
    "CREATED_DATE": date.today().isoformat(),
    "UPDATED_DATE": date.today().isoformat(),
    "BUSINESS_DOC": "02-产品文档/项目_PRD_v1.0.md",
    "API_DOC": "03-技术文档/API接口契约_v1.0.md",
    "DATA_MODEL_DOC": "03-技术文档/数据模型_v1.0.md",
    "DESIGN_DOC": "05-UIUX设计/页面设计契约_v1.0.md",
    "DEPLOY_DOC": "08-其它文档/部署说明_v1.0.md",
    "PACT_STATUS": "待初始化",
    "PRD_DOC": "待补充",
    "PRD_TODO": "待补充",
    "PAGE_CONTRACT_DOC": "待补充",
    "PAGE_CONTRACT_TODO": "待补充",
    "API_CONTRACT_DOC": "待补充",
    "API_CONTRACT_TODO": "待补充",
    "DATA_MODEL_TODO": "待补充",
    "UI_DOC_OR_CANVAS": "待补充",
    "UI_TODO": "待补充",
    "TEST_EVIDENCE": "待执行",
    "TEST_TODO": "待补充",
    "ACCEPTANCE_REPORT": "未开始",
    "ACCEPTANCE_TODO": "待补充",
    "TODAY": date.today().isoformat(),
}


@dataclass
class Action:
    kind: str
    path: Path
    detail: str


class ProjectInitializer:
    def __init__(self, root: Path, *, preview: bool, force: bool, variables: dict[str, str]):
        self.root = root.resolve()
        self.preview = preview
        self.force = force
        self.variables = variables
        self.actions: list[Action] = []
        self.errors: list[str] = []

    def render(self, text: str) -> str:
        return TOKEN_RE.sub(lambda m: str(self.variables.get(m.group(1), m.group(0))), text)

    def record(self, kind: str, rel: str, detail: str) -> None:
        self.actions.append(Action(kind, self.root / rel, detail))

    def mkdir(self, rel: str) -> None:
        path = self.root / rel
        if path.is_dir():
            return
        self.record("mkdir", rel, "create directory")
        if not self.preview:
            path.mkdir(parents=True, exist_ok=True)

    def write_file(self, rel: str, content: str, *, overwrite: bool = False) -> None:
        path = self.root / rel
        if path.exists() and not (overwrite or self.force):
            return
        detail = "overwrite file" if path.exists() else "create file"
        self.record("write", rel, detail)
        if self.preview:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        rendered = self.render(content)
        atomic_write(path, rendered)

    def ensure_dirs(self) -> None:
        for rel in STANDARD_DIRS + AI_DIRS:
            self.mkdir(rel)

    def ensure_ai_files(self) -> None:
        for rel, content in AI_FILES.items():
            self.write_file(rel, content)
        today_log = f".ai/任务日志/{date.today().isoformat()}.md"
        self.write_file(today_log, f"# {date.today().isoformat()} 任务日志\n\n## 初始化\n\n- 已建立项目记忆日志入口。\n")
        self.write_file(".ai/归档/.gitkeep", "")

    def ensure_variables_file(self) -> None:
        rel = ".ai/harness.variables.json"
        path = self.root / rel
        if path.exists() and not self.force:
            return
        self.record("write", rel, "create variables file" if not path.exists() else "overwrite variables file")
        if not self.preview:
            path.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(path, json.dumps(self.variables, ensure_ascii=False, indent=2) + "\n")

    def ensure_startup_doc(self) -> None:
        self.write_file("03-技术文档/本地启动说明_v1.0.md", STARTUP_DOC)

    def render_existing_templates(self) -> None:
        render_targets = [
            "AGENTS.md",
            "project-tracker.md",
            "SECURITY.md",
            ".github/copilot-instructions.md",
            ".cursor/rules/harness.mdc",
            ".kiro/steering/harness.md",
        ]
        for rel in render_targets:
            path = self.root / rel
            if not path.is_file():
                continue
            original = path.read_text(encoding="utf-8")
            rendered = self.render(original)
            if rendered == original:
                continue
            self.record("render", rel, "replace known {{VARIABLE}} placeholders")
            if not self.preview:
                atomic_write(path, rendered)

    def check(self) -> int:
        missing: list[str] = []
        for rel in STANDARD_DIRS + AI_DIRS + ROOT_FILES:
            if not (self.root / rel).exists():
                missing.append(rel)
        for rel in AI_FILES:
            if not (self.root / rel).exists():
                missing.append(rel)
        unresolved: dict[str, list[str]] = {}
        for rel in ROOT_FILES + [".ai/当前状态.md", "project-tracker.md"]:
            path = self.root / rel
            if path.is_file():
                names = sorted(set(TOKEN_RE.findall(path.read_text(encoding="utf-8"))))
                if names:
                    unresolved[rel] = names
        if missing:
            self.errors.append("missing: " + ", ".join(missing))
        for rel, names in unresolved.items():
            self.errors.append(f"unresolved variables in {rel}: {', '.join(names)}")
        return 1 if self.errors else 0

    def init(self, startup_doc: bool) -> int:
        self.ensure_dirs()
        self.ensure_ai_files()
        self.ensure_variables_file()
        if startup_doc:
            self.ensure_startup_doc()
        self.render_existing_templates()
        return 0


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def load_json(path: Path | None) -> dict[str, str]:
    if not path:
        return {}
    if not path.is_file():
        raise FileNotFoundError(f"vars file not found: {path}")
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.items()}


def parse_set(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"--set must be KEY=VALUE, got: {item}")
        key, value = item.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def print_actions(actions: list[Action]) -> None:
    if not actions:
        print("no changes needed")
        return
    for action in actions:
        print(f"{action.kind}: {action.path} ({action.detail})")


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化或检查 ai-harness-kit 项目根目录")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="项目根目录，默认当前目录")
    parser.add_argument("--vars", type=Path, help="项目变量 JSON 文件")
    parser.add_argument("--set", action="append", default=[], help="覆盖变量，格式 KEY=VALUE，可重复")
    parser.add_argument("--preview", action="store_true", help="只预览将要创建的内容，不写入")
    parser.add_argument("--check", action="store_true", help="只检查缺失文件和未替换变量")
    parser.add_argument("--force", action="store_true", help="允许覆盖脚本管理的模板文件")
    parser.add_argument("--no-startup-doc", action="store_true", help="不创建 03-技术文档/本地启动说明_v1.0.md")
    args = parser.parse_args()

    try:
        variables = DEFAULT_VARIABLES | load_json(args.vars) | parse_set(args.set)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"error: {exc}", file=sys.stderr)
        return 2

    initializer = ProjectInitializer(args.root, preview=args.preview, force=args.force, variables=variables)

    if args.check:
        status = initializer.check()
        if initializer.errors:
            for error in initializer.errors:
                print(error)
        else:
            print("project check passed")
        return status

    status = initializer.init(startup_doc=not args.no_startup_doc)
    print_actions(initializer.actions)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
