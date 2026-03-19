# 数据模型：Graph-First 研究时间线工作台

**日期**：2026-03-18  
**状态**：Draft v0.1  
**相关文档**：

- [MVP 定义](./02-mvp-definition.md)
- [技术选型](./03-tech-selection.md)
- [问题域草稿](../../article.md)

---

## 1. 目标

这份文档定义第一版的底层数据模型。

目标不是做一个“大而全 ontology”，而是定住最小但可扩展的 graph schema，让第一版就具备：

- 时间线投影能力
- 证据回溯能力
- 节点邻域追问能力
- 后续扩展到多 Markdown、多视图的能力

---

## 2. 建模原则

### 2.1 事件优先

时间线是第一视图，所以 `Event` 是第一公民。

### 2.2 证据优先

任何重要结论都必须能回到 `Segment` 和原始 `Source`。

### 2.3 图优先

时间线只是 `Event Graph` 的一种投影，不是底层真相本身。

### 2.4 模糊时间可保留

第一版不强求把所有时间都归一成精确日期。  
允许保留 `time_text` 和 `time_precision=fuzzy`。

### 2.5 AI 与人工并存

AI 产出的对象不是最终真理，需要有状态和可修正性。

---

## 3. 第一版节点类型

第一版只定义 5 类核心节点。

### 3.1 Source

表示一个输入来源，目前一期只支持 Markdown。

关键字段：

- `id`
- `title`
- `source_type`：`markdown`
- `raw_content`
- `created_at`
- `checksum`

说明：

- `raw_content` 保留原文，便于重跑抽取
- `checksum` 便于判断内容是否变化

### 3.2 Segment

表示从 Source 中切分出来的语义片段。  
第一版建议用“段落级切分”。

关键字段：

- `id`
- `source_id`
- `index`
- `text`
- `start_offset`
- `end_offset`
- `heading_path`

说明：

- `Segment` 是证据回溯的最小工作单元
- `heading_path` 用于后续在 UI 中定位上下文

### 3.3 Event

表示时间线上的事件节点，是第一版最重要的对象。

关键字段：

- `id`
- `title`
- `summary`
- `time_text`
- `time_start`
- `time_end`
- `time_precision`
- `time_sort_key`
- `importance`
- `status`
- `created_by`

字段建议：

- `time_precision`：`day | month | year | decade | range | fuzzy | unknown`
- `importance`：`1-5`
- `status`：`draft | confirmed | revised | merged`
- `created_by`：`ai | user`

说明：

- `time_text` 保留原始时间表达，如“20 世纪 40 年代初”
- `time_sort_key` 用于时间线排序，即使时间是模糊的也给一个近似排序点

### 3.4 Entity

表示人物、机构、概念、论文、系统、会议等对象。

关键字段：

- `id`
- `name`
- `entity_type`
- `aliases`
- `description`

字段建议：

- `entity_type`：`person | org | concept | paper | system | meeting | place | other`

说明：

- 第一期不需要把实体类型做得特别细
- 关键是先让 Event 与 Entity 之间的关系可查询

### 3.5 Evidence

表示某个事件或关系的证据。

关键字段：

- `id`
- `quote`
- `confidence`
- `note`
- `created_at`

说明：

- `quote` 一般来自 Segment 的片段
- `note` 可用于保存 AI 为什么把这段话归到某个事件

---

## 4. 第一版关系类型

### 4.1 来源与片段

- `(Source)-[:HAS_SEGMENT]->(Segment)`

作用：

- 从原文追到段落

### 4.2 片段到事件

- `(Segment)-[:DESCRIBES]->(Event)`

作用：

- 表示某段原文描述了某个事件

### 4.3 片段到实体

- `(Segment)-[:MENTIONS]->(Entity)`

作用：

- 表示实体在该段中出现

### 4.4 事件到实体

- `(Event)-[:INVOLVES {role, confidence}]->(Entity)`

作用：

- 表示事件涉及的人物、机构、概念等

示例：

- 图灵 1936 年论文 `INVOLVES` 图灵
- 达特茅斯会议 `INVOLVES` 麦卡锡

### 4.5 事件到证据

- `(Event)-[:SUPPORTED_BY]->(Evidence)`
- `(Evidence)-[:FROM_SEGMENT]->(Segment)`

作用：

- 让每个事件都能回溯到原文证据

### 4.6 事件之间的时间关系

- `(Event)-[:PRECEDES]->(Event)`

作用：

- 表达时间顺序关系

说明：

- 即使 `time_start` 可排序，也建议保留显式顺序边
- 这有利于后续做节点邻域追问和因果链探索

### 4.7 事件的主线/支线关系

- `(Event)-[:PARENT_OF]->(Event)`

作用：

- 表达主事件和挂载事件的层级关系

说明：

- 这是实现“主线展开、支线折叠”的关键

### 4.8 事件的关联关系

- `(Event)-[:RELATED_TO {type, confidence}]->(Event)`

作用：

