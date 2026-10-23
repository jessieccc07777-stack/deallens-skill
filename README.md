# DealLens

**Make an investment agreement move.** 一个"让投资协议动起来"的轻量网页工具 + 配套提取技能。

把投资协议变成**交互式可视化模型**：条款关系图谱 + 动态 Cap Table 模拟器。触发回购、业绩对赌等条款，立即看到股权结构如何变化、谁受益谁受限；并支持"修改前 / 修改后"对比（与 DealReview 审核结果联动）。

---

## 两个组件 / Two components

| 组件 | 文件 | 作用 |
|---|---|---|
| **DealLens 可视化应用** | `DealLens.html` | 单文件网页应用，双击浏览器打开即可，无需安装、无需联网 |
| **deallens-extract 提取技能** | `SKILL.md` + `references/` + `scripts/` | AI 助手技能，把协议 Word/PDF 提取成 DealLens 可导入的 JSON |

## 快速体验（30 秒）/ Quick start

1. 双击 `DealLens.html`（推荐 Chrome / Edge）
2. 点击「导入协议 JSON」，选择 `sample_seriesA.json`（虚构演示数据）
3. 点击各模块，触发回购/对赌情景，观察 Cap Table 与权利义务变化

> 在线演示（虚构数据，无需登录）：https://deallens-demo.surge.sh

## 分析你自己的协议 / Analyze your own agreement

1. 安装 `deallens-extract` 技能（见 [`docs/INSTALL.md`](docs/INSTALL.md)）
2. 把协议文件发给 AI，说：**"请用 deallens-extract 提取这份协议"**
3. 将 AI 输出的 JSON 保存为 `.json` 文件
4. 在 `DealLens.html` 中点击「导入协议 JSON」，选择该文件

## 与 DealReview 联动 / Works with DealReview

- `deallens-extract` 只产出**中性描述 JSON**，不做风险分级
- 风险分级由配套技能 [DealReview](https://github.com/jessieccc07777-stack/dealreview-skill) 审核后写回 JSON 的 `review` / `postReview` 字段
- 写回后，DealLens 显示「审查对比」页与"修改前/修改后"切换

## 隐私与脱敏 / Privacy & anonymization

- DealLens **完全在本地浏览器运行**，协议数据不上传任何服务器
- 提取技能默认**仅匿名化权利主体名称**（公司/自然人/机构角色化），注册号、地址、身份证号、银行账号不进入 JSON；金额与股权比例保留以保证可视化价值
- 对外演示建议使用脱敏模式或虚构数据

## 适用法域 / Jurisdiction

面向**中国大陆（PRC）创投交易**（SPA/SHA/TS），交付物中英双语。

## 目录结构 / Repository layout

```
deallens/
├── SKILL.md                  # deallens-extract skill 定义
├── DealLens.html             # 可视化主程序（单文件应用）
├── sample_seriesA.json       # 虚构演示数据
├── references/
│   ├── schema.md             # JSON schema 规范
│   └── extraction-guide.md   # 中式投资协议提取指南
├── scripts/
│   ├── extract_text.py       # 提取文本（含表格）
│   └── validate_json.py      # JSON 校验
└── docs/
    ├── INSTALL.md            # 安装 SOP
    └── QUICKSTART.zh-CN.md   # 快速体验
```

## 许可 / License

本仓库整体采用 **MIT License**（见 [`LICENSE`](LICENSE)）。DealLens 为工具 + 技术规范，与 [DealReview](https://github.com/jessieccc07777-stack/dealreview-skill)（其条款卡知识库另用 CC BY-NC-SA 4.0 保护）的许可策略不同。

## 免责声明 / Disclaimer

本工具用于**辅助理解协议结构**，**不构成法律意见**。重要决策请咨询专业律师。作者不对依赖本工具产生的后果承担责任。

## 作者 / Author

Jessie —— 前 PE/VC 从业者，十年投融资与资本市场法律实务经验。

反馈与联系：jessieccc0713@gmail.com

---

*First released 2026. Built with practitioner experience — responsible AI that widens access to legal expertise.*
