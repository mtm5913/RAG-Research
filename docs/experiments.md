# Experiments & checks

**All app checks below are planned. No retrieval or generation experiment has been executed in this notebook.**

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

## Actual results log

No exercise results recorded yet. For each exercise save the date, source, question, method, actual observation, explanation, limitation, and next step. For any later tool-based experiment, also record its configuration and versions.
