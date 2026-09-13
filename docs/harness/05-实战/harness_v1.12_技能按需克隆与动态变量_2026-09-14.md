# harness v1.12 · 技能按需克隆与动态变量

> 日期：2026-09-14
> 结论：`ai-harness-kit` 主仓库不再跟踪 `skills/` 下的角色技能内容；初始克隆后按清单拉取 14 个独立技能仓库。

## 一、调整结论

1. `ai-harness-kit` 主仓库推送时过滤 `skills/` 内容，只保留 `skills/.gitkeep` 占位。
2. 14 个角色技能由 `.ai/skills-manifest.json` 管理。
3. 初始克隆后运行 `python3 scripts/clone-skills.py` 拉取 14 个角色技能。
4. 每个角色技能仍作为独立 GitHub 仓库维护和推送。
5. 项目字段统一采用 `{{VARIABLE_NAME}}` 动态变量。

## 二、任务对话提示机制

AI 进入项目后必须先读：

1. `AGENTS.md`
2. `project-tracker.md`
3. `.ai/SKILLS.md`
4. `.ai/skills-manifest.json`

如果发现 `skills/*/SKILL.md` 不存在或数量不足，先提示并执行：

```bash
python3 scripts/clone-skills.py
```

## 三、技能维护与推送

角色技能本地目录与远程仓库关系：

```text
skills/<skill-name>/  <->  https://github.com/genapohub/<skill-name>
```

单个技能修改后，在对应 `skills/<skill-name>/` 目录内单独 commit。

批量推送全部技能仓库：

```bash
python3 scripts/push-skills.py
```

只检查推送可行性：

```bash
python3 scripts/push-skills.py --dry-run
```

## 四、动态变量

变量样例文件：

```text
.ai/harness.variables.example.json
```

新项目复制为：

```bash
cp .ai/harness.variables.example.json .ai/harness.variables.json
```

检查变量：

```bash
python3 scripts/apply-variables.py --check
```

渲染变量：

```bash
python3 scripts/apply-variables.py
```

`.ai/harness.variables.json` 不进入版本控制。

---

> _版本：v1.12（2026-09-14）· ai-harness-kit_
