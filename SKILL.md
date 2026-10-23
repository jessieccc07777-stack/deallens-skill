---
name: deallens-extract
description: >-
  Extract structured clause data from PRC investment agreements (SPA / SHA / TS, in
  .docx or .pdf) into a JSON descriptor importable by the DealLens visualization app,
  with party-name anonymization. Use when the user wants to import an agreement into
  DealLens, visualize agreement clauses, generate a cap-table / trigger-scenario model,
  or mentions DealLens / 协议可视化 / 增资协议 / 股东协议 / SPA / SHA / 对赌 / 回购条款 /
  提取协议 JSON. Produces a neutral descriptive JSON (no risk grading); risk review is
  handled by the companion DealReview skill. Content in Simplified Chinese (PRC venture
  transactions).
license: MIT
compatibility: "Claude Code, Codex CLI, Cursor, WorkBuddy and other SKILL.md-compatible agents"
metadata:
  author: "Jessie"
  version: "1.0.0"
  tags: "legal, contract-extraction, venture-capital, China, PRC, visualization, cap-table, SPA, SHA"
  language: "Simplified Chinese"
agent_created: true
---

# DealLens 协议提取

把投资协议（Word/PDF）转换为 DealLens 单文件应用可导入的 JSON 描述文件。

## 工作流

1. **收取文件**：将协议复制进当前工作区再处理，不直接改动原文件。
2. **提取文本**：运行 `scripts/extract_text.py <协议文件>`，生成同名 `.txt`（含表格内容，股权结构表通常在表格里）。
3. **通读全文**：按 `references/extraction-guide.md` 的清单定位关键条款与数据。协议可能很长，优先精读：交易安排/增资条款、股权结构表、投资人特别权利（回购/对赌/反稀释/清算优先/优先购买/领售随售/知情权）、公司治理、违约责任。
4. **脱敏（默认政策：仅匿名化权利主体名称）**：
   - 公司 → `标的公司 / TargetCo Ltd.`；自然人 → `创始人A / 现有股东B`；机构/合伙 → `合伙人 / 投资人1 / 投资人2 / 领投方` 等角色化名称
   - 注册号、地址、身份证号、银行账号一律不进入 JSON
   - **保留真实金额与股权比例**——DealLens 的内部工作用途（管理层演示、谈判推演）依赖真实数字，这是用户明确的政策
   - 例外：用户明确要求对外展示级别脱敏时，才对金额做归一化（最终投前=100 单位）或改用虚构数据；在 `_meta.desensitization` 中如实记录所用口径
5. **构建 JSON**：严格按 `references/schema.md` 的字段规范。条款节点含中英双语解读；解读要写出"谁是权利人、谁是义务人、触发后发生什么"，并指出专业要点（谈判留白、罕见保护结构等）。
6. **校验**：运行 `scripts/validate_json.py <生成的json>`，必须全部通过（比例合计=100%、边与关联引用完整、必需字段齐全）。
7. **交付**：报告 JSON 路径，并附**提取发现摘要**——这笔交易的独特结构、留白/缺失条款、值得用户注意的风险点。提醒用户在 DealLens 中「导入协议 JSON」验收。

## 关键规则

- **阶梯/多次交割**：holders 使用显式 `post`（协议载明的最终持股比例）；`round` 用末批定价口径（投前/该批增资额）；各批估值与对价写入 `_meta.dealFacts`。
- **单次标准交割**：老股东用 `pre`（投前比例）、新投资人用 `money`（出资额，单位：人民币百万元），由应用自动计算稀释。
- **协议中没有的条款**：在 `scenarios` 中显式关闭（`ratchet:false` / `antiDilution:false`），不要虚构； redemption 几乎所有 SHA 都有，默认 `true`。
- **留白条款**（如利率 `【 】%`）：在 `_meta.notes` 标注，在该 clause 的 `plain` 中以"活谈判点"提示，`redemption.rate` 按 0.08 假设并注明。
- **条款图谱布局**：4 列 × 3 行网格，x ∈ {40, 310, 580, 840}，y ∈ {50, 210, 390}；`captable` 锚点节点 `"anchor": true`，置于右侧列；edges 只画协议中真实存在的触发/引用关系，每条配中英双语标签。
- **输出文件名**：`<标的公司或项目代号>_DealLens.json`，保存到工作区。
- **与 dealreview 的联动**：本技能只产出中性描述 JSON，不做风险分级。若输入 JSON 或同目录已有文件含 `review` / `reviewMeta` 字段（dealreview 审核写回的风险覆盖层），重新提取或更新时原样保留。用户需要"审核 + 可视化"联动时，提示其先运行本技能生成 JSON，再用 dealreview 审核写回。
