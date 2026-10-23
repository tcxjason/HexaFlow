# 备用安装路径：从 ima 知识库还原本技能

> 适用场景：不想用 `git clone`，或需要在一台**没有 GitHub 访问**的设备上装本技能。
> 该路径**不需要网络、不需要 ima 连接器**——安装包是纯文本，自带全部文件内容。

## 一、首选：自还原安装包

在 ima 个人知识库「成果 / **易经占卦-skill**」中取这一份：

| 文件 | 说明 |
| --- | --- |
| `hexaflow-安装包（自还原）.md` | 包含**全部 17 个文件**的完整内容，用 `<!-- ===BEGIN FILE: <路径>=== -->` 标记分节 |
| `hexaflow-使用说明.md` | 安装 / 使用 / 维护 全说明 |

把它交给新设备的 Agent（如 WorkBuddy），说：

> 这是一份技能安装包。请按文档中的「===BEGIN FILE: <路径>===」标记切分文件，逐一写入
> `~/.workbuddy/skills/hexaflow/`（Windows 为 `%USERPROFILE%\.workbuddy\skills\hexaflow\`），
> 保持标记中的相对路径结构。完成后列出目录结构确认，应共 17 个文件。

还原后目录结构：

```
hexaflow/
├── SKILL.md
├── data/            （README + 01~08，共 9 个文件）
├── references/      （gua-index / jiugua-rules / knowledge-map）
├── scripts/         （divine_gua.py）
├── docs/            （本文件）
├── README.md
└── LICENSE
```

## 二、为什么不再逐个文件归档

早期（2026-10-13）曾把技能拆成 4 个单文件（`hexaflow-SKILL.md`、`-gua-index.md`、`-jiugua-rules.md`、`-knowledge-map.md`）归档，靠"逐份读取再写盘"还原。该方式已废弃：

- 它把技能拆成 4 份，**漏文件、错目录的风险高**；
- 它无法承载 `data/`（八部经文，92 KB）与 `scripts/`，**早已落后于自包含改造**；
- 单文件方式还需要**逐份核对**，而自还原包**一次到位**。

所以：**请以下载自还原安装包（或 GitHub 仓库）为唯一还原途径。** 若在「易经占卦-skill」中看到那批带 `hexaflow-` 前缀的**单文件旧归档**，它们已停止维护，请勿使用。

## 三、可选组件

| 组件 | 是否必需 | 说明 |
| --- | --- | --- |
| `scripts/divine_gua.py` | ⬜ 可选 | 已包含在安装包内。若不还原它，按 `references/gua-index.md` 第三节的算法手算即可 |
| ima 连接器 | ⬜ 可选 | 本技能已完全自包含，**安装与运行均不需要**；仅在需要交叉核对上游知识库时使用 |

## 四、补充

- 若能访问 GitHub，`git clone https://github.com/tcxjason/HexaFlow.git ~/.workbuddy/skills/hexaflow` 更省事（该仓库为 Private，需凭据）。
- 安装后**重开一次会话**（技能列表有扫描缓存），说「解卦：本卦泰，三爻变」验证。
- 本地已装好技能时，改动 `SKILL.md` 或 `data/` 后**务必同步**到 `~/.workbuddy/skills/hexaflow/`（用 `diff -r` 校验）。
