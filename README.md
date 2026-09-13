# ai-harness-kit · AI 编程 Harness 项目根模板

> 后续主线维护仓库：`ai-harness-kit`。
> 目标是一件事：把 AI 编程治理层直接放进项目根目录，让 Claude Code / Cursor / GitHub Copilot / Kiro / Codex 在同一套规则下协作。

## 一、它解决什么问题

`ai-harness-kit` 不是业务代码框架，而是一套项目根目录级 AI 编程治理模板。

它把 4 类资产一次性放进项目：

1. `AGENTS.md`：AI 行为宪法，约束角色、工作流、红线、review。
2. `project-tracker.md`：项目状态单一事实源，记录 WIP、风险、决策、交接。
3. `skills/` + `.ai/SKILLS.md`：项目可用角色技能库。
4. `evals/` + 多工具适配文件：用回归检查和工具规则守住产出质量。

## 二、对外用户怎么用

### 路径 A：新项目，推荐用 GitHub Template

适合：从零创建一个新业务项目。

1. 打开仓库：[https://github.com/genapohub/ai-harness-kit](https://github.com/genapohub/ai-harness-kit)
2. 点击 `Use this template`
3. 创建你的业务项目仓库
4. 克隆新业务仓库到本地
5. 改完下面 3 个文件就可以开工：
   - `AGENTS.md`：项目目标、目标用户、技术栈、AI 角色、红线
   - `project-tracker.md`：当前阶段、WIP、风险、决策
   - `.ai/SKILLS.md`：本项目启用哪些角色技能

### 路径 B：新项目，直接克隆

```bash
git clone https://github.com/genapohub/ai-harness-kit.git your-project
cd your-project
git remote rename origin ai-harness-kit-template
git remote add origin git@github.com:your-org/your-project.git
```

如果你已经配置 SSH，也可以：

```bash
git clone git@github.com:genapohub/ai-harness-kit.git your-project
```

克隆完成后，`your-project/` 就已经是带 AI 编程治理能力的项目根目录，不需要额外执行装机脚本。

### 路径 C：已有项目，复制治理资产

适合：项目已经存在，并且已经有自己的 `.git`。

不要把本仓库直接 clone 到已有项目里面。把下面这些资产复制到已有项目根目录：

```text
AGENTS.md
project-tracker.md
SECURITY.md
.ai/
.claude/
.cursor/
.github/
.kiro/
skills/
evals/
```

复制后先改 3 个入口文件：`AGENTS.md`、`project-tracker.md`、`.ai/SKILLS.md`。

## 三、项目结构

```text
your-project/
├── AGENTS.md                  # AI 行为宪法：项目身份、角色、红线、工作流
├── project-tracker.md         # 项目状态单一事实源：WIP、风险、决策、AI 交接
├── SECURITY.md                # 安全子法：密钥、脱敏、模型路由、事故响应
├── .ai/SKILLS.md              # 项目技能索引
├── .claude/settings.json      # Claude Code 权限建议
├── .cursor/rules/harness.mdc  # Cursor 项目规则
├── .github/                   # Copilot 指令 + PR 模板
├── .kiro/steering/harness.md  # Kiro steering
├── skills/                    # 仓库内置角色技能库，默认内置 14 个技能
├── evals/                     # AI 产出质量回归检查
├── scripts/                   # 维护脚本，日常使用无需先执行
└── docs/harness/              # 05 沉淀 + ai-harness-kit 主线迭代记录
```

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
| 内置角色技能 | `skills/` + `.ai/SKILLS.md` |
| Claude Code 适配 | `.claude/settings.json` |
| Cursor 适配 | `.cursor/rules/harness.mdc` |
| GitHub Copilot 适配 | `.github/copilot-instructions.md` |
| PR 模板 | `.github/pull_request_template.md` |
| Kiro 适配 | `.kiro/steering/harness.md` |
| 质量回归检查 | `evals/runner.py` |
| 历史沉淀 | `docs/harness/` |

使用建议：

1. Claude Code / Codex：进入项目后先读 `AGENTS.md`、`project-tracker.md`、`.ai/SKILLS.md`。
2. Cursor：自动读取 `.cursor/rules/harness.mdc`，同时把 `AGENTS.md` 作为项目规则源。
3. GitHub Copilot：读取 `.github/copilot-instructions.md` 和 PR 模板。
4. Kiro：读取 `.kiro/steering/harness.md`。
5. 团队协作：每次重要变更都同步更新 `project-tracker.md`。

## 六、质量检查

日常使用不需要先跑脚本。需要验收 AI 产出时，可以运行：

```bash
python3 evals/runner.py . --since HEAD~1
```

检查范围包括：

1. Harness 治理三件套是否落位。
2. 是否有明显调试残留。
3. 是否有常见密钥泄露。
4. 新增 commit message 是否符合约定。

## 七、版本

当前版本：`harness-v1.10`

v1.10 变更：

1. 技能主源收敛到 `ai-harness-kit/skills/`，不再依赖外部 `00-Skills汇总`。
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

1. 合并 `05-Harness` 母体资料到 `docs/harness/`。
2. 仓库升级为可直接克隆的项目根目录模板。
3. 默认内置角色技能和多工具适配文件。

## 八、维护原则

1. 以后只维护 `ai-harness-kit`。
2. 不再保留 `05-Harness` / `06-harness-kit` 多套分叉；`08-ai-dev-suite` 原始内容待备份恢复后补入 `ai-harness-kit`。
3. 新项目优先用 GitHub Template 创建。
4. 规则、技能、evals、适配文件都跟项目根目录一起进入版本控制。
5. 每次稳定变更都更新 `AGENTS.md` 版本段，并打 `harness-vX.Y` tag。
