# 技术选型：AI 辅助历史研究时间线工作台

**日期**：2026-03-18  
**状态**：Draft v0.2  
**相关文档**：

- [MVP 定义](./02-mvp-definition.md)
- [现有技术调研](./01-investigate.md)
- [问题域草稿](../../article.md)

---

## 1. 目标

这份文档直接回答第一版怎么做：

- 用什么技术
- 哪些技术明确不用
- 为什么现在就做 graph-first

当前决策是：

> 一期只支持 `Markdown`，但底层架构按 `图谱化对象模型 + 图数据库优先` 来做。

也就是说，输入范围保守，底层建模激进。

---

## 2. 当前仓库约束

当前仓库很轻：

- 后端已有最小 [FastAPI](../../../fastapi/simple/main.py) 入口
- 已有 OpenAI 兼容方式调用模型的脚本 [zhipu.py](../../../llm/zhipu.py)
- 还没有前端、数据库、抽取流程、任务系统

因此第一版技术选型遵循两个原则：

1. 尽量沿用 `Python + FastAPI`
2. 把复杂度花在 `数据模型` 上，而不是一上来引入过多平台级中间件

---

## 3. 第一版拍板结果

### 3.1 后端

选择：

- `Python 3.11+`
- `FastAPI`

原因：

- 当前仓库已有最小 FastAPI 入口
- 适合做抽取 API、时间线 API、节点编辑 API、节点追问 API
- 和现有 OpenAI 兼容模型调用方式一致

结论：

第一版后端继续使用 `Python + FastAPI`。

### 3.2 LLM 接入

选择：

- 使用 `OpenAI-compatible API`
- 封装统一 `llm_client`
- 通过环境变量切换模型供应商

原因：

- 当前 [zhipu.py](../../../llm/zhipu.py) 已经说明项目可按 OpenAI 兼容模式接模型
- 这样后面可以在 `智谱 / OpenAI / 其他兼容供应商` 间切换
- 当前核心是结构化抽取与图谱写入，不是供应商绑定

结论：

第一版统一封装 provider，不把业务逻辑写死在某个模型 SDK 上。

### 3.3 前端

选择：

- `React + TypeScript`
- 主时间线组件优先使用 `vis-timeline`

原因：

- 第一版核心是强交互时间线
- 时间线节点需要点击、折叠、联动右侧详情和追问面板
- 纯模板页面不适合后续演化成研究工作台

结论：

第一版前后端分离：

- 后端：FastAPI
- 前端：React + TypeScript
- 时间线：`vis-timeline`

### 3.4 主存储

选择：

- 第一版主存储直接使用 `Neo4j`

原因：

- 你已经明确选择 `底层架构更激进`
- 系统的核心对象天然是图结构：`Source / Segment / Event / Entity / Evidence / Relation`
- 第一版虽然只导入 Markdown，但很快就会从“单篇文章”走向“同一主题下的多篇 Markdown”
- 如果第一版只是做成“时间线数组 + 表结构”，后面一旦要做跨文档合并、人物关系、概念演化、节点邻域追问，很容易重构

为什么现在就用 Neo4j：

- 时间线本质上只是 `Event` 图的一种投影视图
- 节点追问以后要用到相邻事件、关联实体、证据链，这些都更适合图遍历
- 主线 / 支线挂载、本体关系、来源追溯都更适合直接建边

为什么不是 SQLite-first：

- SQLite 更适合“先做一个时间线工具”
- 但你现在要的是“未来能长成研究图谱系统的时间线工作台”
- 当前决策重点已经不是最省工程量，而是减少未来重构

结论：

第一版主存储直接采用 `Neo4j graph-first`。

### 3.5 资料输入

选择：

- 第一版只支持 `Markdown`

原因：

- 当前已有 [article.md](../../article.md) 可直接作为样本
- PDF、网页、EPUB 会把问题提前复杂化成文档解析问题
- 你已经把“激进”押在底层架构，而不是输入通道

结论：

`Markdown first` 不变。

### 3.6 文本切分与抽取

选择：

- 先做 `段落级切分`
- 再做 `LLM 结构化抽取`
- 抽取结果直接映射到图谱对象

原因：

- 当前资料是研究型 Markdown，段落本身通常具备较清晰语义
- 第一版证据回溯最重要，段落级切分就足够支撑
- 过早引入复杂 chunking 策略收益不高

抽取输出建议包含：

- 事件候选
- 时间表达
- 人物 / 机构 / 概念
- 事件摘要
- 证据段落
- 关系候选
- 置信度

结论：

第一版先做 `Markdown -> Segment -> Event/Entity/Evidence/Relation`。

### 3.7 时间归一化

选择：

- `规则优先`
- `LLM 辅助`
- 自定义时间字段表达

原因：

- 历史文本里的时间表达经常是模糊的
- 例如“战后”“同年”“20 世纪 40 年代初”很难只靠单一 parser 解决
- 即便采用图数据库，时间本身仍然应该由你自己的字段模型控制

第一版时间字段建议：

- `time_text`
- `time_start`
- `time_end`
- `time_precision`
- `time_sort_key`

结论：

第一版时间归一化目标不是“全自动完全正确”，而是 `可排序 + 可保留模糊性 + 可人工修正`。

### 3.8 节点追问

选择：

- 不做全局开放式 RAG
- 做 `graph neighborhood chat`

即：

- 当前事件节点
- 父/子事件
- 相邻事件
- 关联实体
- 关联证据段落

一起作为上下文喂给模型。

原因：

