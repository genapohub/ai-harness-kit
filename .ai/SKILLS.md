# 项目 Skills 清单

技能数量: 2
来源: `.ai/skills-manifest.json`
维护日期: 2026-09-28

> 当前只维护常用流程技能：`software-dev-team` 与 `pact-flow`。
> 任务对话中若 AI 发现 `skills/*/SKILL.md` 缺失，先提示按下节命令拉取后再开工。

## 一、拉取常用技能

在项目根目录执行：

```bash
git clone https://github.com/genapohub/software-dev-team.git skills/software-dev-team
git clone https://github.com/genapohub/pact-flow.git skills/pact-flow
```

已配置 SSH 时，可使用：

```bash
git clone git@github.com:genapohub/software-dev-team.git skills/software-dev-team
git clone git@github.com:genapohub/pact-flow.git skills/pact-flow
```

拉取后确认 `skills/<name>/SKILL.md` 存在，即可使用对应能力。

## 二、技能清单

| Skill | 本地路径 | 独立仓库 | 用途 |
|---|---|---|---|
| software-dev-team | skills/software-dev-team | https://github.com/genapohub/software-dev-team | 软件开发团队编排：MVP、产品迭代、BugFix、交付闭环 |
| pact-flow | skills/pact-flow | https://github.com/genapohub/pact-flow | 契约化交付：PRD、页面契约、API 契约、Mock、联调验收 |

## 三、本项目启用技能

- [x] 软件开发团队 software-dev-team
- [x] 契约化交付流程 pact-flow

## 四、扩展说明

如果某个项目后续确实需要独立角色技能，再单独登记到本文件和 `.ai/skills-manifest.json`。默认新项目不拉取 14 个角色技能，避免换机恢复和项目初始化过重。
