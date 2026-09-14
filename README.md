# ai-harness-kit · AI 编程 Harness 项目根模板

> 后续主线维护仓库：`ai-harness-kit`。
> 目标是一件事：把 AI 编程治理层直接放进项目根目录，让 Claude Code / Cursor / GitHub Copilot / Kiro / Codex 在同一套规则下协作。
>
> English version → [README.en.md](README.en.md)

## 一、它解决什么问题

`ai-harness-kit` 不是业务代码框架，而是一套项目根目录级 AI 编程治理模板。

它把 4 类资产一次性放进项目：

1. `AGENTS.md`：AI 行为宪法，约束角色、工作流、红线、review。
2. `project-tracker.md`：项目状态单一事实源，记录 WIP、风险、决策、交接。
3. `.ai/skills-manifest.json` + `.ai/SKILLS.md`：项目可用角色技能清单。
4. `evals/` + 多工具适配文件：用回归检查和工具规则守住产出质量。

## 二、怎么用：克隆到你的项目根目录

对外只有一条使用方式——**把本仓库克隆成你的项目根目录**。克隆下来即为可用形态，不需要执行任何装机脚本。

```bash
git clone https://github.com/genapohub/ai-harness-kit.git your-project
cd your-project
git remote rename origin ai-harness-kit-template
git remote add origin git@github.com:your-org/your-project.git
```

也可以从 GitHub 上点 `Use this template` 创建自己的项目仓库，效果等同（本质仍是克隆一份副本）。

已经配置 SSH 的话：

```bash
git clone git@github.com:genapohub/ai-harness-kit.git your-project
```

想固定版本而不是跟随最新改动（版本列表见 §九）：

```bash
git clone -b harness-v1.18 https://github.com/genapohub/ai-harness-kit.git your-project
```

### 克隆后第一步：拉取角色技能

初始克隆不包含 `skills/` 下的角色技能内容（主仓库只保留 `.gitkeep` 占位）。首次任务对话或开工前运行一次：

```bash
python3 scripts/clone-skills.py
```

维护者若要把技能仓库克隆成 SSH remote 方便后续推送：

```bash
python3 scripts/clone-skills.py --protocol ssh
```

### 克隆后第二步：改三个入口文件

改 `AGENTS.md` / `project-tracker.md` / `.ai/SKILLS.md` 三处即可开工，每个文件写什么见 §四。

### 例外：项目已存在

已经有自己的 `.git` 的存量项目，不要直接把本仓库 clone 进去（会打乱原有历史）。改用脚本把治理资产注入现有项目根目录：

```bash
# 轻量（推荐）：只铺治理三件套 + evals，不克隆 14 仓、不强制填变量
python3 scripts/init-harness.py --lite --name "你的项目名" /path/to/your-project
python3 scripts/init-harness.py --lite --name "你的项目名" --with-gate /path/to/your-project

# 完整：额外带上多端适配文件与维护脚本
python3 scripts/init-harness.py --full /path/to/your-project
```

- 已存在的文件默认跳过不覆盖；加 `--force` 强制覆盖；加 `--dry-run` 先预览会动什么。
- `--with-gate` 额外写入 `.github/workflows/evals-gate.yml`（观察期 `continue-on-error`，稳定后删该行变硬门禁）。
- 不想跑脚本，也可以按 §三 项目结构把资产逐个复制过去，再改上面三个入口文件。
- 脚本**不会**自动克隆 14 个角色技能仓库，需要时单独跑 `python3 scripts/clone-skills.py`。

## 三、项目结构

