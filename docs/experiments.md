# Experiments & checks

**Status:** a real, isolated Qdrant embedding/retrieval smoke test was executed November 14, 2026. The remaining app checks below are planned. No generated answer or real photography corpus has been tested.

## Start with a learning exercise

Use a short permitted text to explore how content is imported, represented, retrieved, and cited. No app or technology stack is assumed. Begin by inspecting source text and chunk boundaries; add database or model experiments only when ready.

## Trace one source — workshop task

Choose a real permitted passage. Record its document ID and exact location, the proposed chunk or graph fact, a useful question, expected evidence, proposed answer and citation. Then explain what would count as missing or contradictory evidence. This trace is pending; a diagram alone would not be an executed check.

## Evaluation questions — draft categories

Replace these prompts with exact questions and expected source passages after choosing the corpus.

| ID | Question type | Evidence needed | Failure to watch for |
| --- | --- | --- | --- |
| Q1 | Exact term appearing in a source | Identified passage with that fact | Correct term, incorrect passage |
| Q2 | Paraphrase of Q1 | Same evidence despite different wording | Relevant passage missed |
| Q3 | Relationship question, if supported | Explicit relationship and its passage | Invented connection |
| Q4 | Question spanning nearby context | All necessary qualifiers and units | Chunk boundary removes context |
| Q5 | Deliberately unanswerable question | Confirmed absence from selected corpus | Unsupported confident answer |

## Bounded comparisons

1. Run the same questions against the keyword/structured baseline and selected database approach. Preserve returned IDs, passage text and ranking.
2. Compare paragraph/heading chunks and fixed-size chunks if choosing vectors; compare two bounded schema or retrieval choices if choosing graphs. Keep other settings constant and explain the observed tradeoff.

## Small learning exercises

| Exercise | What to observe | Status |
| --- | --- | --- |
| Divide one text two ways | Which boundaries preserve the meaning and source location? | Planned |
| Explain a vector comparison | What does similarity indicate, and what does it leave uncertain? | Planned |
| Sketch a small graph | Which entities and relationships are explicit in the source? | Planned |
| Trace one question to evidence | Is the passage sufficient to support an answer? | Planned |
| Try an unsupported question | What evidence would be missing? | Planned |

## Actual results: Qdrant integration smoke test

**November 14, 2026; executed by AI through the authenticated dashboard at Megan’s request.** Cluster photography-rag was Healthy on the Free tier, AWS us-east-2, Qdrant v1.20.1.

Created a separate collection, `photography_smoke_test`, with 384-dimensional vectors and cosine distance. Inserted three original synthetic passages via Cloud Inference using `sentence-transformers/all-MiniLM-L6-v2`. Each payload explicitly records `synthetic: true`, a source ID and passage text. Upsert returned completed/status ok.

Question: **“How can I take pictures of the night sky using a stable camera support?”** Same model for query embedding; requested three results with payloads.

| Rank | Source ID | Synthetic content | Similarity score |
| --- | --- | --- | --- |
| 1 | SYNTHETIC-01 | Stars at night, camera on a tripod | 0.5264486 |
| 2 | SYNTHETIC-02 | Daytime mountains, trees and lake | 0.30493823 |
| 3 | SYNTHETIC-03 | Cooking vegetable soup | -0.05513684 |

Query returned `status: ok`, 15 inference tokens and server-reported time 0.07756809 seconds. This is not measured end-to-end latency; scores are not confidence probabilities.

**Result:** real cloud embeddings and vector retrieval worked; the intended synthetic topic ranked first with preserved metadata. The isolated test collection remains for repeatability. No photography documents were imported, no generation model was called, and missing-evidence behavior, citations and keyword-baseline comparisons remain untested.

### Course-server checks

Read-only SSH connection succeeded using the existing course key and an already trusted host IP. Current snapshot: total memory 1967 MB; available 730 MB; no swap. An HTTPS request from that server to Qdrant without a key returned HTTP 403: network/TLS reachability worked, while authenticated access has not yet been demonstrated. No deployment-repository changes, server writes or service restarts were performed.

**Next required input:** the saved API key must be entered into a private hidden prompt to complete an authenticated server test. Do not put it in chat or GitHub. The prepared local connection-check script sends it over SSH stdin without writing a server file.

## Remaining results log

For each further exercise save date, source, question, configuration, expected evidence, actual observation, explanation, limitation, and next step. Keep app performance and answer-quality claims separate from this bounded plumbing test.
