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
| Executed retrieval/chunking comparisons | [Comparison results](./comparisons.md) | Live vector vs keyword comparison and local tokenizer/boundary comparison, with raw evidence and limits |
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
- **Next:** Broaden the completed retrieval comparison and run retrieval on alternative chunkings; repeat answer evaluation; independently verify relevant claims and carry out the proposed new source-support check. [My explanations of the choices are recorded](./research.md#my-takeaways-from-the-technical-research-and-checks). A working foundation does not complete every research or release requirement.

## Help and contribution

Megan chose the application focus, intended users, initial camera/topics, vector direction and free-option preference; supplied learning resources/notes and privately entered account credentials. AI researched supporting sources, prepared code and paraphrases, reviewed outputs and ran the checks labeled as AI-executed. Those activities are not presented as Megan’s independent reading, peer feedback or authored reflection.


## Peer feedback: homepage readability — November 16, 2026

[GitHub issue #1](https://github.com/mtm5913/RAG-Research/issues/1) records feedback received from a peer and posted by the project owner because the peer could not post directly. The peer reported crowded homepage headline letters/words and process text too small to read: “source → represent → retrieve → answer → check”. The peer was not identified by name in the supplied feedback.

**Decision and changed documentation:** Accept the feedback. Remove negative tracking from the homepage headline and its italic text, add a little word spacing, and use 1.25 line spacing. Increase the process text from 8px desktop / 6px mobile to 14px at both sizes with 1.7 line spacing. Let the card grow and its content flow vertically so wrapped text does not overlap the note. Preserve the wording and site colors. This section records the feedback, decision, change, checks and next step in the existing research record.

**Actual checks:** AI-assisted review of local production builds at 1440 × 1000 and 390 × 844. Both headlines use normal letter spacing; process text computes to 14px. No document-level horizontal overflow was observed (1425px content at a 1440px viewport; 375px at a 390px viewport). The process text wraps on mobile and stays inside its card, below the note. Both headlines and process cards were also visually inspected in Chrome at actual 200% page zoom; content reflowed and the reviewed text remained visible without overlap. Chrome zoom was reset afterward. Production build and internal-link checks passed before adding this review section (154 internal references); final release checks are attached to the issue.

[View the updated desktop homepage screenshot](/peer-review/homepage-desktop.png).

**Help and limits:** AI made the CSS changes, drafted this record and performed the browser/build checks at Megan’s request. The peer supplied the original feedback; these follow-up checks are not a peer retest or a comprehensive accessibility audit. No new employer-source review or RAG answer-quality test is claimed by this visual change.

**Peer follow-up — November 16, 2026:** Megan relayed the peer’s response to the updated homepages: “Yeah that looks much better”. This confirms the peer perceived an improvement after the typography changes. The response did not specify a device, browser, zoom level, or separate test of each text element, so those details are not claimed.

**Decision / next:** Keep the revised typography. Peer confirmation is now recorded; no additional change was requested in this response. Deployment and issue-resolution evidence remains in the linked GitHub issue. Recheck readability if the homepage layout or wording changes.
