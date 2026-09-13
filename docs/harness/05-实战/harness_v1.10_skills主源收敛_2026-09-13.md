# harness v1.10 · Skills 主源收敛记录

> 日期：2026-09-13
> 结论：`ai-harness-kit` 内置 `skills/` 成为套件内角色技能维护入口，不再依赖外部 `00-Skills汇总` 同步。v1.11 补充：每个角色技能仍保留 GitHub 同名独立仓库，并要求保持一致。

## 一、调整背景

外部 `00-Skills汇总` 中的技能内容与 `ai-harness-kit/skills/` 重复，继续两边保留会造成：

1. 技能版本漂移。
2. README 与 `.ai/SKILLS.md` 口径不一致。
3. 对外用户误以为还需要本地额外装机或同步。

## 二、调整结论

1. 删除重复技能后，当前仓库内置技能数量为 14 个。
2. `.ai/SKILLS.md` 改为从仓库自身 `skills/` 生成索引。
3. `scripts/refresh-skills.sh` 改为本仓库内索引刷新脚本，不再从外部目录复制技能。
4. README、AGENTS、project-tracker 更新到 v1.10 口径。

## 三、当前内置技能

1. `backend-dev-guide`
2. `data-analyst-guide`
3. `devops-guide`
4. `frontend-dev-guide`
5. `graphic-design-guide`
6. `growth-guide`
7. `monetization-guide`
8. `operations-guide`
9. `product-plan-guide`
10. `project-mgmt-guide`
11. `qa-testing-guide`
12. `team-orchestrator`
13. `tech-lead-guide`
14. `ui-designer-guide`

## 四、维护规则

以后新增、删除或更新角色技能时，先维护 `ai-harness-kit/skills/`。更新完成后运行：

```bash
bash scripts/refresh-skills.sh
```

该脚本只刷新 `.ai/SKILLS.md` 索引，不再复制外部技能目录。

v1.11 补充规则：`skills/<skill-name>/` 与 `https://github.com/genapohub/<skill-name>` 必须保持一致。

---

> _版本：v1.10（2026-09-13）· ai-harness-kit_
