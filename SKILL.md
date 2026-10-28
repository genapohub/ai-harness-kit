---
name: ai-harness-kit
description: 新项目初始化铺地基。当用户说「初始化新项目 / 开新项目 / 铺项目地基 / 建项目宪法」时启用。分批与用户逐项确认项目背景变量（名称/目标/用户/范围/技术栈/阶段/模式/指标/仓库分支），确认后用脚本生成项目根 AGENTS.md、project-tracker.md、.ai 记忆目录和 8 个标准目录；禁止不经确认替用户编造变量值。
version: 1.0.0
---

# ai-harness-kit：新项目地基初始化

你正在帮哥拿坡初始化一个新软件项目的治理底座。核心理念：**变量逐个确认、绝不编造；用脚本生成、不手工复制；幂等可重跑、不覆盖已有文件。**

## 0. 前置

- 本技能目录即模板源：根下 `AGENTS.md`（项目宪法样板，含 `{{变量}}` 占位符）、`project-tracker.md`、`SECURITY.md`，脚本 `scripts/init_project.py`。
- 通用规则以主真源 `~/Downloads/WorkBuddy/agents.md` 为准；本技能只管新项目初始化这一件事。

## 1. 触发与产出

触发词：初始化新项目 / 开新项目 / 铺项目地基 / 建项目宪法。

产出（在新项目根目录下）：

- `AGENTS.md`（项目宪法，变量已按确认值替换）
- `project-tracker.md`、`SECURITY.md`
- `.ai/`（当前状态.md、决策记录.md、经验候选.md、任务日志/、归档/、harness.variables.json）
- 8 个标准目录（01-竞品分析 … 08-其它文档）
- `03-技术文档/本地启动说明_v1.0.md`

## 2. 交互确认流程（核心，不许跳过）

分 3 批向用户确认变量，**一批问完再下一批**；每批列出「变量名＋含义＋默认值」，用户说"用默认"就填默认。用户没回答的写「待决策／待填写」，**禁止编造**。

**批次 A · 项目身份（必答）**

| 变量 | 含义 |
|---|---|
| PROJECT_NAME | 项目名 |
| PROJECT_GOAL | 项目目标（一句话） |
| TARGET_USERS | 目标用户 |
| MVP_SCOPE | MVP 范围 |
| OUT_OF_SCOPE | 明确不做什么 |

**批次 B · 交付方式**

| 变量 | 含义 | 默认 |
|---|---|---|
| CURRENT_STAGE | 当前阶段（Demo/MVP/V1.0 RC/V1.0 试运营/V2.0） | MVP |
| DELIVERY_MODE | 开发模式（敏捷／瀑布） | 待决策 |
| UI_OUTPUT_MODE | UI 产出方式（Ardot／Figma／不产出设计稿但保留页面契约） | 待决策 |
| NORTH_STAR_METRIC | 北极星指标 | 待填写 |

**批次 C · 工程信息**

| 变量 | 含义 | 默认 |
|---|---|---|
| TECH_STACK | 技术栈 | 待决策 |
| REPOSITORY_URL | 代码仓库 | 待填写 |
| MAIN_BRANCH / DEV_BRANCH | 主干／开发分支 | main / develop |
| 项目根目录位置 | 放在哪 | `~/Downloads/WorkBuddy/<项目名>/` |

auto 权限模式（不能弹提问卡片）时：在回复正文里分批列出问题，等用户文字回答，不静默跳过。

## 3. 生成步骤

1. 确认项目根目录（不存在则创建）。
2. 从本技能目录复制模板到项目根（不覆盖已有文件）：
   `cp -n AGENTS.md project-tracker.md SECURITY.md <项目根>/`
3. 预览（把将创建的内容列给用户确认）：
   `python3 scripts/init_project.py --root <项目根> --set PROJECT_NAME=xxx --set ... --preview`
4. 用户确认后正式执行（去掉 `--preview`）。脚本天然幂等、不覆盖已有业务文件。
5. 校验：`python3 scripts/init_project.py --root <项目根> --check`——必须无 missing；仍残留的 `{{变量}}` 列给用户，说明属「待决策」项，后续在项目根 AGENTS.md 里补。

## 4. 收尾

- 输出就绪报告：已创建的文件／目录、已填变量、待决策变量清单。
- 下一步建议：用 `pact-flow` 初始化契约流程（生成 PACT.md、PRD 骨架）。
- 提醒：项目根 `AGENTS.md` 从此是该项目最高优先级规范；通用规则改动改主真源，不回写项目层。
