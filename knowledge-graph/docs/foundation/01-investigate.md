# 现有技术调研：面向 AI 辅助研究与图形化学习系统

**日期**：2026-03-18  
**范围**：围绕“文本资料 -> 结构化理解 -> 时间线/关系图/导图等多视图 -> 可交互研究”的系统方向，调研可直接复用或值得进一步验证的现有技术。  
**背景材料**：[article.md](/Users/zhihu/code/m_code/python/lang_primer/knowledge-graph/article.md)

---

## 1. 结论摘要

当前没有一个单一产品，能完整覆盖以下链路：

`多源资料导入 -> AI 抽取事件/人物/概念/关系 -> 时间归一化 -> 多层级时间线编排 -> 关系图切换 -> 围绕节点继续对话 -> 人工校正与持续演化`

但已经存在一组成熟度较高的“积木”：

- 前端研究工作台参考：[Heptabase](https://newsite.heptabase.com/)、[Tana](https://tana.inc/)、[Obsidian Canvas](https://obsidian.md/canvas)
- 图谱构建与 Graph RAG：[Microsoft GraphRAG](https://microsoft.github.io/graphrag/index/overview/)、[Graphiti](https://github.com/getzep/graphiti)、[Neo4j GraphRAG](https://github.com/neo4j/neo4j-graphrag-python)、[LlamaIndex Property Graph](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)
- 文档入口与资料处理：[Zotero](https://www.zotero.org/support/pdf_reader)、[Marker](https://github.com/datalab-to/marker)
- 时间信息抽取：[HeidelTime](https://github.com/HeidelTime/heideltime)、[SUTime](https://nlp.stanford.edu/software/sutime.html)
- 主图数据库与混合检索：[Neo4j](https://neo4j.com/docs/)、[Kuzu](https://docs.kuzudb.com/)、[Weaviate Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search)
- 可视化层：[vis-timeline](https://visjs.github.io/vis-timeline/docs/timeline/)、[React Flow](https://reactflow.dev/)、[Cytoscape.js](https://js.cytoscape.org/)
- Agent / 工作流编排：[LangGraph](https://docs.langchain.com/langgraph)、[Temporal](https://docs.temporal.io/)

对本项目最重要的判断是：

- `时间线` 应该是第一视图，而不是附属视图。
- `事件（Event）` 应该是底层模型的一等公民。
- `时间归一化` 不能只靠 LLM，最好结合规则系统。
- 第一版应该做成 `时间线研究台`，而不是一开始就做全能知识图谱平台。

---

## 2. 问题拆解

你的目标不是做一个普通笔记工具，而是做一套 `AI 辅助研究系统`。它至少要覆盖 5 层能力：

1. `资料入口层`：书籍、博客、网页、对话、手工笔记、PDF。
2. `结构化理解层`：抽取人物、事件、概念、观点、关系、时间。
3. `证据与校正层`：保留出处、置信度、原文片段、人工修订。
4. `多视图投影层`：时间线、关系图、导图、流程图、矩阵。
5. `交互研究层`：围绕任一节点继续追问、补线索、调整权重。

所以调研重点不应只看“哪个工具能画图”，而应看：

- 是否支持从文本中抽结构
- 是否支持时间维度
- 是否支持持续增量更新
- 是否支持证据回溯
- 是否支持多视图投影

---

## 3. 可参考的现成产品

### 3.1 [Heptabase](https://newsite.heptabase.com/)

定位更接近“视觉化研究工作台”。它的白板、卡片、块级链接、AI 研究能力都与本项目的交互形态高度相关。公开帮助中心已出现 [Heptabase MCP](https://support.heptabase.com/en/articles/12679581-how-to-use-heptabase-mcp)，说明其内容结构已经在朝“可被 AI 操作”的方向演进。

适合借鉴的点：

- 白板 + 卡片 + 块级引用的研究交互
- 将阅读材料与结构化卡片连接
- 让 AI 能读白板/卡片结构

不适合直接替代的点：

- 不是为“自动抽时间线”设计的
- 不是事件驱动模型
- 对“主线/支线/折叠层级时间线”不是原生中心能力

判断：

[Heptabase](https://newsite.heptabase.com/) 更像产品形态参考，而不是本项目的底层引擎。

### 3.2 [Tana](https://tana.inc/)

[Tana](https://tana.inc/) 的强项是结构化节点、[Supertags](https://tana.inc/docs/supertags) 和 AI 工作流。它很适合把“人物 / 事件 / 概念 / 来源”做成带字段的对象。

适合借鉴的点：

- 节点对象化
- AI 命令作用于结构化节点
- 适合非线性知识组织

局限：

- 时间线不是主战场
- 更偏“结构化知识库”，不是“研究时间编排器”

### 3.3 [Obsidian Canvas](https://obsidian.md/canvas)

[Obsidian Canvas](https://obsidian.md/canvas) 很适合做本地优先的可视化编辑层参考。它适合连接 Markdown、卡片、链接和手工布局。

适合借鉴的点：

- 本地优先
- 与 Markdown 资料兼容
- 适合做个人研究工作台原型

局限：

- 自动语义抽取能力需要自己补
- 图谱关系、时间归一化、增量知识演化并非其核心能力

### 3.4 [Zotero](https://www.zotero.org/support/pdf_reader)

如果你的输入包含大量 PDF、网页、书摘、论文，[Zotero](https://www.zotero.org/support/pdf_reader) 值得作为资料入口层接入，而不是重复造轮子。

适合借鉴/复用的点：

- 资料采集
- 元数据管理
- PDF 批注
- 来源组织

判断：

[Zotero](https://www.zotero.org/support/pdf_reader) 更适合作为“来源管理层”，而不是主研究界面。

---

## 4. 图谱构建与 Graph RAG 技术

### 4.1 [Microsoft GraphRAG](https://microsoft.github.io/graphrag/index/overview/)

根据 [GraphRAG Methods](https://microsoft.github.io/graphrag/index/methods/)，它的标准流程会从非结构化文本中提取 `entities`、`relationships`、`claims`，再做社区发现、摘要和报告生成。

优势：

- 很适合静态语料的批量建图
- 方法论成熟
- 对“文档 -> 图结构 -> 高层摘要”链路支持完整

局限：

- 偏批处理
- 索引成本不低
- 对你的“持续加资料、持续修正、做个人研究工作台”场景，工程重量偏大

判断：

如果要做“文章集/书集的阶段性批处理建图”，可以试。  
如果要做“边学边补资料、边改线索”的系统，它不一定是最顺手的第一选择。

### 4.2 [Graphiti](https://github.com/getzep/graphiti)

[Graphiti](https://github.com/getzep/graphiti) 的定位非常贴近你的方向：面向 [temporal knowledge graph](https://github.com/getzep/graphiti) 的增量更新、历史查询和时态感知。

优势：

- 支持时态图谱
- 支持持续增量写入
- 适合动态数据和持续演化的知识
- 明确强调 point-in-time 查询

这点对你特别重要，因为你的系统不是“一次性出一张图”，而是：

- 不断新增资料
- 不断修正线索
- 不同时间会形成新的理解

判断：

如果底层想优先围绕 `时间 + 图谱 + 持续更新` 设计，[Graphiti](https://github.com/getzep/graphiti) 是最值得优先验证的候选之一。

### 4.3 [Neo4j GraphRAG](https://github.com/neo4j/neo4j-graphrag-python)

如果主存储考虑 [Neo4j](https://neo4j.com/docs/)，那么 [neo4j-graphrag-python](https://github.com/neo4j/neo4j-graphrag-python) 很值得看。它已经把图数据库、向量检索和 Graph RAG 的连接做好了一部分。

优势：

- 建立在成熟图数据库之上
- 对工程落地友好
- 和 [Cypher](https://neo4j.com/docs/cypher-manual/current/) 生态兼容

局限：

- 更偏工程组件，不是完整研究产品
- 时间建模和研究工作流仍需自己定义

### 4.4 [LlamaIndex Property Graph](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)

更像一个编排和抽象层，方便你在应用里快速试验“文档抽图谱 + 查询 + 检索”。

适用场景：

- 快速试验 [property graph indexing](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)
- 用现成图存储做原型
- 做 retrieval + graph query 的组合实验

判断：

适合作为原型加速器，不一定适合作为长期唯一基础设施。

---

## 5. 时间信息抽取与归一化

这是本项目的关键技术点，重要性高于普通“实体关系抽取”。

### 5.1 为什么不能只靠 LLM

如果只靠 LLM，从文本里抽“时间”，会遇到几个问题：

- 模糊时间表达难统一，如“战后”“同年”“20 世纪 40 年代初”
- 相对时间需要上下文推理
- 同一事件可能出现多个版本
- 中文历史材料里常出现模糊年代、区间、朝代、纪年法

所以更稳的方式通常是：

`LLM 抽事件与候选时间 -> 规则/时态工具做归一化 -> 人工校正`

### 5.2 [HeidelTime](https://github.com/HeidelTime/heideltime)

[HeidelTime](https://github.com/HeidelTime/heideltime) 是多语言、跨领域的 temporal tagger，适合做时间表达识别与标准化。

适合本项目的原因：

- 多语言支持
- 专门处理时间表达
- 适合作为时间线系统的基础能力之一

### 5.3 [SUTime](https://nlp.stanford.edu/software/sutime.html)

[SUTime](https://nlp.stanford.edu/software/sutime.html) 是 Stanford 的规则型时间抽取工具，更适合英文，但它代表了一类值得吸收的方法：`时间表达不应该完全交给生成模型`。

判断：

若系统第一阶段主要处理中文资料，仍应考虑“规则 + LLM”的混合方案，而不是纯生成式抽取。

---

## 6. 资料入口与预处理

### 6.1 [Marker](https://github.com/datalab-to/marker)

如果系统要处理 PDF、EPUB、DOCX、HTML 等材料，[Marker](https://github.com/datalab-to/marker) 很值得试。它擅长把复杂文档转成 Markdown/结构化中间结果，方便后续抽取。

为什么重要：

- 你的研究资料不会永远是纯 Markdown
- 前处理质量直接决定后续抽取质量
- PDF 解析是整个链路里最容易被低估、但最容易拖垮体验的一环

### 6.2 [Zotero](https://www.zotero.org/support/pdf_reader)

除了作为参考产品，[Zotero](https://www.zotero.org/support/pdf_reader) 也可以是实际的资料入口层：

- 存放资料
- 管理元数据
- 保存批注
- 提供引用来源

判断：

如果第一版不想自己重做资料管理，完全可以把 [Zotero](https://www.zotero.org/support/pdf_reader) 当外部资料库来集成。

---

## 7. 存储与检索

### 7.1 [Neo4j](https://neo4j.com/docs/)

如果目标是做可查询、可扩展、可做关系遍历的研究图谱，[Neo4j](https://neo4j.com/docs/) 是最稳妥的主图数据库候选。

适合点：

- 属性图模型成熟
- Cypher 查询成熟
- 与 Graph RAG 生态连接较好

不利点：

- 对个人轻量原型来说偏重

### 7.2 [Kuzu](https://docs.kuzudb.com/)

[Kuzu](https://docs.kuzudb.com/) 是嵌入式图数据库，适合本地优先、轻量化、个人研究工作台原型。

适合点：

- 嵌入式
- 图查询快
- 适合桌面/本地工具实验

判断：

如果第一版先做给自己用，本地优先，[Kuzu](https://docs.kuzudb.com/) 很值得作为轻量候选。

### 7.3 [Weaviate Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search)

研究系统的检索不能只靠向量，也不能只靠关键词。  
[Weaviate](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) 的 [hybrid search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) 明确支持 `BM25 + 向量` 并行融合。

为什么重要：

- 人名、年份、术语很适合关键词精确命中
- 概念追问、同义表达更适合语义检索
- 研究型问答需要两者结合

判断：

如果后续要支持“围绕线索继续追问”，混合检索几乎是必选能力。

---

## 8. 可视化与交互层

### 8.1 [vis-timeline](https://visjs.github.io/vis-timeline/docs/timeline/)

这是当前最适合做第一版 `主时间线` 的候选之一。

优点：

- 原生时间轴交互
- 支持单点事件与时间区间
- 支持缩放、分组、编辑
- 适合做“主线/支线”的时间编排

判断：

如果要尽快把“分层时间线”跑起来，[vis-timeline](https://visjs.github.io/vis-timeline/docs/timeline/) 是优先级很高的选项。

### 8.2 [React Flow](https://reactflow.dev/)

如果你要的不只是展示，而是“可挂载、可折叠、可拖拽、可编排”的研究工作台，那么 [React Flow](https://reactflow.dev/) 很值得用作自定义编辑层。

适合点：

- 节点式 UI 灵活
- 可自定义节点和边
- 适合构建“事件卡片 + 支线挂载 + 手工调整”

判断：

[React Flow](https://reactflow.dev/) 更像研究工作台画布层，不是纯关系图引擎。

### 8.3 [Cytoscape.js](https://js.cytoscape.org/)

更适合关系图、概念图、人物网络，而不是主时间线。

适合点：

- 图网络表达成熟
- 适合人物关系与概念关联

局限：

- 用来做时间编排不自然

### 8.4 [TimelineJS](https://timeline.knightlab.com/docs/)

更适合最终展示型、叙事型时间线，而不是你要的研究编辑器。

判断：

可作为“对外展示导出层”候选，不适合作为主研究界面。

---

## 9. Agent 与工作流编排

### 9.1 [LangGraph](https://docs.langchain.com/langgraph)

如果后续会有很多长链路操作，例如：

- 导入资料
- 切块
- 抽实体/事件
- 时间归一化
- 生成主线
- 构图
- 生成解释与追问建议

那么 [LangGraph](https://docs.langchain.com/langgraph) 这种可持久化、可检查点的 agent/workflow 编排框架很适合做中控层。

### 9.2 [Temporal](https://docs.temporal.io/)

如果系统以后变成较重的生产级后台，有大量长时任务、重试、补偿、异步批处理，[Temporal](https://docs.temporal.io/) 值得考虑。

但对于第一版个人研究系统：

- 太重
- 上手成本高

判断：

第一版优先 [LangGraph](https://docs.langchain.com/langgraph) 或者更轻的自定义任务编排；[Temporal](https://docs.temporal.io/) 放到后续阶段。

---

## 10. 推荐的第一阶段技术组合

如果目标是尽快做出一个能验证核心价值的 MVP，我建议的组合是：

### 方案 A：偏稳妥、适合尽快验证

- 资料入口：`Markdown + 手工摘录` + [Zotero](https://www.zotero.org/support/pdf_reader)
- 文档预处理：[Marker](https://github.com/datalab-to/marker)
- 抽取层：`LLM + 规则`
- 时间归一化：[HeidelTime](https://github.com/HeidelTime/heideltime)
- 主存储：[Neo4j](https://neo4j.com/docs/)
- 检索：`向量检索 + 关键词检索`
- 主视图：[vis-timeline](https://visjs.github.io/vis-timeline/docs/timeline/)
- 关系视图：[Cytoscape.js](https://js.cytoscape.org/)
- 工作台编辑层：[React Flow](https://reactflow.dev/)
- 编排：[LangGraph](https://docs.langchain.com/langgraph)

### 方案 B：偏时间图谱探索

- 资料入口：`Markdown + PDF`
- 文档预处理：[Marker](https://github.com/datalab-to/marker)
- 图谱层：[Graphiti](https://github.com/getzep/graphiti)
- 主图数据库：[Neo4j](https://neo4j.com/docs/) 或 Graphiti 支持的后端
- 主视图：[vis-timeline](https://visjs.github.io/vis-timeline/docs/timeline/)
- 工作台：[React Flow](https://reactflow.dev/)

这套更贴近你“线索会持续生长”的设想。

### 方案 C：先做本地个人版

- 资料入口：本地 Markdown / PDF
- 抽取：LLM + 规则
- 图存储：[Kuzu](https://docs.kuzudb.com/)
- 时间线：[vis-timeline](https://visjs.github.io/vis-timeline/docs/timeline/)
- 工作台：[React Flow](https://reactflow.dev/)

这套适合先做个人学习原型，成本更低。

---

## 11. 当前最值得优先验证的点

第一轮技术验证，不建议同时验证所有东西。建议按下面顺序压缩不确定性：

1. `事件抽取质量`：能否从一篇历史文章中稳定抽出事件、人物、概念、关系。
2. `时间归一化质量`：能否把“1940 年代初”“战后”“同年”等表达归一。
3. `分层时间线交互`：主线展开、支线折叠，这个交互是否真的提高理解效率。
4. `证据挂载`：每个时间线节点能否回溯出处与原文。
5. `节点对话`：围绕某个事件节点继续追问，是否真能帮助深入研究。

这些问题比“先选哪种数据库”更核心。

---

## 12. 建议暂缓的内容

以下内容不建议在第一版投入过多：

- 全自动生成所有视图
- 复杂协作能力
- 很重的多用户权限系统
- 过早设计庞大 ontology
- 一开始就做生产级任务系统

第一版最重要的是验证：

`时间线作为研究主界面，是否真的比纯文本整理更有效`

---

## 13. 最终判断

就你的方向而言，现有技术里最值得重点关注的不是某一个“大而全产品”，而是下面这条组合路线：

`[Zotero](https://www.zotero.org/support/pdf_reader) / [Marker](https://github.com/datalab-to/marker) -> [Graphiti](https://github.com/getzep/graphiti) 或 [GraphRAG](https://microsoft.github.io/graphrag/index/overview/) -> [Neo4j](https://neo4j.com/docs/) -> [vis-timeline](https://visjs.github.io/vis-timeline/docs/timeline/) + [React Flow](https://reactflow.dev/) -> 节点对话`

其中最关键的差异化点有 3 个：

- `事件中心建模`
- `时间归一化`
- `主线/支线的分层时间线交互`

如果这 3 个点成立，这个系统就不是“另一个知识管理工具”，而会更像一套真正的 `AI 辅助研究工作台`。

---

## 14. 参考链接

### 产品与工作台

- [Heptabase](https://newsite.heptabase.com/)
- [Heptabase MCP](https://support.heptabase.com/en/articles/12679581-how-to-use-heptabase-mcp)
- [Tana AI](https://tana.inc/docs/tana-ai)
- [Tana Supertags](https://tana.inc/docs/supertags)
- [Obsidian Canvas](https://obsidian.md/canvas)
- [Zotero PDF Reader](https://www.zotero.org/support/pdf_reader)
- [Zotero Retrieve PDF Metadata](https://www.zotero.org/support/retrieve_pdf_metadata)

### 图谱与 Graph RAG

- [Microsoft GraphRAG Overview](https://microsoft.github.io/graphrag/index/overview/)
- [Microsoft GraphRAG Methods](https://microsoft.github.io/graphrag/index/methods/)
- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [Zep / Graphiti Docs](https://help.getzep.com/)
- [Neo4j GraphRAG Python](https://github.com/neo4j/neo4j-graphrag-python)
- [LlamaIndex Property Graph Guide](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)

### 时间抽取与资料处理

- [HeidelTime GitHub](https://github.com/HeidelTime/heideltime)
- [SUTime](https://nlp.stanford.edu/software/sutime.html)
- [Marker GitHub](https://github.com/datalab-to/marker)

### 存储、检索、可视化、编排

- [Neo4j Docs](https://neo4j.com/docs/)
- [Kuzu Docs](https://docs.kuzudb.com/)
- [Weaviate Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search)
- [vis-timeline Docs](https://visjs.github.io/vis-timeline/docs/timeline/)
- [React Flow](https://reactflow.dev/)
- [Cytoscape.js](https://js.cytoscape.org/)
- [TimelineJS Docs](https://timeline.knightlab.com/docs/)
- [LangGraph Overview](https://docs.langchain.com/langgraph)
- [Temporal Docs](https://docs.temporal.io/)
