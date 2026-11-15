# Executed comparisons

**November 14, 2026. AI-executed technical checks for Fieldlight; Megan’s independent verification and personal takeaways remain separate.** These comparisons use the current two-source, seven-passage paraphrase corpus. No production collection, model, credentials or deployed app code was changed.

## Index to evidence

- [Retrieval inputs, rankings, metrics and actual public responses (JSON)](/retrieval-comparison.json)
- [Chunk records, token counts, offsets and boundary checks (JSON)](/chunking-comparison.json)
- [Download the reproduction scripts and corpus (ZIP)](/comparison-reproduction.zip)
- [Source permission assessments](./sources.md) · [Tool alternatives](./tools.md) · [Previous failures and retests](./experiments.md)

## 1. Vector retrieval versus a keyword baseline

### What actually ran

The baseline ranked the **same stored passage text** by the number of unique exact query tokens shared with it, using an explicit stopword list. Ties were broken by source ID; it returned four passages even when scores were zero. This is a deliberately simple lexical baseline, not BM25 or a tuned full-text search engine.

For vector retrieval, the same seven questions were submitted to the **live public app**. The backend uses Qdrant Cloud inference with MiniLM and returns four passages in retrieval order. Returned passage wording and original URLs were checked against the local corpus manifest after removing the same project annotations the app removes. Questions were spaced to respect the app’s request limit. No provider keys were read. The raw artifact records the corpus hash and UTC execution timestamps.

The retrieval metrics ignore generated answer prose. They measure whether the predeclared relevant passage IDs are returned, not whether an answer is correct. The R1 menu question has no supporting procedure, so it is excluded from recall/rank averages.

### Questions and actual results

“Rank” means the first expected passage’s position, within the four returned passages. N1 needs three passages; both methods retrieved all three.

| ID | Exact question | Expected evidence | Keyword rank / recall@4 | Vector rank / recall@4 |
| --- | --- | --- | --- | --- |
| W1 | How can I make a waterfall look smoother in a landscape photo? | PHOTO-06-C02 | 1 / 1.00 | 1 / 1.00 |
| A1 | How does aperture affect depth of field in an outdoor landscape photograph? | PHOTO-06-C03 | 1 / 1.00 | 1 / 1.00 |
| G1 | When is golden hour, and what is its light like for landscapes? | PHOTO-06-C04 | 1 / 1.00 | 1 / 1.00 |
| N1 | What starting settings could I try for a starry sky with a tripod, and how should I focus? | PHOTO-05-C01–C03 | 1 / 1.00 | 1 / 1.00 |
| P1 | How can I give falling water a silky appearance while keeping the camera still? | PHOTO-06-C02 | 1 / 1.00 | 1 / 1.00 |
| P2 | How could I give a cascade a silky appearance rather than freeze its motion? | PHOTO-06-C02 | Not in top 4 / 0.00 | 1 / 1.00 |
| U1 | What exact EOS R1 menu buttons turn on remote shooting? | No supporting procedure | Not scored | Not scored; live app refused |

Across the **six answerable questions**, macro recall@4 and mean reciprocal rank@4 were **0.833 for the keyword baseline** and **1.000 for vector retrieval**. Recall@4 is the fraction of expected passages in the first four results, averaged per question. Reciprocal rank@4 is one divided by the first relevant result’s rank, or zero if none appears in the first four.

### What this supports — and what it does not

The five straightforward cases did not distinguish the methods. P1 still shares useful words such as “water” and “camera.” P2 deliberately tests a more different wording; the lexical baseline had no matching terms and its tie rule did not return the waterfall passage, while the vector result ranked that passage first. P2 was added as a lexical-mismatch stress case **before vector execution**; it is not a randomly selected or held-out query.

This small, purpose-selected set supports keeping vector retrieval for paraphrased photography questions while retaining keyword search as a viable baseline. It does **not** establish a general accuracy advantage, statistical reliability, lower latency or superiority to a stronger lexical/hybrid method. Retrieving four of only seven passages also makes high recall relatively easy. No latency comparison was made because the public route additionally performs generation.

