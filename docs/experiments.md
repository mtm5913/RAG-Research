# Experiments & checks

**Status:** a real, isolated Qdrant embedding/retrieval smoke test was executed November 14, 2026. Megan subsequently supplied successful terminal output for Qdrant authentication, Groq generation and the combined synthetic retrieval/generation pipeline. These are user-reported executed results. Megan also supplied a real-source pilot response. The five-case evaluation suite remains planned; the single observed real-source case is reviewed below.

## Real-source trace — prepared, not executed

**Source:** [NPS: How to Photograph Acadia’s Night Skies](https://home.nps.gov/articles/000/night-skies-photography-acadia.htm), updated October 14, 2021; checked November 14, 2026. The article presents ranger guidance. Selected prose has no separate third-party attribution observed; images, captions and logos are excluded. [NPS ownership policy](https://www.nps.gov/aboutus/disclaimer.htm#ownership) generally places NPS-created material in the public domain. This is an attribution-based permission assessment, not written individual permission.

**Representation:** three manually checked paraphrase passages, not verbatim extracted chunks. PHOTO-05-C01 covers equipment/manual mode; C02 covers experimental settings and star-trail context; C03 covers focus/release/white balance. General guidance must stay distinct from verified EOS R1 operations. The versioned local manifest records the original URL, section, date, permission basis and transformation.

**Proposed retrieval:** query the separate `photography_pilot_v1` collection with the same 384-dimensional MiniLM model used for indexing; retrieve up to three passages with source IDs. The synthetic collection remains separate. Model-tokenizer chunk-size verification and comparison with another chunking strategy remain pending; these short manual passages do not prove an optimal chunk size.

**Question:** “What starting settings could I try for a starry sky with a tripod, and how should I focus?”

**Expected evidence:** C01 for tripod/manual mode, C02 for experimental aperture/ISO/exposure suggestions and star trails, C03 for manual focus using a distant bright light. A proposed answer can give those general starting points with passage citations; it must say they are conditional NPS guidance, not tested R1 settings. A missing C03 would reveal incomplete evidence for focus. A confident R1-specific guarantee would exceed this source.

**Import status:** Megan’s subsequent successful query returned all three real-source passages from the separate pilot collection. This demonstrates those indexed passages were available to retrieval; a separate importer output was not supplied. The real-source response is reviewed below.

## Exact evaluation questions — planned

| ID | Exact question | Expected evidence | Failure criteria |
| --- | --- | --- | --- |
| E1 | What starting settings could I try for a starry sky with a tripod, and how should I focus? | C01–C03: manual mode/tripod; conditional settings; distant-light manual focus | Missing focus or stability context; invented R1 specificity; missing/incorrect citations |
| E2 | How can I photograph stars without streaks, and what exposure range does this guide suggest? | C02: Earth’s rotation/star trails, 10–20 seconds as an experiment | Guarantees no trails for every lens; invents an R1 maximum |
| E3 | What exact EOS R1 menu buttons turn on remote shooting? | No supporting passage in pilot | Invents menu paths or claims the NPS source provides R1 instructions |
| E4 | Should I use autofocus or focus on a faraway bright object for this setup? | C03: manually focus using distant bright light | Omits manual focus or invents an autofocus mode |
| E5 | What shutter speed freezes a basketball player indoors? | Outside this pilot’s coverage | Reuses night-sky exposure values as sports guidance instead of acknowledging missing evidence |

For each run preserve question, returned passage IDs/ranks, answer, citations, model, settings, outcome and date. Compare E1/E2 paraphrases against a keyword baseline. Passing citation-ID validation proves IDs exist, not that claims are supported. Review each claim against its cited passage.

## Observable app stories — planned acceptance checks

| Story | Observable check | Status |
| --- | --- | --- |
| Ask a typed night-sky question | Input produces a short checklist, explanations and inspectable source passages | Synthetic CLI plumbing observed via Megan’s output; real-source answer and website UI pending |
| Ask for an unsupported R1 procedure | Answer states missing evidence; no invented menu path | One synthetic missing-settings case passed; real-source E3 pending |
| Inspect a citation | ID resolves to the returned passage, original URL and section; unsupported IDs withhold answer | Seven automated pipeline checks pass locally, including citation rejection and corpus separation; factual support still reviewed manually |
| Encounter an API failure | Clear error without credentials or a fabricated answer | Mac certificate issue observed and corrected; quota/timeouts need controlled checks |
| Import as owner | Only an authenticated owner may change the corpus; visitors cannot upload or replace it | Local hidden-key importer prepared; deployed owner authorization not implemented |

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

**Subsequent user-reported result:** Megan supplied HTTP 200/status ok with collection `photography_smoke_test` from the prepared authenticated server check. Keys were entered privately; none were shared in chat.

## Combined synthetic retrieval and generation — executed, user-reported

On November 14 Megan supplied the CLI output for the exact question: “What exact aperture, shutter speed and ISO should I use on a Canon EOS R1 for a starry sky?” Qdrant returned SYNTHETIC-01 first (0.39016587), SYNTHETIC-02 second (0.14912388), and SYNTHETIC-03 third (0.017931856). Groq `openai/gpt-oss-120b` generated an answer that cited SYNTHETIC-01 and explicitly declined exact settings because the passages lacked them. Citation-ID validation passed. Reported usage: 331 prompt tokens, 195 completion tokens, 526 total; provider total_time 0.431809615 seconds, not end-to-end latency.

**Observed scope:** the synthetic integration and one missing-evidence behavior worked. No hosted app, import authorization enforcement or broad reliability claim follows from this synthetic case. A separate Groq API test also returned HTTP 200 and acknowledged missing settings. Local automated tests use mock responses and do not count as live cloud tests.

## Remaining results log

For each further exercise save date, source, question, configuration, expected evidence, actual observation, explanation, limitation, and next step. Keep app performance and answer-quality claims separate from this bounded plumbing test.

## Real-source pilot — executed, user-reported

**November 14, 2026.** Megan supplied the `--real` CLI output for the default exact EOS R1 starry-sky settings question. Retrieved passages: PHOTO-05-C02 first (0.65089595), C01 second (0.5213499), C03 third (0.37628973), each retaining original URL and section. Groq returned a generated answer citing C02, labeled the guidance as general experimental starting points rather than an R1-specific recipe, and listed f/1.4–f/3.5, ISO 400 and 10–20 seconds. Usage: 660 prompt tokens, 328 completion tokens, 988 total; provider total_time 0.718832268 seconds is not end-to-end latency.

**Review:** retrieval and citation-ID checks succeeded. The numbers match the reviewed NPS paraphrase, but answer quality needs improvement: “longer times will start to show star trails” overstates a conditional risk, and the answer omitted the tripod context attached to the exposure suggestions. It added lens/sky-brightness/desired-effect qualifiers that were not all explicit in the indexed text. This is a partial answer-quality result, not an unqualified pass.

**Change:** prompt now requires conditional star-trail wording, tripod context for long night-sky exposures, no unstated explanations and a clear distinction between general guidance and exact R1 instructions. This revised prompt has not yet been retested live. Seven local mock-based pipeline tests pass; those do not measure answer quality.

**Next:** run the prepared five-question evaluation suite, including focus, unsupported R1 menu instructions and an out-of-domain sports question. Returned-ID inclusion is checked automatically; factual support and refusal behavior require review. Because the pilot has only three passages and retrieval requests all three, this does not establish selective retrieval quality. Expand the authorized corpus and compare rankings with a keyword baseline before making such a claim.
