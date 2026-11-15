# Tools, hosting & resource comparison

**Current implementation, November 14:** the [hosted Fieldlight prototype](https://fieldlight.megan373lab.xyz) uses Qdrant Cloud MiniLM inference, Groq `openai/gpt-oss-120b` fact selection and a separate course-server container. [Actual hosting checks](./experiments.md#hosted-foundation-public-checks-executed) supersede earlier proposed/unexecuted status statements below. The tables preserve alternatives and reasons; historical starting limits are not measured performance. The current selector uses strict JSON schema, low reasoning effort and a 2,000-completion-token cap; it does not generate the displayed checklist wording.


**Research checked November 14, 2026.** AI-assisted comparison for Megan’s proposed EOS R1 photography assistant. These are recommendations for a prototype, not installed services, measured performance, or a final stack approved by Megan. No accounts were created and no deployment/server configuration was changed.

## Constraints that drive the comparison

Megan chose typed questions, checklist answers with explanations and citations, an honest insufficient-evidence response, owner-only source management, the existing course server, and a goal of no additional service charges. The first topics are landscapes and low light, handheld and tripod-based.

The [deployment specification](https://github.com/mtm5913/is373-deployment/blob/main/docs/SPECIFICATION.md) reports an approximately 2 GB RAM / 48 GB disk DigitalOcean host, observed October 27. It describes other websites sharing the machine. [Its ETL configuration](https://github.com/mtm5913/is373-deployment/blob/main/compose.etl.yaml) permits a separate Neo4j container up to 1 GB. These are historical documentation and configuration limits, not a measurement of current free memory. The repository is a read-only reference; nothing there was modified.

**Budget interpretation:** reuse the already-provisioned server and seek free software/API tiers. This does not make the existing hosting or domain free, nor guarantee that free tiers remain available.

## Vector database comparison

| Option | Where it runs | Benefit for this project | Constraint / tradeoff | Assessment |
| --- | --- | --- | --- | --- |
| Chroma, single node | Course server | Straightforward document/vector workflow; no separate hosted database account | Chroma advises against systems below 2 GB; the server’s total RAM is shared. Index memory and other workloads must fit together. | Useful local experiment; not my first deployment recommendation on this host |
| Qdrant, self-hosted | Separate private container on course server | Persistent vector database; control of data and deployment | Adds database maintenance, backups and RAM/CPU consumption. Actual footprint must be measured; no claim it fits yet. | Fallback if external database use is undesirable and capacity checks pass |
| Qdrant Cloud, Free | External managed database; app stays on course server | Keeps the vector index off the shared server | Free prototype tier lists 1 GB RAM, 0.5 vCPU, 4 GB disk and one node, without a card. Limited regions, downtime on upgrades and inactivity suspension/deletion apply. | Recommended first candidate, subject to account eligibility and source/data terms |
| Keyword/structured baseline | App’s local text/metadata store | Inspectable comparison for exact camera terms and section names | Does not demonstrate the chosen vector database path | Keep as an evaluation baseline |

Sources: [Chroma single-node guidance](https://docs.trychroma.com/guides/performance/single-node), [Qdrant local deployment](https://qdrant.tech/documentation/quickstart/), [Qdrant Free cluster details](https://qdrant.tech/documentation/cloud/create-cluster/).

**Reasoning:** Qdrant Cloud is preferred here because of limited shared server memory, not because it has been shown faster or more accurate. Free clusters can suspend after one week unused and be deleted after four weeks without reactivation. Keep the authorized corpus, chunk manifest and regeneration procedure outside the database; check readiness before demonstrations. Cloud API access must be authenticated and used by the backend, never directly by visitors.

## Update: cloud embeddings verified

On November 14, a real dashboard smoke test successfully used Qdrant Cloud Inference with `sentence-transformers/all-MiniLM-L6-v2`, the free option Megan observed in her cluster. This is now the preferred embedding path to investigate, instead of loading the encoder on the course server. The database and embedding work can both stay in Qdrant Cloud. A separate generation provider is still required for complete RAG answers.

[Actual test results and limits](./experiments.md#actual-results-qdrant-integration-smoke-test) include the three synthetic records, paraphrased query, returned rankings and server reachability check. Availability was verified on this cluster; no paid model was selected.

## Embedding comparison

Embeddings represent text for retrieval; the generation model writes the answer. Choosing one does not automatically supply the other.

| Option | Benefit | Limitation | Proposed use |
| --- | --- | --- | --- |
| `sentence-transformers/all-MiniLM-L6-v2` locally | Apache-2.0 model; 384-dimensional vectors; no per-call embedding API fee | Default truncation after 256 word pieces; runtime still consumes RAM/CPU and query latency must be measured | Fallback candidate if cloud inference is unavailable; server memory and latency remain untested |
| Hosted embedding API | Moves query embedding computation off the course server | Separate quotas, permissions, data handling and model lifecycle; changing models requires a compatible reindex | Qdrant Cloud MiniLM is now the preferred path after the November 14 smoke test; verify limits before importing the corpus |

Source: [MiniLM model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

For MiniLM, propose heading-aware chunks capped at **200 model-tokenizer word pieces including title/heading context**, then compare with another bounded chunking rule. This is a starting hypothesis, not a proven best size. Count with the actual tokenizer and reject accidental truncation. Preserve identical model revision, preprocessing and normalization for documents and questions.

## Free generation API comparison

| Option | What the official documentation establishes | Tradeoff for this app | Assessment |
| --- | --- | --- | --- |
| Groq Free | A Free tier exists; the API is mostly compatible with OpenAI client libraries. Model-specific request/token quotas apply. | Confirm actual model access and organization limits. Data retention has exceptions; source reuse must allow sending passages to the provider. | First generation-provider candidate to test |
| Gemini API Free | Selected models have free input/output allowances; current pricing lists `gemini-3.5-flash-lite` as one example. | Free-tier content may be used for product improvement. Quotas, eligibility and model availability need checking. | Alternative for a controlled prototype using permitted non-sensitive content |
| Self-hosted generation model | Avoids per-request external API fees | Shares the already constrained CPU/RAM; weights, latency and memory have not been tested | Defer; no evidence the course host can support acceptable generation |

Sources: [Groq billing tiers](https://console.groq.com/docs/billing-faqs), [Groq limits](https://console.groq.com/docs/rate-limits), [Groq API compatibility](https://console.groq.com/docs/openai), [Groq data handling](https://console.groq.com/docs/your-data), [Gemini pricing and data-use table](https://ai.google.dev/gemini-api/docs/pricing).

Groq does not retain inference inputs/outputs by default, but some features and reliability/abuse investigations can entail retention; usage metadata is retained. This is not a zero-retention guarantee. Do not infer the account’s free quotas from a Developer-plan table. Record the actual free model ID, limits, date and configuration before a test. Keep billing disabled; quota exhaustion should produce a clear temporary-unavailable response, not an automatic paid upgrade or silent provider change.

## Proposed architecture

**Recommended prototype for Megan to consider:** a small FastAPI service on the course server, Qdrant Cloud Free for vectors, Qdrant Cloud MiniLM inference for embeddings, and a Groq Free generation model selected after account verification. Gemini is the alternative. The Qdrant Free cluster and isolated synthetic test collection exist. The app service and generation provider have not been deployed.

1. **Owner import:** authenticated owner submits an authorized source. Backend checks permissions, extracts/cleans text, removes duplicates and retains document IDs, headings, URLs and passage locations.
2. **Indexing:** tokenize/chunk; generate real embeddings; store vectors, text and provenance in Qdrant. Keep a recoverable source/manifest copy and record model revision and collection configuration.
3. **Visitor question:** backend validates length, applies request limits and embeds the typed question. Metadata distinguishes EOS R1-specific sources from general photography guidance.
4. **Evidence:** retrieve a bounded candidate set, inspect relevance and support, and attach passage IDs. A high similarity score alone is not proof that the question can be answered.
5. **Answer:** send only the question and selected permitted passages to the configured provider. Return a short settings checklist, brief explanations and validated citations. If support is missing, acknowledge that and ask a useful clarification rather than inventing settings.
6. **Deployment:** use a separate app container/Compose project behind the existing HTTPS proxy. Persist required state; keep credentials server-side. This page proposes that arrangement without modifying the deployment repository or live server.

## Starting resource limits — proposed, not measured

- Five candidate source documents; import only after permission review. Exclude photographs, menus and unrelated webpage boilerplate.
- One app worker initially; no concurrent bulk embedding jobs on the server.
- Question limit: 1,000 characters. Initial retrieval: top 4 passages, at most 1,000 embedding-tokenizer word pieces combined; also validate the generation provider’s token budget.
- Answer cap: 500 output tokens. One active generation per visitor; initial server-wide cap of 2 concurrent generations.
- Initial public limit: 3 questions/minute per visitor plus a shared provider-budget guard. Tune against verified account quotas; identify proxy clients correctly.
- On timeout, quota failure or database suspension: report temporary unavailability, preserve the question locally only if appropriate, and make no unsupported model-only answer.

## Verification required before selection

Measure current host memory, disk and workload; benchmark query embedding and app memory with other services running; verify Qdrant region, authentication, persistence and inactivity behavior; verify provider Free eligibility, exact model ID and quotas; resolve source permissions including external processing. Then run the same evidence/citation questions on each viable candidate. Record failures, latency and resource observations. No performance tests, API requests, imports or deployments have been executed for this comparison.
