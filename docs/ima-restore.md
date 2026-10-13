# 备用安装路径：从 ima 知识库还原本技能

> 适用场景：不想用 `git clone`，或需要在一台**没有 GitHub 访问**的设备上装本技能。
> 前提：该设备登录**同一个 ima 账号**，并已连接 ima 连接器。

## 一、技能由两部分组成

| 部件 | 存放位置 | 是否随设备走 |
| --- | --- | --- |
| 技能文件（4 个 .md） | ima「成果」知识库 | 云端，跟账号走 |
| 运行时典籍（15 个文件） | ima「资料 / 易经 / 知识库」 | 云端，跟账号走 |

因此换设备**不需要重新整理任何内容**，只要：① 还原技能文件到本地技能目录；② 新设备登录同一 ima 账号并连接 ima 连接器。

## 二、还原映射

本地技能目录（**用户级**，所有项目通用）：

- Windows：`C:\Users\<你的用户名>\.workbuddy\skills\yijing-divination\`
- macOS / Linux：`~/.workbuddy/skills/yijing-divination/`

| 本地目标文件 | 来源（ima「成果」中的标题） |
| --- | --- |
| `SKILL.md` | yijing-divination-SKILL.md |
| `references/gua-index.md` | yijing-divination-gua-index.md |
| `references/jiugua-rules.md` | yijing-divination-jiugua-rules.md |
| `references/knowledge-map.md` | yijing-divination-knowledge-map.md |
| `scripts/divine_gua.py` | （ima 上传不支持 .py；可选，见下） |

## 三、最简还原方式：一句话交给 Agent

在新设备的 Agent（如 WorkBuddy）里直接发这句话：

> 请从 ima「成果」知识库读取 yijing-divination-SKILL.md、yijing-divination-gua-index.md、yijing-divination-jiugua-rules.md、yijing-divination-knowledge-map.md 四个文件，按下列映射写入本地技能目录：
> - SKILL.md → `~/.workbuddy/skills/yijing-divination/SKILL.md`
> - 其余三个 → `~/.workbuddy/skills/yijing-divination/references/` 下，文件名去掉 `yijing-divination-` 前缀。
> 完成后列出目录结构确认。

（Windows 下 `~` 即 `C:\Users\<你的用户名>`。）

## 四、注意事项

1. 新设备需登录**同一个 ima 账号**，否则读不到「资料 / 易经 / 知识库」的原文。
2. `scripts/divine_gua.py` 无法经 ima 归档（其 MIME 对照表不含 `.py`）。缺它**不影响使用**——SKILL.md 已写明「脚本不可用时，按 `references/gua-index.md` 第三节的算法手算」。如需脚本，从 GitHub 仓库取，或从已有设备拷贝。
3. 连接器若显示已授权但工具不可调用，在连接器菜单里**重连一次**即可恢复。
