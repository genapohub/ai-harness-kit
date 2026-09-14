# harness v1.13 · 技能默认 HTTPS 克隆

> 日期：2026-09-14
> 结论：14 个角色技能默认使用公开 HTTPS 克隆，维护者需要推送时可选择 SSH remote。

## 一、调整原因

`ai-harness-kit` 面向外部用户时，第一次使用不应要求用户先配置 SSH key。

14 个角色技能仓库当前均可公开 HTTPS 访问，因此 `.ai/skills-manifest.json` 的默认克隆协议调整为 `https`。

## 二、使用方式

外部用户首次拉取技能：

```bash
python3 scripts/clone-skills.py
```

维护者需要推送技能仓库：

```bash
python3 scripts/clone-skills.py --protocol ssh
python3 scripts/push-skills.py
```

## 三、验收标准

1. 初始克隆 `ai-harness-kit` 后，`skills/` 只包含 `.gitkeep`。
2. 默认运行 `python3 scripts/clone-skills.py` 使用 HTTPS 克隆 14 个技能。
3. 维护者可用 `--protocol ssh` 克隆技能仓库并独立推送。

---

> _版本：v1.13（2026-09-14）· ai-harness-kit_
