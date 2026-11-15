# Sources & tutorials

## Course research handout

[Open or download the RAG research handout (PDF)](/handouts/RAG.pdf)

[Original Canvas source](https://njit.instructure.com/courses/70733/files?preview=10598448) · [HTML version linked in the assignment](https://kaw393939.github.io/is373-studio/handouts/database-rag-research.html)

The assignment identifies this as the technical research handout. Use it to guide research on vector and graph approaches, chunking, embeddings, import, and evaluation, alongside the project brief. Decisions informed by the handout are still pending. A copy of the supplied PDF is available directly on this site. Reading notes and content verification remain pending.

## Start here: instructor’s student RAG guide

[Build a small RAG system you can explain](https://github.com/kaw393939/is373-rag/blob/main/docs/students/index.md)

This student guide offers optional, step-by-step help for the existing assignment. It recommends a small permitted source set and a traceable path through import, representation, retrieval, generation, and checking. Canvas and the project brief remain the official requirements.

### Beginner learning guides

- [Optional implementation reference: extending an App Studio app](https://github.com/kaw393939/is373-rag/blob/main/docs/students/from-app-studio.md)
- [Learn embeddings](https://github.com/kaw393939/is373-rag/blob/main/docs/students/embeddings.md)
- [Try chunking and source traces](https://github.com/kaw393939/is373-rag/blob/main/docs/students/chunking.md)
- [Plan a question and source set](https://github.com/kaw393939/is373-rag/blob/main/docs/students/plan.md)
- [Run evaluation questions](https://github.com/kaw393939/is373-rag/blob/main/docs/students/check.md)
- [Compare providers and token costs](https://github.com/kaw393939/is373-rag/blob/main/docs/students/ai-costs.md)

**Status:** AI read the student guide index on November 13, 2026. Linked exercises have not been completed or verified here. Personal learning notes and resulting decisions are pending.

## Instructor repository

[IS373 RAG — kaw393939/is373-rag](https://github.com/kaw393939/is373-rag)

The repository provides a VitePress documentation site with draft architecture, a decision register, design reviews, a research library, and an assignment roadmap. Its README states that application services are not implemented. It is an instructor reference, not a mandatory technology stack or a completed student deliverable.

**How I can use it:** study how research connects to decisions, compare its proposed approaches and their tradeoffs, and follow relevant references. My own takeaways and any decisions influenced by it are still pending.

**Source check:** AI inspected the repository README on November 13, 2026. No application code or benchmarks were executed.

## Article I used: vector and graph RAG

[GraphRAG vs. Vector RAG: side-by-side comparison guide — Meilisearch](https://www.meilisearch.com/blog/graph-rag-vs-vector-rag)

**Author:** Maya Shin. **Published:** October 21, 2025; updated August 25, 2026. **Used for:** comparing representation, retrieval, and implementation tradeoffs. **Status:** Megan supplied reading notes on November 14, 2026; AI checked the article and identified qualifications. These are reading notes, not experimental results.

[Read my notes and technical clarifications](./research.md#my-notes-vector-and-graph-rag).

This is a vendor-authored overview. Its speed, accuracy, and product comparisons are claims to investigate, not measured results for this project.

## Tutorials I used

These are the tutorials I used while learning about RAG. Dates, personal takeaways, and related project decisions still need to be added.

| Tutorial | Status |
| --- | --- |
| [YouTube tutorial 1](https://youtu.be/RxHOiCe2tQo?si=-h05JjLBIj2wJ7zA) | Used |
| [YouTube tutorial 2](https://youtu.be/W-_OBmwrNk4?si=BMGY3ubfXjHdByPR) | Used |
| [YouTube tutorial 3](https://youtu.be/xU8CeMhQt1c?si=si3iAS2teJPkc41V) | Used |
| [YouTube tutorial 4](https://youtu.be/cCD303XsUjI?si=uTdJznzy5v2eN-jL) | Used |

## Photography source plan

**Selected for research on November 14, 2026:** one EOS R1 manual and four supplementary guides. These are proposed corpus documents, not an imported or fully permission-cleared collection. The RAG-learning resources above teach implementation; the photography documents below would supply answers.

| ID | Document / publisher | Intended coverage | Permission and import status |
| --- | --- | --- | --- |
| PHOTO-01 | [EOS R1 Advanced User Guide — Canon](https://cam.start.canon/en/C018/index.html) | R1-specific controls and limitations. Proposed scope: whole manual, with sections preserved. | Manual listed on official support site; exact edition and import permission pending. Not imported. |
| PHOTO-02 | [Landscape Photography 101 — Canon New Zealand](https://www.canon.co.nz/get-inspired/landscape-photography-tips) | Aperture priority, depth of field, exposure compensation, ISO and tripod use. | Linked research reference; no public-RAG import authorization recorded. Not imported. |
| PHOTO-03 | [6 Simple Low Light Photography Tips — Canon New Zealand](https://www.canon.co.nz/get-inspired/6-low-light-photography-tips) | Aperture, shutter speed, ISO, focusing and camera shake; handheld and tripod contexts. | Linked research reference; no public-RAG import authorization recorded. Not imported. |
| PHOTO-04 | [Canon Explains Exposure: Basic Manual Settings — Canon Canada](https://www.canon.ca/CanonOutsideOfAuto/learn) | Basic aperture, shutter speed, ISO and exposure-meter explanations. | Linked research reference; import permission pending. Not imported. |
| PHOTO-05 | [How to Photograph Acadia’s Night Skies — National Park Service](https://home.nps.gov/articles/000/night-skies-photography-acadia.htm) | Tripod-based night scenes, manual focus, long exposures and experimental starting settings. | NPS-created material is generally public domain, with exceptions. Selected ranger-guidance prose reviewed against NPS ownership policy November 14. Three paraphrases prepared, excluding all images/captions/logos. Live import pending; see the source trace. |

### Source checks and limitations

- AI inspected the linked guidance on November 14, 2026. This establishes relevance and availability, not Megan’s completion of each reading or an executed retrieval test.
- PHOTO-05 displays an update date of October 14, 2021. Stable publication/version dates for PHOTO-02–04 have not been established; save dated source snapshots if import is authorized.
- The [Canon New Zealand terms](https://www.canon.co.nz/terms-of-use) and [NPS ownership policy](https://home.nps.gov/aboutus/disclaimer.htm) are permission-review references. Public access is not itself a reuse license. Record the applicable permission before copying content into an index or public download.
- Only PHOTO-01 establishes EOS R1-specific operations. The supplementary guides may discuss other cameras or general techniques; do not relabel their examples as tested R1 settings.
- Treat settings as conditional starting points, not universal recipes. Preserve the scene, lens, stability and motion context around any recommendation. Check simplified explanations against the manual and supporting technical sources.

### Proposed import record

For each authorized source, retain document ID, title, publisher, original URL, edition/update date, access date, permission evidence, included sections and stable source locations. Extract article text rather than navigation, advertisements or photographs. Keep heading paths and passage IDs through cleaning and chunking; record duplicate handling, parser configuration, import date and embedding configuration when actually run.

**Status:** five candidate documents identified; zero real documents imported. PHOTO-05 prose pilot is prepared after attribution/ownership review. Canon import permissions and the manual’s edition remain open. [Review the real-source trace and planned evaluations](./experiments.md#real-source-trace-prepared-not-executed).

## Tutorial notes — template

**Title / URL:** pending. **Date used:** pending. **What I tried:** pending. **What I learned in my own words:** pending. **What failed or remains unclear:** pending. **Code or output:** pending. **Decision affected:** pending.
