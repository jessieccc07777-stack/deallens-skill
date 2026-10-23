# DealLens 安装与使用指南

## 组件一：DealLens 可视化应用（无需安装）

`DealLens.html` 是单文件应用，**双击用浏览器打开即可**，无需安装、无需联网、无需账号。

1. 双击 `DealLens.html`（推荐 Chrome / Edge）
2. 点击「导入协议 JSON」
3. 选择 `sample_seriesA.json`（演示）或你自己的协议 JSON

## 组件二：deallens-extract 提取技能

把协议 Word/PDF 提取成 DealLens 可导入的 JSON，需要一个支持 SKILL.md 的 AI 助手。

### 安装（以 Claude Code 为例）

```bash
mkdir -p ~/.claude/skills
cp -r deallens ~/.claude/skills/deallens-extract
```

> 注意：本仓库的 `SKILL.md` 定义的是提取技能 `deallens-extract`，安装时建议把文件夹名也命名为 `deallens-extract`。

| AI 助手 | skills 目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Codex CLI | `~/.codex/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` |

### 提取协议

1. 把协议文件发给 AI，说：**"请用 deallens-extract 提取这份协议"**
2. AI 运行 `scripts/extract_text.py` 提取文本 → 通读定位关键条款 → 脱敏 → 构建 JSON → `scripts/validate_json.py` 校验
3. 将 AI 输出的 JSON 保存为 `.json` 文件
4. 在 `DealLens.html` 中导入该文件

### 脚本依赖

- `scripts/extract_text.py`：提取 docx/pdf 文本（含表格），依赖 `python-docx`、`pdfplumber`
- `scripts/validate_json.py`：校验 JSON 字段与比例勾稽

```bash
pip install python-docx pdfplumber
```

两个脚本均**本地运行**，不联网、不访问外部服务。

## 常见问题

**Q：DealLens.html 打不开？**
A：换 Chrome / Edge 浏览器；确认文件未损坏（重新下载）。

**Q：导入 JSON 报错？**
A：确认 JSON 符合 `references/schema.md` 规范；用 `validate_json.py` 校验。

**Q：协议数据安全吗？**
A：DealLens 在本地浏览器运行，数据不上传服务器；提取技能默认脱敏主体名称，注册号/地址/身份证号/银行账号不进入 JSON。
