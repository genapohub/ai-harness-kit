# 企业 AI 编程落地：整体选型（可分享版）

> 一份给「想在企业里把 AI 编程真正用起来」的负责人看的选型手册。
> 不讲玄学，只给判断框架、架构图、红线与落地节奏。配套治理壳见 `ai-harness-kit`。

---

## 0. 一句话结论

把 AI 编程搬进企业，核心不是“选哪个模型”，而是 **选自主度 + 选部署架构 + 守红线 + 控节奏** 四件事。

- **自主度**：默认停在「对话（L2）+ 协作（L3）」，别一上来就上「代理（L4）全自主」。
- **架构**：本地主力干重活 + 线上补充做评审/CI/演示，全部收敛到**统一代码仓库**。
- **红线**：敏感代码不喂公网、AI 不直接推 main、跳过扫描不 merge。
- **节奏**：个人试点 1 周 → 团队规范 2 周 → CI 评审 1 月 → 全员 evals 持续。

---

## 1. 总框架：壳 / 引擎 / 代理

企业 AI 编程有三类角色，它们**叠加而非替代**：

- **壳（治理层，本项目 `ai-harness-kit`）**：不产出产品，只给团队套上 AGENTS.md + project-tracker + SECURITY 红线 + evals 门禁。任何项目都能挂。
- **引擎（生产层，如 `mvp-expert-team`）**：一句话需求直接出可上线产品（需求→设计→开发→测试→部署端到端）。
- **代理（自主层，如 Devin / Factory）**：自主跑完整任务。能力强但风险高，企业里**慎用**。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 320" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#475569"/>
    </marker>
  </defs>
  <rect x="20" y="40" width="150" height="60" rx="10" fill="#e2e8f0" stroke="#94a3b8"/>
  <text x="95" y="66" text-anchor="middle" font-size="16" fill="#0f172a">一句话需求</text>
  <text x="95" y="86" text-anchor="middle" font-size="11" fill="#64748b">产品 / 任务描述</text>
  <path d="M170,70 L300,70" stroke="#475569" stroke-width="2" marker-end="url(#ar)"/>
  <rect x="310" y="45" width="120" height="50" rx="10" fill="#6366f1" stroke="#4338ca"/>
  <text x="370" y="70" text-anchor="middle" font-size="15" fill="#fff">路由判断</text>
  <text x="370" y="88" text-anchor="middle" font-size="10" fill="#a5b4fc">按目标选角色</text>
  <!-- 壳 -->
  <path d="M430,70 L470,30 L620,30 L620,80 L470,80 Z" fill="#f1f5f9" stroke="#0ea5e9"/>
  <text x="545" y="48" text-anchor="middle" font-size="14" fill="#0369a1">壳 · 治理层</text>
  <text x="545" y="66" text-anchor="middle" font-size="11" fill="#0c4a6e">ai-harness-kit</text>
  <!-- 引擎 -->
  <path d="M430,70 L470,110 L620,110 L620,160 L470,160 Z" fill="#ecfdf5" stroke="#10b981"/>
  <text x="545" y="128" text-anchor="middle" font-size="14" fill="#047857">引擎 · 生产层</text>
  <text x="545" y="146" text-anchor="middle" font-size="11" fill="#065f46">mvp-expert-team</text>
  <!-- 代理 -->
  <path d="M430,70 L470,190 L620,190 L620,240 L470,240 Z" fill="#fef2f2" stroke="#ef4444"/>
  <text x="545" y="208" text-anchor="middle" font-size="14" fill="#b91c1c">代理 · 自主层</text>
  <text x="545" y="226" text-anchor="middle" font-size="11" fill="#991b1b">Devin / Factory（慎用）</text>
  <path d="M370,70 L420,55" stroke="#0ea5e9" stroke-width="2" marker-end="url(#ar)"/>
  <path d="M370,70 L420,135" stroke="#10b981" stroke-width="2" marker-end="url(#ar)"/>
  <path d="M370,70 L420,215" stroke="#ef4444" stroke-width="2" marker-end="url(#ar)"/>
  <text x="95" y="300" text-anchor="middle" font-size="12" fill="#475569">三者叠加非替代：壳管规矩，引擎出产品，代理干重活但要守边界。</text>
