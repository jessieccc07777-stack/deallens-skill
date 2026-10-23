# DealLens JSON Schema

DealLens 单文件应用「导入协议 JSON」入口接受的描述文件格式。顶层字段：

## 顶层字段

| 字段 | 类型 | 必需 | 说明 |
|---|---|---|---|
| `_meta` | object | 建议 | 来源、脱敏口径、交易事实、假设。不参与渲染，供追溯 |
| `company` | {en, zh} | ✓ | 脱敏后的公司名称 |
| `roundName` | {en, zh} | ✓ | 轮次名，如 "Pre-A Round" / "天使轮 · 阶梯交割" |
| `round` | {preMoney, newMoney} | ✓ | 数字，单位 = 人民币百万元（RMB M）。多次交割时用末批定价口径 |
| `normalized` | bool | 默认 false | true 时金额按"归一化单位"显示（对外展示脱敏用） |
| `cashOnHand` | number | 建议 | 现金对比基数（RMB M），用于回购情景的现金缺口条形图 |
| `scenarios` | {ratchet, redemption, antiDilution} | 建议 | 控制模拟器三个情景开关的显隐；协议没有的条款设 false |
| `redemption` | {rate, closingYear, deadline} | 建议 | rate 为小数（0.08）；rate 留白时按 0.08 假设并在 _meta 注明 |
| `holders` | array | ✓ | 股东列表，见下 |
| `clauses` | array | 建议 | 条款图谱节点；缺省时图谱保持内置演示数据 |
| `edges` | array | 建议 | 条款关系边 |
| `parties` | array | v1.0 建议 | 影响矩阵的主体列：`[{id, en, zh}]`，如 founders / company / newinv / angels |
| `effects` | object | v1.0 建议 | 影响矩阵数据：`{条款id: {主体id: {t, en, zh}}}`，`t` ∈ `R`（权利/受益）/ `O`（义务/受限）/ `RO`（兼具）；en/zh 为一句话效果说明。只填受影响的条款×主体组合 |
| `presets` | array | v1.0 可选 | 情景沙盘预设：`{id, icon, title{en,zh}, desc{en,zh}, chain:[{en,zh}], chkRatchet?, chkRedeem?, chkAnti?}`；chkXxx 值为滑杆设定值（完成率% / 年份 / 价格%）。chain 为 4–6 步后果链（触发→股权变动→治理→IPO/合规→谈判要点） |
| `reviewMeta` | object | 可选 | 审核覆盖层来源标注：`{tool, date, note{en,zh}}`，通常由 dealreview 写回 |
| `postReview` | object | 可选 | 修订结果对比层：`{tool, date, basis{en,zh}, clauses{条款id: {level?, status, change{en,zh}}}}`，由 dealreview 在 redline 落实后写回；`status` ∈ `redlined`（已修订，须带修订后 `level`）/ `pending`（待谈判，省略 `level`）。存在时 DealLens 显示「审查对比」页与"修改前/修改后"切换 |

## holders[]

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 唯一标识。`founders` 会被对赌/反稀释情景默认为补偿义务人；`lead`/`follow` 或 `isNew:true` 识别为新投资人 |
| `en` / `zh` | string | 脱敏后的双语名称 |
| `post` | number | 交割后持股比例（%），显式指定。**与 pre/money 二选一**；阶梯交割必须用它 |
| `pre` | number | 投前持股比例（%），标准单次交割的老股东用 |
| `money` | number | 新投资人出资额（RMB M），标准单次交割用 |
| `isNew` | bool | 标记本轮新进入者 |
| `color` | string | 十六进制色值，缺省自动分配。建议沿用暖橙色系：#6B4A2F #D9CFC4 #F2B33D #C9A15A #E8713A #B8551F #8A857E |

校验规则：全部 holder 的最终比例合计必须 = 100（±0.05）。

## clauses[]

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 唯一标识 |
| `x`, `y` | number | 布局坐标，x ∈ {40,310,580,840}，y ∈ {50,210,390} |
| `tag` | {en, zh} | 分类标签，如 Foundation/Economic Trigger/Consequence/Governance/Exit |
| `en` / `zh` | string | 条款名（双语） |
| `plain` | {en, zh} | 通俗解读：这段条款在说什么、触发什么、谁受益谁受限。2–3 句，要有专业判断（留白、罕见结构、谈判要点） |
| `rh` | {en:[…], zh:[…]} | 权利人（rights-holder）数组 |
| `ob` | {en:[…], zh:[…]} | 义务人（obligor）数组 |
| `related` | string[] | 关联条款 id，须与 edges 一致 |
| `anchor` | bool | 仅 captable 锚点节点使用 |
| `review` | object | 可选。**提取时不填**——这是 dealreview 审核后写回的风险覆盖层。存在时 DealLens 按级别给节点着色并在详情面板显示审核意见。结构：`{level, issue{en,zh}, floor{en,zh}, trade{en,zh}, card?}`；`level` ∈ `red`（🔴红线）/ `major`（🟠重大）/ `minor`（🟡可协商）/ `ok`（🟢市场惯例·放行）；`issue`=问题摘要，`floor`=可接受底线，`trade`=建议交换条件，`card`=来源条款卡编号 |

## review 覆盖层（dealreview 写回）

提取技能只产出中性描述 JSON；风险分级由 `dealreview` 技能审核后写回各条款的 `review` 字段，并可在顶层加 `reviewMeta`；redline 落实后 dealreview 还会写回顶层 `postReview`（修改前/修改后对比层）。若用户给你的 JSON 已含 `review`/`reviewMeta`/`postReview`，重新提取或更新时**必须原样保留**，不要删除。

## edges[]

`{f, t, en, zh}`：f/t 为条款 id；en/zh 为关系标签（如 "shortfall triggers" / "不达标触发"）。只画协议中真实存在的关系。

## 最小示例

```json
{
  "company": {"en": "TargetCo Ltd.", "zh": "标的公司"},
  "roundName": {"en": "Pre-A", "zh": "Pre-A 轮"},
  "round": {"preMoney": 28.5, "newMoney": 2.5},
  "cashOnHand": 2.5,
  "scenarios": {"ratchet": false, "redemption": true, "antiDilution": false},
  "redemption": {"rate": 0.08, "closingYear": 2025, "deadline": "触发情形发生"},
  "holders": [
    {"id": "founders", "en": "Founder A", "zh": "创始人A", "post": 84.42},
    {"id": "lead", "en": "Investor 1", "zh": "投资人1", "post": 5.00, "isNew": true, "money": 1.5}
  ],
  "clauses": [ ... ], "edges": [ ... ]
}
```
