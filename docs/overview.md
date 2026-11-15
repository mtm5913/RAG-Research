# Research index

**2. Individual RAG app + technical research — evolving individual record, updated November 14, 2026.** This notebook is separate from the portfolio research site. Link it under section 2 of the existing combined individual record; it is not an additional submission report.

## Start here

| Evidence | Where to find it | Current status |
| --- | --- | --- |
| Working application | [Fieldlight photography assistant](https://fieldlight.megan373lab.xyz) | Hosted prototype; HTTPS, one supported answer, citation expansion and one unsupported-question response checked publicly |
| Vector/graph research and decision | [Research & comparisons](./research.md) | Vector selected provisionally; explicit relationships remain a comparison, not a demonstrated need |
| Sources and permissions | [Sources & tutorials](./sources.md) | Two NPS prose sources represented by seven checked paraphrases; Canon candidates remain permission-pending |
| Exact questions, failures, changes and retests | [Experiments & checks](./experiments.md) | Synthetic and real-source results, three earlier evaluation rounds, constrained checklist and expanded-corpus browser checks |
| Tools and resource tradeoffs | [Tools & hosting](./tools.md) | Qdrant Cloud MiniLM inference, Groq and a separate course-server container |
| Outstanding work | [Next steps](./roadmap.md) | Baseline/chunk comparisons, broader evaluation and independent source review remain |

## Purpose and bounded scope

Fieldlight helps photographers explore general night-sky and landscape guidance through typed questions, concise source-backed checklist items and inspectable citations. The intended camera is the Canon EOS R1, but the current permitted corpus does **not** establish R1-specific operations. It must refuse unsupported menu procedures and settings for subjects outside its evidence. Camera connection and photo editing remain future ideas, outside this prototype.

The research site documents learning from the beginning: chunking, embeddings, retrieval, graph relationships, import, tool comparisons and evaluation. The application is a separate product linked from this record.

## Actual foundation

The app uses four-passage vector retrieval from seven indexed passages. Groq selects from checked fact IDs using a strict JSON schema; the backend renders the checklist from allowlisted source-derived wording rather than free-form model prose. This prevents novel model wording in displayed checklist items, but selection relevance, completeness and paraphrase accuracy still require review.

A separate Fieldlight container now runs on the course server behind its existing HTTPS proxy. Credentials stay in private server files; none are included in this record or browser responses. The portfolio and existing deployment repository were not modified. [Read the observed checks and limitations](./experiments.md).

## Changed / checked / next

- **Changed:** Defined a photography purpose; compared approaches and tools; prepared permitted prose; built the local interface and separate hosted foundation; replaced unconstrained answers after observing grounding failures.
- **Checked:** 21 local pipeline tests and 10 HTTP tests; bounded local live browser cases; public HTTPS, supported waterfall answer, citation expansion and R1-procedure refusal. User-reported results are distinguished from AI-executed checks in the record.
- **Next:** Complete a keyword baseline and bounded chunking comparison; broaden repeated answer/retrieval evaluation; independently verify source paraphrases and explain the decisions in my own words. A working foundation does not complete every research or release requirement.

## Help and contribution

Megan chose the application focus, intended users, initial camera/topics, vector direction and free-option preference; supplied learning resources/notes and privately entered account credentials. AI researched supporting sources, prepared code and paraphrases, reviewed outputs and ran the checks labeled as AI-executed. Those activities are not presented as Megan’s independent reading, peer feedback or authored reflection.
