# Findings & Decisions

## Requirements
- Deeply evaluate the方案 in `knowledge-graph/docs/foundation/`.
- Focus on soundness of the plan, not just summarize it.
- Produce a review grounded in specific source locations.

## Research Findings
- The target review scope currently includes four docs:
  - `knowledge-graph/docs/foundation/01-investigate.md`
  - `knowledge-graph/docs/foundation/02-mvp-definition.md`
  - `knowledge-graph/docs/foundation/03-tech-selection.md`
  - `knowledge-graph/docs/foundation/04-data-model.md`
- `01-investigate.md` establishes three strong core principles:
  - timeline-first UI
  - event as first-class object
  - time normalization should be `LLM + rules + human correction`
- `01-investigate.md` correctly prioritizes uncertainty reduction around extraction quality, time normalization, layered timeline interaction, evidence linkage, and node-centric Q&A before over-focusing on infrastructure choices.
- `02-mvp-definition.md` sharply narrows the product scope to a single-user historical research timeline workbench with one primary view.
- `02-mvp-definition.md` still pushes the底层 toward `graph-first` and graph-database-priority storage from day one, which may conflict with the stated MVP principle of minimizing scope.
- The current MVP definition is product-clear, but early signs show possible architectural overreach relative to the first validation goal.
- `03-tech-selection.md` explicitly embraces a strategy of conservative input scope but aggressive infrastructure scope: Markdown-only input, but Neo4j and graph-first modeling from day one.
- `03-tech-selection.md` deliberately rejects GraphRAG, vector DBs, and workflow frameworks for v1, which is good scope discipline relative to the chosen graph-first bet.
- `04-data-model.md` defines a coherent minimal graph around `Source / Segment / Event / Entity / Evidence` and the necessary provenance edges for timeline projection and evidence traceability.
- The data model is internally consistent around provenance and timeline projection, but several behaviors central to the MVP still remain heuristic rather than modeled:
  - how `importance` is assigned and revised
  - how `mainline` is determined reproducibly
  - how duplicate or conflicting events are represented before merge
  - how multi-evidence support and contradictory evidence affect event confidence
- Across the full document set, the main architectural tradeoff is now clear:
  - strong long-term extensibility
  - but higher first-version implementation complexity, especially around graph write correctness, merge logic, and timeline projection rules
- The reference source sample (`knowledge-graph/article.md`) is not clean paragraph prose; it contains nested bullets and a table, which weakens the assumption that paragraph-level segmentation is sufficient for precise event/evidence mapping.
- The scheme emphasizes continuous updates and human correction, but there is still no explicit model for extraction runs, revision lineage, or reconciliation between new extractions and already revised graph objects.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Evaluate by document chain and cross-document consistency | The folder appears to define a staged foundation plan rather than isolated docs |
| Use severity-based review output | User asked for deep evaluation; the highest-value output is prioritized findings |
| Separate product-scope judgment from infrastructure-scope judgment | The docs may be disciplined at the UX level but still too heavy at the system level |
| Validate stated repo constraints against actual files before final judgment | Tech-selection quality depends partly on whether its starting assumptions are true |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| None so far | N/A |

## Resources
- `knowledge-graph/docs/foundation/01-investigate.md`
- `knowledge-graph/docs/foundation/02-mvp-definition.md`
- `knowledge-graph/docs/foundation/03-tech-selection.md`
- `knowledge-graph/docs/foundation/04-data-model.md`
- `knowledge-graph/article.md`

## Visual/Browser Findings
- Not applicable yet.