</svg>
```

---

## 2. 维度一：自主度四级（决定“AI 能自己干到哪一步”）

| 级别 | 名称 | 典型工具 | 人介入程度 | 企业建议 |
|------|------|----------|------------|----------|
| L1 | 补全 | Copilot、通义灵码、Continue | 每行都看 | 基础标配 |
| L2 | 对话 | Cursor、CodeBuddy、Claude | 改片段/文件 | **主力档** |
| L3 | 协作 | Claude Code、Aider | 审 PR/跑任务 | **主力档** |
| L4 | 代理 | Devin、Factory、Codegen | 几乎不管 | 暂不上 |

**判断原则**：自主度每升一级，失控风险指数上升。企业项目默认停在 **L2 + L3**，把 L4 留给内部非核心、可回滚的实验性任务。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 300" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <marker id="up" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 阶梯 4 级 -->
  <rect x="40"  y="210" width="140" height="50" rx="8" fill="#cbd5e1" stroke="#94a3b8"/>
  <rect x="190" y="160" width="140" height="100" rx="8" fill="#93c5fd" stroke="#3b82f6"/>
  <rect x="340" y="110" width="140" height="150" rx="8" fill="#60a5fa" stroke="#2563eb"/>
  <rect x="490" y="60"  width="140" height="200" rx="8" fill="#fca5a5" stroke="#ef4444"/>
  <text x="110" y="240" text-anchor="middle" font-size="14" fill="#0f172a">L1 补全</text>
  <text x="110" y="258" text-anchor="middle" font-size="11" fill="#334155">Copilot</text>
  <text x="260" y="210" text-anchor="middle" font-size="14" fill="#fff">L2 对话</text>
  <text x="260" y="228" text-anchor="middle" font-size="11" fill="#eff6ff">Cursor</text>
  <text x="410" y="190" text-anchor="middle" font-size="14" fill="#fff">L3 协作</text>
  <text x="410" y="208" text-anchor="middle" font-size="11" fill="#eff6ff">Claude Code</text>
  <text x="560" y="170" text-anchor="middle" font-size="14" fill="#fff">L4 代理</text>
  <text x="560" y="188" text-anchor="middle" font-size="11" fill="#fef2f2">Devin</text>
  <!-- 上升箭头 -->
  <path d="M540,60 L560,40 L580,60" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#up)"/>
  <text x="600" y="46" font-size="11" fill="#475569">风险↑</text>
  <!-- 企业默认停驻带 -->
  <rect x="190" y="285" width="290" height="14" rx="7" fill="#16a34a" opacity="0.18"/>
  <text x="335" y="296" text-anchor="middle" font-size="11" fill="#166534">企业默认停：L2 + L3</text>
</svg>
```

---

## 3. 维度二：三层混合架构（决定“代码在哪跑、哪看”）

把能力拆成「本地主力」和「线上补充」，最后全部收敛到一个**统一代码仓库**——这样既利用公网模型的强能力，又把敏感代码留在本地。

- **本地主力（teal）**：Claude Code / Aider 跑大任务；Continue / Cody 跑补全；Ollama + Qwen2.5-Coder 跑敏感代码（不上公网）。
- **线上补充（blue）**：Cursor Web 跑 PR 评审；GitHub Actions + Claude 跑 CI/CD 自动修 bug；StackBlitz 跑跨设备演示。
- **收敛点**：所有产出回到统一代码仓库，避免“本地一份、线上一份”的分裂。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 320" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <marker id="c" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 本地主力 -->
  <rect x="30" y="30" width="290" height="180" rx="12" fill="#f0fdfa" stroke="#14b8a6"/>
  <text x="175" y="55" text-anchor="middle" font-size="15" fill="#0f766e">本地主力（teal）</text>
  <rect x="50" y="70" width="250" height="34" rx="6" fill="#ccfbf1" stroke="#5eead4"/>
  <text x="175" y="92" text-anchor="middle" font-size="12" fill="#134e4a">Claude Code / Aider — 大任务</text>
  <rect x="50" y="112" width="250" height="34" rx="6" fill="#ccfbf1" stroke="#5eead4"/>
  <text x="175" y="134" text-anchor="middle" font-size="12" fill="#134e4a">Continue / Cody — 补全</text>
  <rect x="50" y="154" width="250" height="34" rx="6" fill="#ccfbf1" stroke="#5eead4"/>
  <text x="175" y="176" text-anchor="middle" font-size="12" fill="#134e4a">Ollama+Qwen2.5-Coder — 敏感代码</text>
  <!-- 线上补充 -->
  <rect x="360" y="30" width="290" height="180" rx="12" fill="#eff6ff" stroke="#3b82f6"/>
  <text x="505" y="55" text-anchor="middle" font-size="15" fill="#1d4ed8">线上补充（blue）</text>
  <rect x="380" y="70" width="250" height="34" rx="6" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="505" y="92" text-anchor="middle" font-size="12" fill="#1e3a8a">Cursor Web — PR 评审</text>
  <rect x="380" y="112" width="250" height="34" rx="6" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="505" y="134" text-anchor="middle" font-size="12" fill="#1e3a8a">GH Actions+Claude — CI/CD 修 bug</text>
  <rect x="380" y="154" width="250" height="34" rx="6" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="505" y="176" text-anchor="middle" font-size="12" fill="#1e3a8a">StackBlitz — 跨设备演示</text>
  <!-- 收敛 -->
  <path d="M175,210 L340,255" stroke="#475569" stroke-width="2" marker-end="url(#c)"/>
  <path d="M505,210 L340,255" stroke="#475569" stroke-width="2" marker-end="url(#c)"/>
  <rect x="220" y="255" width="240" height="44" rx="10" fill="#0f172a"/>
  <text x="340" y="282" text-anchor="middle" font-size="14" fill="#fff">统一代码仓库（唯一真相源）</text>
