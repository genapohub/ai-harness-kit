# harness v1.11 · 技能仓库一致性规则

> 日期：2026-09-14
> 结论：角色技能以后只在 `ai-harness-kit/skills/` 里维护，同时每个角色技能仍与 GitHub 同名独立仓库保持一致。

## 一、最终口径

`ai-harness-kit/skills/` 是套件内角色技能维护入口。

每个角色技能仍保留独立 GitHub 仓库：

```text
ai-harness-kit/skills/<skill-name>/  <->  https://github.com/genapohub/<skill-name>
```

这两个位置不是两套不同内容，而是同一份技能的套件内嵌版本与独立分发版本。

## 二、为什么这么做

1. 对外用户克隆 `ai-harness-kit` 后，项目根目录天然带完整角色技能，不需要额外安装。
2. 单个技能仍可作为独立仓库维护、传播、更新和复用。
3. 避免重新回到 `00-Skills汇总`、`ai-harness-kit/skills`、单技能仓库三套并行维护。

## 三、维护流程

1. 先修改 `ai-harness-kit/skills/<skill-name>/`。
2. 修改稳定后，同步到 `https://github.com/genapohub/<skill-name>`。
3. 运行：

```bash
bash scripts/refresh-skills.sh
python3 scripts/check-skill-repos.py
```

4. 若一致性检查通过，再提交 `ai-harness-kit`。
5. 重要技能变更需要同步更新 `AGENTS.md` 版本记录并打 `harness-vX.Y` tag。

## 四、验收标准

1. `.ai/SKILLS.md` 能列出当前内置技能与对应独立仓库。
2. 14 个内置技能的同名 GitHub 仓库都可访问。
3. `scripts/check-skill-repos.py` 能检查本地技能与远程技能仓库的内容差异。

---

> _版本：v1.11（2026-09-14）· ai-harness-kit_
