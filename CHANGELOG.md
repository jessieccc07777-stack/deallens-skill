# Changelog

本文件记录 DealLens 的版本变更。

## [1.0.0] - 2026-08-10

首个公开发布（开源）版本，对应参赛提交的 `DealLens_20260810` 包。

### 内容
- **DealLens.html**：单文件可视化应用（条款关系图谱 + 动态 Cap Table 模拟器 + 修改前/后对比）
- **deallens-extract skill**：`SKILL.md` + `references/schema.md` + `references/extraction-guide.md` + `scripts/extract_text.py` + `scripts/validate_json.py`
- **sample_seriesA.json**：虚构演示数据（AI 制药公司融资故事线）

### 特性
- 完全本地浏览器运行，无账号、无数据留存、无第三方传输
- 默认仅匿名化权利主体名称，金额与股权比例保留
- 与 DealReview 联动：审核结果写回 `review` / `postReview` 字段，支持"修改前/修改后"对比

### 许可
- 整体 MIT License

---

*内部迭代版本（2025–2026）未在此列明，首个公开版本以 1.0.0 起算。*