```text
your-project/
├── AGENTS.md                  # AI 行为宪法：项目身份、角色、红线、工作流
├── project-tracker.md         # 项目状态单一事实源：WIP、风险、决策、AI 交接
├── SECURITY.md                # 安全子法：密钥、脱敏、模型路由、事故响应
├── .ai/SKILLS.md              # 项目技能清单
├── .ai/skills-manifest.json   # 14 个角色技能仓库清单
├── .ai/harness.variables.example.json # 项目动态变量样例
├── .claude/settings.json      # Claude Code 权限建议
├── .cursor/rules/harness.mdc  # Cursor 项目规则
├── .github/                   # Copilot 指令 + PR 模板
├── .kiro/steering/harness.md  # Kiro steering
├── skills/                    # 初始为空，按需克隆 14 个独立角色技能仓库
├── evals/                     # AI 产出质量回归检查
├── scripts/                   # 维护脚本，日常使用无需先执行
└── docs/harness/              # Harness 方法论速览（可选），外部项目可删
```

> `docs/` 只是方法论参考，**不是运行必需的**，外部项目可以直接删掉。

## 四、开工前只需要改三处

1. `AGENTS.md`：项目目标、目标用户、技术栈、当前阶段。
2. `project-tracker.md`：当前阶段总览、WIP、风险、决策日志。
3. `.ai/SKILLS.md`：确认本项目启用哪些角色技能。

## 五、不同 AI 工具怎么读

| 能力 | 文件 |
|---|---|
| AI 行为规范 | `AGENTS.md` |
| 项目状态持久化 | `project-tracker.md` |
| 安全红线 | `SECURITY.md` |
| 角色技能清单 | `.ai/skills-manifest.json` + `.ai/SKILLS.md` |
| Claude Code 适配 | `.claude/settings.json` |
| Cursor 适配 | `.cursor/rules/harness.mdc` |
| GitHub Copilot 适配 | `.github/copilot-instructions.md` |
| PR 模板 | `.github/pull_request_template.md` |
| Kiro 适配 | `.kiro/steering/harness.md` |
| 质量回归检查 | `evals/runner.py` |
| 方法论参考（可选） | `docs/harness/` |

使用建议：

1. Claude Code / Codex：进入项目后先读 `AGENTS.md`、`project-tracker.md`、`.ai/SKILLS.md`。
2. Cursor：自动读取 `.cursor/rules/harness.mdc`，同时把 `AGENTS.md` 作为项目规则源。
3. GitHub Copilot：读取 `.github/copilot-instructions.md` 和 PR 模板。
4. Kiro：读取 `.kiro/steering/harness.md`。
5. 团队协作：每次重要变更都同步更新 `project-tracker.md`。

## 六、角色技能维护

`ai-harness-kit` 主仓库推送时过滤 `skills/` 内容，只保留 `skills/.gitkeep` 占位。初始克隆后，按清单拉取 14 个同名独立技能仓库：

```bash
python3 scripts/clone-skills.py
```

以后任务对话里，如果 AI 发现 `skills/` 为空或缺少 `SKILL.md`，必须先提示并执行上面的克隆动作，再使用角色技能。

角色技能维护入口仍是本地 `ai-harness-kit/skills/<skill-name>/`，但每个角色技能都作为同名 GitHub 仓库单独维护和推送：

```text
skills/frontend-dev-guide  <->  https://github.com/genapohub/frontend-dev-guide
skills/backend-dev-guide   <->  https://github.com/genapohub/backend-dev-guide
```

维护规则：

1. 修改角色技能时，先改 `ai-harness-kit/skills/<skill-name>/`。
2. 在对应技能目录里单独 commit 并 push 到 `https://github.com/genapohub/<skill-name>`。
3. 回到 `ai-harness-kit` 主仓库，运行 `bash scripts/refresh-skills.sh` 刷新 `.ai/SKILLS.md`。
4. 运行 `python3 scripts/check-skill-repos.py` 检查本地技能与同名远程仓库是否一致。
5. `ai-harness-kit` 主仓库只提交清单、脚本和治理文件，不提交 `skills/<skill-name>/` 内容。

批量推送技能仓库：

```bash
python3 scripts/push-skills.py
```

只检查不推送：

```bash
python3 scripts/push-skills.py --dry-run
```

如果技能目录是用 HTTPS 克隆的，推送需要 GitHub 登录凭据；维护者更推荐用 `python3 scripts/clone-skills.py --protocol ssh` 克隆技能仓库。