- 表达非纯时间顺序的关联，如“影响”“延续”“对比”“回应”

### 4.9 实体之间的关联关系

- `(Entity)-[:RELATED_TO {type, confidence}]->(Entity)`

作用：

- 为第二阶段的人物关系图、概念关系图打基础

---

## 5. 时间字段设计

第一版时间设计不求完美，但必须可排序、可解释、可修正。

### 5.1 必须保留的字段

- `time_text`
- `time_start`
- `time_end`
- `time_precision`
- `time_sort_key`

### 5.2 字段含义

- `time_text`
  - 原始文本表达
  - 例：`20 世纪 40 年代初`

- `time_start`
  - 归一化起始时间
  - 例：`1940-01-01`

- `time_end`
  - 归一化结束时间
  - 例：`1943-12-31`

- `time_precision`
  - 时间精度
  - 例：`year`、`decade`、`fuzzy`

- `time_sort_key`
  - 用于前端排序
  - 可以取 `time_start`，也可以是近似时间点

### 5.3 第一版处理规则

- 明确日期：直接归一
- 明确年份：按年份归一
- 年代区间：记录 `start/end`
- 模糊时间：保留 `time_text`，给近似 `time_sort_key`
- 无法判断：`time_precision=unknown`

---

## 6. 主线与支线模型

主线与支线不是两套表，而是同一套 Event 节点上的不同关系和属性。

### 6.1 主线判断

第一版可以先用：

- `importance`
- 是否具备明确时间
- 是否处于核心历史推进链

综合得到主线候选。

### 6.2 支线表达

支线通过两种方式表达：

- `PARENT_OF`
- 较低的 `importance`

说明：

- `PARENT_OF` 决定结构挂载
- `importance` 决定默认展开或折叠策略

---

## 7. 去重与合并策略

第一版必须允许 AI 抽出重复事件，但不能强制第一次就彻底去重正确。

### 7.1 第一版原则

- 先允许重复候选存在
- 再通过人工确认或规则合并

### 7.2 Event 合并建议

可以通过以下条件判断候选是否可能是同一事件：

- 标题相近
- 时间接近
- 关联实体高度重合
- 证据片段指向相同语义

### 7.3 合并后的处理

合并后建议：

- 保留一个 canonical Event
- 被合并节点 `status=merged`
- 证据关系保留，不直接丢弃

---

## 8. 节点追问上下文模型

第一版不做全局知识问答，而是围绕当前节点取图邻域。

### 8.1 默认取值范围

围绕一个 Event 节点，默认取：

- 当前 Event
- 父 Event
- 子 Event
- 前后相邻 Event
- 直接关联 Entity
- 直接关联 Evidence
- Evidence 对应的 Segment

### 8.2 为什么这么取

这样能让模型回答：

- 这个事件为什么重要
- 它和前后事件怎么接起来
- 它涉及哪些人物或概念
- 证据出自哪里

---

## 9. Cypher 视角下的最小模型示例

下面只是概念示例，不是最终实现代码：

```cypher
(s:Source)-[:HAS_SEGMENT]->(seg:Segment)-[:DESCRIBES]->(e:Event)
(seg)-[:MENTIONS]->(ent:Entity)
(e)-[:INVOLVES]->(ent)
(e)-[:SUPPORTED_BY]->(ev:Evidence)-[:FROM_SEGMENT]->(seg)
(e1)-[:PRECEDES]->(e2)
(parent:Event)-[:PARENT_OF]->(child:Event)
```

这个模型已经足够支撑：

- 时间线排序
- 节点详情
- 证据回溯
- 主线/支线折叠
- 围绕事件做邻域追问

---

## 10. 第一期明确不建模的内容

为了避免 schema 失控，第一期不单独建模：

- 用户权限
- 评论线程
- 任务流状态机
- 向量索引对象
- 复杂 Topic 层级
- 地图坐标与空间关系
- 完整 Claim / Counter-Claim 争议系统

这些都可以在第二阶段再扩展。

---

## 11. 当前待定点

虽然主 schema 已经可以定下来，但还有几个点后续需要决定：

1. 第一版是否引入 `Topic` 节点？
2. `PRECEDES` 是抽取生成，还是根据时间排序后自动补边？
3. `PARENT_OF` 完全由 AI 初判，还是必须人工确认？
4. `RELATED_TO` 的 `type` 是否先限制枚举？

这些问题不会阻塞第一版原型。

---

## 12. 结论

第一版建议把下面这套模型作为稳定基础：

- 节点：`Source / Segment / Event / Entity / Evidence`
- 关键边：`DESCRIBES / MENTIONS / INVOLVES / SUPPORTED_BY / PRECEDES / PARENT_OF`
- 时间：`time_text + time_start + time_end + time_precision + time_sort_key`
- 交互：从 Event 图投影时间线，从 Event 邻域构造追问上下文

一句话总结：

> 第一期虽然只输入 Markdown，但底层已经按“可生长的研究图谱”来建模，而不是按“时间线数组”来建模。