- 你的追问场景是“围绕一条线索继续研究”，不是对整个知识库盲查
- 图邻域检索比向量检索更贴近第一版问题
- 这样能直接利用 graph-first 架构优势

结论：

节点追问第一版采用 `graph neighborhood context`，不引入向量库。

### 3.9 任务编排

选择：

- 第一版不引入 `LangGraph / Temporal`
- 先用普通 Python service 层编排

原因：

- 当前任务链路还不长
- 真正的复杂度在数据模型和交互，不在工作流中间件
- 过早引入编排框架会分散实现重点

结论：

第一版仍然用普通 service functions 即可。

---

## 4. 第一版明确不用的技术

为了让“激进”落在正确位置，第一版明确不用：

- `Graphiti`
- `Microsoft GraphRAG`
- `Neo4j GraphRAG`
- `Weaviate`
- `LangGraph`
- `Temporal`
- `PDF / 网页自动导入`
- `关系图主视图`

当前的激进，不等于第一版就把所有重技术都堆上去。

---

## 5. 第一版推荐架构

### 5.1 逻辑结构

建议拆成 5 层：

1. `Ingest Layer`
   - 接收 Markdown
   - 创建 Source
   - 切分 Segment

2. `Extraction Layer`
   - 调 LLM 抽取 Event / Entity / Relation / Evidence 候选

3. `Graph Persistence Layer`
   - 把抽取结果写入 Neo4j
   - 做 canonical id 归一和重复合并

4. `Timeline Projection Layer`
   - 从 Event 图中投影出主时间线
   - 计算主线 / 支线
   - 构造前端展示树

5. `Interaction Layer`
   - 节点详情
   - 节点编辑
   - 图邻域追问

### 5.2 API 方向

第一版建议至少有这些接口：

- `POST /sources`
  - 导入 Markdown
- `POST /sources/{id}/extract`
  - 执行结构化抽取并写入图谱
- `GET /timelines/{source_id}`
  - 获取某来源的时间线投影
- `GET /events/{id}`
  - 获取事件详情与证据
- `PATCH /events/{id}`
  - 修改事件
- `POST /events/{id}/chat`
  - 围绕节点发起追问

---

## 6. 第一版图谱结构建议

### 6.1 Node Labels

- `Source`
- `Segment`
- `Event`
- `Entity`
- `Evidence`

### 6.2 Core Relationships

- `(Source)-[:HAS_SEGMENT]->(Segment)`
- `(Segment)-[:DESCRIBES]->(Event)`
- `(Segment)-[:MENTIONS]->(Entity)`
- `(Event)-[:INVOLVES]->(Entity)`
- `(Event)-[:SUPPORTED_BY]->(Evidence)`
- `(Evidence)-[:FROM_SEGMENT]->(Segment)`
- `(Event)-[:PRECEDES]->(Event)`
- `(Event)-[:PARENT_OF]->(Event)`
- `(Event)-[:RELATED_TO]->(Event)`
- `(Entity)-[:RELATED_TO]->(Entity)`

### 6.3 Event 核心属性

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

### 6.4 Evidence 核心属性

- `id`
- `quote`
- `confidence`
- `source_id`
- `segment_id`

---

## 7. 第一版工程取舍

### 7.1 为什么第一天就上图数据库

因为你现在已经明确把长期正确性放在第一位。  
第一版不是为了证明“时间线能画出来”，而是为了证明“这条时间线来自一个可持续生长的研究图谱”。

### 7.2 为什么还不上 GraphRAG

因为当前需要的不是“大规模图摘要系统”，而是：

- 单用户
- Markdown first
- 事件图谱
- 时间线投影
- 节点邻域追问

GraphRAG 适合后续更大规模的资料和更重的检索增强。

### 7.3 为什么仍然不引入向量库

因为第一版的问题还不在“全局语义搜索”，而在：

- 事件抽取是否可信
- 时间归一是否可控
- 图关系是否合理
- 时间线交互是否顺手

向量库会在第二阶段更有价值。

---

## 8. 第一版目录建议

如果下一步开始实现，建议把仓库整理成这个形态：

```text
knowledge-graph/
  docs/
    investigate/
    mvp/
    tech/
    model/
  backend/
    app/
      api/
      services/
      graph/
      schemas/
      prompts/
  frontend/
    src/
      components/
      pages/
      timeline/
      api/
```

---

## 9. 验证顺序

建议按这个顺序推进：

1. `Markdown 导入`
2. `Segment 切分`
3. `LLM 抽取 Event / Entity / Evidence`
4. `写入 Neo4j`
5. `按时间投影时间线`
6. `证据详情联动`
7. `事件编辑`
8. `graph neighborhood chat`

每一步都应该可以在当前 [article.md](../../article.md) 上直接验证。

---

## 10. 结论

第一版技术路线明确如下：

- 后端：`Python + FastAPI`
- 前端：`React + TypeScript`
- 时间线组件：`vis-timeline`
- 主存储：`Neo4j`
- 输入：`Markdown`
- 抽取：`LLM 结构化抽取`
- 时间归一：`规则优先 + 人工修正`
- 节点问答：`graph neighborhood context`
- 编排：`普通 service 层`

一句话总结：

> 一期只限制输入，不限制底层；产品范围保守，但研究图谱底层从第一天就按 graph-first 搭。

---

## 11. 下一步

现在最合理的后续动作只有两个：

1. 写 `数据模型文档`
2. 写 `首个原型实施计划`

其中优先级更高的是：

> 直接把 `Source / Segment / Event / Entity / Evidence / Relation` 的图谱模型定死，然后开始做最小原型。