## 七、动态变量

模板里的项目字段统一使用 `{{VARIABLE_NAME}}` 占位。新项目从样例复制一份变量文件：

```bash
cp .ai/harness.variables.example.json .ai/harness.variables.json
```

填好后检查变量是否完整：

```bash
python3 scripts/apply-variables.py --check
```

需要把变量渲染进当前项目文件时运行：

```bash
python3 scripts/apply-variables.py
```

## 八、质量检查

日常使用不需要先跑脚本。需要验收 AI 产出时，可以运行：

```bash
python3 evals/runner.py . --since HEAD~1
```

检查范围（runner v0.4，对应 regression-cases.json 全部 14 个 case）：

- **Harness 治理**：harness-001 治理三件套（AGENTS.md / project-tracker.md / SECURITY.md）是否落位
- **代码质量**：code-001 命名规范（Python snake_case / 文件名无空格）· code-002 无遗留调试代码（console.log / debugger / print，deploy/scripts/test_/migrate_ 豁免）· code-003 测试覆盖率（结构代理：测试基础设施是否就位）
- **规范遵守**：spec-001 不调用黑名单工具（rm -rf /、git push --force、擅改 CI workflow）· spec-002 PR 描述完整性（本地仅查 PR 模板，逐字段需 CI/forge）· spec-003 commit message 规范（conventional 前缀 + 首行 ≤72）
- **文档质量**：doc-001 PRD 结构 · doc-002 API 文档结构 · doc-003 技术选型/设计文档决策可追溯
- **AI 协作**：collab-001 跨角色上下文交接（project-tracker 含「AI 协作上下文」）· collab-002 角色冲突升级（含「决策日志」）
- **安全合规**：security-001 无密钥泄露 · security-002 敏感数据脱敏（客户数据文件中无明文手机号/身份证号）

> 提示：doc / spec-002 / code-003 为「结构/代理检查」，命中=待人工复核的基线项，不一定是硬伤；历史存量告警按 regression-cases.json 豁免策略处理，增量模式（`--since`）守护新增。

### PR 门禁（evals-gate）

想要把质量检查变成合并前的硬约束，把仓库里的工作流模板复制到项目：

```bash
mkdir -p .github/workflows
cp scripts/templates/evals-gate.yml .github/workflows/evals-gate.yml
```

它在 PR 或 push 到 `main` 时自动执行 `python3 evals/runner.py . --since HEAD~1`。默认 `continue-on-error: true`（只收集基线、不挡合并）；观察几轮、确认误报都已豁免后，删掉那一行即变硬门禁。

> 存量项目走「例外」路径时，用 `init-harness.py --with-gate` 可以直接写入同一个文件。

技能仓库一致性检查：

```bash
python3 scripts/check-skill-repos.py
```

## 九、版本

当前版本：`harness-v1.18`

v1.18 变更：

1. **对外使用方式收敛为单一路径**：统一为「直接克隆到项目根目录」，删除原路径 A / B / C 三分法；`Use this template` 作为等价快捷方式保留一句说明。
2. `init-harness.py` 从对外主路径撤下，降为「项目已存在」这一例外场景的治理资产注入工具，不再作为装机步骤出现。
3. 版本固定示例与 §二 的克隆命令同步更新。

v1.17 变更：

1. **去除模板中的个人数据**：`project-tracker.md` 责任人字段、`AGENTS.md` 变更条目等处的个人名/项目名统一通用化，模板不再夹带任何个人字段。
2. `docs/harness/` 对外只保留一份通用《方法论速览》（README.md）；维护者的调研笔记、工具脚本、实战记录全部移出主干（`.gitignore` 忽略，本地保留），不再随模板分发。
3. 中英文 README 的 `docs/` 描述同步更新。

v1.16 变更：