U1 illustrates why a high-ranked passage is not sufficient evidence: both methods return nearby text, including stored project scope notes, but the corpus contains no actual R1 menu procedure. The live app returned insufficient evidence. Project annotations participate in the stored text for both retrieval methods; they are separately labeled and excluded from generator evidence. That representation choice remains a limitation to investigate.

**Decision:** keep the current vector path provisionally. These results reveal no demonstrated need for graph traversal: the tested answers use direct passage evidence. The existence of relationships among cameras, scenes and settings is not by itself evidence that a graph database would improve this app. A graph or hybrid choice needs an actual unmet query and a measured comparison.

## 2. Heading passages versus fixed token windows

### What actually ran

This was a **local representation/boundary comparison**, not an alternate-vector-index experiment. The same stored paraphrase text was used, including separately labeled project annotations. Documents were kept separate. Existing hand-prepared passages associated with headings were compared with **64 WordPiece-token windows with no overlap**, and **64-token windows with 16-token overlap**. The 64-token size is a small-corpus boundary stress test, not a recommended universal setting.

Token counts used the actual MiniLM tokenizer configuration, with truncation disabled while counting and special tokens included in reported chunk lengths. Tokenizer package: `tokenizers 0.23.3`; model repository revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. File and corpus hashes are in the artifact. This does not establish the exact revision used inside Qdrant Cloud.

The [model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) describes default truncation beyond 256 word pieces. The measured current passages fit below that bound for this downloaded tokenizer. Future title/heading prefixes, larger sources and cloud preprocessing still need their own checks.

### Boundary criteria and results

Eleven units were the complete source-derived fact wordings used by the current checklist. A twelfth unit joined the exposure suggestions to the stored experimental qualifier and conditional star-trail statement. The check asked whether each complete unit remained within **one** chunk. Those units reflect the existing app’s structure and favor its current boundaries; they are not an independent answer-quality benchmark.

| Representation | Chunks | Largest chunk, tokens incl. specials | Complete units in one chunk | Chunks crossing existing passage boundaries | Total stored tokens incl. specials |
| --- | ---: | ---: | ---: | ---: | ---: |
| Existing heading passages | 7 | 106 | 12/12 | 0 | 405 |
| Fixed 64, no overlap | 7 | 66 | 8/12 | 4 | 405 |
| Fixed 64, overlap 16 | 8 | 66 | 11/12 | 6 | 503 |

The no-overlap version split the settings, release and golden-hour fact units, plus the joined exposure/context unit. Overlap recovered all the individual fact units but still did not keep the long exposure/context span together. It also increased stored tokens from 405 to 503, about **24%**. All measured alternatives stayed below 256 tokens per chunk.

“Split” means evidence may need more than one retrieved chunk; it does not mean the information is lost or an answer necessarily fails. Crossing existing passage boundaries and using overlap are not inherently wrong. This check did not measure retrieval quality, generation quality, index size or request latency for the alternative chunkings, and the live collection was not reimported.

**Decision:** retain the current heading passages for this small extractive checklist. They preserve its required complete fact/context units without duplication and already fit the measured token budget. For larger documents, compare bounded heading-aware chunks and overlapping windows in separate indexes with the same query set before choosing. Do not claim these seven passages establish an optimal strategy for a whole camera manual.

## Changed / checked / next

- **Changed:** added a reproducible keyword baseline, live paired retrieval comparison, tokenizer-based structural comparison and raw evidence downloads.
- **Checked:** seven live queries; six answerable paired retrieval cases; one unsupported-query case; all returned passage texts/URLs matched the local manifest; three chunk representations evaluated against twelve declared units.
- **Next:** stronger lexical baseline, independent held-out questions, separate indexes for alternative chunkings and larger authorized documents. [Megan’s personal takeaways are now recorded](./research.md#my-takeaways-from-the-technical-research-and-checks). Independent verification and her proposed new source-support check remain separate from these AI-executed results.