</svg>
```

---

## 4. 维度三：三条红线（决定“什么绝对不能越”）

无论自主度多高，这三条不可破：

1. **敏感不喂公网**：客户代码、财务/合同代码不进任何公网模型。敏感部分用本地模型（Ollama + Qwen2.5-Coder）或脱敏后处理。
2. **AI 不直接推 main**：AI 产出只走 PR/分支，由人 review 后合入。主分支的保护规则不能因“AI 写的”而放开。
3. **跳过扫描不 merge**：必须过代码扫描（lint / SAST / 密钥检测）才能 merge，AI 提交也不例外。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 200" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <rect x="30" y="30" width="620" height="44" rx="10" fill="#fef2f2" stroke="#ef4444"/>
  <text x="50" y="58" font-size="15" fill="#b91c1c">① 敏感代码不喂公网模型（本地/脱敏处理）</text>
  <rect x="30" y="84" width="620" height="44" rx="10" fill="#fef2f2" stroke="#ef4444"/>
  <text x="50" y="112" font-size="15" fill="#b91c1c">② AI 不直接 push main（只走 PR，人 review 后合入）</text>
  <rect x="30" y="138" width="620" height="44" rx="10" fill="#fef2f2" stroke="#ef4444"/>
  <text x="50" y="166" font-size="15" fill="#b91c1c">③ 跳过代码扫描不 merge（lint/SAST/密钥检测必过）</text>
</svg>
```

---

## 5. 维度四：落地四阶段（决定“按什么节奏铺开”）

不要全员一把梭。按成熟度逐级推进：

1. **个人试点（1 周）**：1–2 个志愿者用 L2/L3 跑真实任务，攒手感与反例。
2. **团队规范（2 周）**：写 `AGENTS.md` + `CLAUDE.md`，明确“AI 能/不能做什么、怎么 review”。
3. **流程嵌入（1 月）**：CI 里挂 PR 评审 + evals 门禁（观察期 `continue-on-error`，稳定后转硬）。
4. **全员覆盖（持续）**：evals 套件覆盖主要模块，纳入常规质量基线。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 160" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <marker id="r" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#475569"/>
    </marker>
  </defs>
  <rect x="20"  y="40" width="140" height="70" rx="10" fill="#f1f5f9" stroke="#64748b"/>
  <text x="90"  y="70" text-anchor="middle" font-size="14" fill="#0f172a">① 个人试点</text>
  <text x="90"  y="92" text-anchor="middle" font-size="12" fill="#475569">1 周</text>
  <rect x="180" y="40" width="140" height="70" rx="10" fill="#e0f2fe" stroke="#0ea5e9"/>
  <text x="250" y="70" text-anchor="middle" font-size="14" fill="#0369a1">② 团队规范</text>
  <text x="250" y="92" text-anchor="middle" font-size="12" fill="#0369a1">2 周</text>
  <rect x="340" y="40" width="140" height="70" rx="10" fill="#dcfce7" stroke="#22c55e"/>
  <text x="410" y="70" text-anchor="middle" font-size="14" fill="#15803d">③ 流程嵌入</text>
  <text x="410" y="92" text-anchor="middle" font-size="12" fill="#15803d">1 月</text>
  <rect x="500" y="40" width="140" height="70" rx="10" fill="#fef9c3" stroke="#eab308"/>
  <text x="570" y="70" text-anchor="middle" font-size="14" fill="#a16207">④ 全员覆盖</text>
  <text x="570" y="92" text-anchor="middle" font-size="12" fill="#a16207">持续</text>
  <path d="M160,75 L180,75" stroke="#475569" stroke-width="2" marker-end="url(#r)"/>
  <path d="M320,75 L340,75" stroke="#475569" stroke-width="2" marker-end="url(#r)"/>
  <path d="M480,75 L500,75" stroke="#475569" stroke-width="2" marker-end="url(#r)"/>
</svg>
```

---

## 6. 明确“不做”清单（防过度投入）

- **OPC / 中小团队阶段**：不碰 Devin / Factory / Codegen 这类全自主 Agent。
- 不自建 LangSmith / Helicone 等商业级 Harness 平台（团队 < 5 人用不上）。
- 不强制全员用 AI——先自愿试点，用结果说话。

---

## 7. 推荐起步动作（30 分钟可完成）

1. 在项目根目录放一份 `AGENTS.md`，写清：AI 能做什么、不能做什么、怎么 review。
2. 挂 `ai-harness-kit` 治理壳：`./scripts/init-harness.py --lite --name <项目名>`（只铺治理三件套 + evals，不克隆 14 仓、不强制填变量）。
3. 加 `.github/pull_request_template.md`（含 Harness 自检 4 项）。
4. 跑一次 evals，确认观察期门禁能跑通。

---

## 8. 与 `ai-harness-kit` 的关系

本选型文档是 `ai-harness-kit` 的“为什么这么设计”的顶层说明。壳负责把上面的红线、门禁、规范落到每个项目；引擎（如 `mvp-expert-team`）负责把需求变成产品；代理作为可选项按需启用。三者通过**统一代码仓库**和**同一套规范**串起来。

---

*© 张孟博（PM哥拿坡）· 2026-09-14 · 配套治理壳 `ai-harness-kit`*