1. 对外发布整洁化：维护者自身项目实战记录移出主干，本地保留、不再随模板分发。
2. 新增 `README.en.md` 英文版，降低非中文用户上手门槛。
3. 修复 README「路径 C 复制清单」与「项目结构」不一致：清单现列出 `docs/`，并标注为可选。
4. 新增版本固定说明：克隆时可用 `git clone -b harness-vX.Y` 锁定版本（此前默认只能跟随最新）。

v1.15 变更：

1. 新增 `scripts/init-harness.py`：把治理壳应用到目标项目，支持 `--lite`（只铺治理三件套 + evals，不克隆 14 仓、不强制填变量）与 `--full`（完整资产集）双形态。
2. 新增 `scripts/templates/evals-gate.yml`：可一键生成的 GitHub Actions PR 门禁，PR/push 时跑 evals runner，`--with-gate` 写入目标仓库。
3. 轻量模式是 kit 最灵活的入口，替代被移除的 install.sh：lite-first，多数团队无需克隆 14 仓即可上手治理。

v1.14 变更：

1. `evals/runner.py` 升级 v0.4，补全 14 个 case 实现（此前仅 4 个），详见 AGENTS.md 附录 C。

v1.13 变更：

1. 14 个角色技能默认使用公开 HTTPS 克隆，降低外部用户首次使用门槛。
2. 维护者需要推送技能仓库时，可通过 `python3 scripts/clone-skills.py --protocol ssh` 使用 SSH remote。

v1.12 变更：

1. `ai-harness-kit` 主仓库推送过滤 `skills/` 内容，只保留技能清单与空目录占位。
2. 初始克隆后通过 `python3 scripts/clone-skills.py` 拉取 14 个独立技能仓库。
3. 新增 `scripts/push-skills.py`，支持 14 个角色技能独立仓库逐个推送。
4. 新增 `.ai/harness.variables.example.json` 与 `scripts/apply-variables.py`，统一项目动态变量字段。

v1.11 变更：

1. 明确 `ai-harness-kit/skills/` 是角色技能维护入口。
2. 明确每个角色技能仍与 GitHub 同名独立仓库保持一致。
3. 新增 `scripts/check-skill-repos.py`，检查内置技能与独立仓库内容差异。
4. `.ai/SKILLS.md` 增加独立仓库链接列。

v1.10 变更：

1. 技能主源收敛到 `ai-harness-kit/skills/`，不再依赖外部目录。
2. `.ai/SKILLS.md` 按当前 14 个内置技能重建索引。
3. `scripts/refresh-skills.sh` 改为从仓库自身 `skills/` 生成技能索引。

v1.9 变更：

1. README 重写为对外用户使用版。
2. 明确 GitHub Template、直接克隆、已有项目复制三条使用路径。
3. GitHub 仓库开启 Template repository。

v1.8 变更：

1. 本地与远程仓库统一命名为 `ai-harness-kit`。
2. 克隆地址切换为 `git@github.com:genapohub/ai-harness-kit.git`。
3. README、AGENTS、project-tracker、SECURITY、evals 元信息统一更换为新名称。

v1.7 变更：

1. 后续维护主线当时切到 `ai-governance-example`，v1.8 已统一更名为 `ai-harness-kit`。
2. 使用方式收敛为“直接克隆到项目根目录”，不再要求执行装机命令。
3. README 去掉克隆后的自检命令，把脚本降为维护工具。
4. 标记 08 原始目录待备份恢复后再补融合。

v1.6 变更：

1. 合并早期 Harness 资料到 `docs/harness/`。
2. 仓库升级为可直接克隆的项目根目录模板。
3. 默认内置角色技能和多工具适配文件。

## 十、维护原则

1. 以后只维护 `ai-harness-kit`。
2. 不再保留多套分叉；所有治理资产统一收敛到 `ai-harness-kit`。
3. 新项目优先用 GitHub Template 创建。
4. 规则、技能、evals、适配文件都跟项目根目录一起进入版本控制。
5. 每次稳定变更都更新 `AGENTS.md` 版本段，并打 `harness-vX.Y` tag。
