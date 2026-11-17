# Executed source-to-answer trace

**2. Individual RAG app + technical research · November 17, 2026**

This responds to [issue #2](https://github.com/mtm5913/RAG-Research/issues/2). Two typed questions were run against the [public Fieldlight app](https://fieldlight.megan373lab.xyz), which displayed **Live · Qdrant + Groq** and two articles/seven passages. These were new live requests, not saved examples. Canon material was not imported for this check.

## 1. Permitted original passage and location

**Source:** [How to Photograph Acadia’s Night Skies — National Park Service](https://home.nps.gov/articles/000/night-skies-photography-acadia.htm), updated October 14, 2021. Original source rechecked November 17, 2026.

**Location:** **Set Up**, third suggested-settings bullet, beginning “Choose a shutter speed”. Its exact wording is:

> Choose a shutter speed from 10 to 20 seconds and experiment with different variations to get the best result.

The article's **Equipment List** includes a sturdy tripod. That context matters: this bullet is not a handheld EOS R1 exposure prescription.

**Import basis:** The article introduces the guidance as advice from Acadia park rangers. The [NPS ownership policy](https://www.nps.gov/aboutus/disclaimer.htm#ownership) generally permits reuse of NPS-created material while identifying third-party and trademark exceptions. The existing corpus records a prose-only, attribution-based reuse assessment; no separate third-party prose notice was observed. This is not individual written permission. Images, captions, logos, and Canon sources are excluded. See the [permission record](./sources#photography-source-plan).

## 2. Representation and citation metadata

The existing import uses checked **paraphrases**, not verbatim extraction. The source bullet is represented in **PHOTO-05-C02**, together with related settings and star-trail context. Its metadata identifies the original article and section:

```json
{
  "collection": "photography_expanded_v1",
  "point_id": 2,
  "document_id": "PHOTO-05",
  "source_id": "PHOTO-05-C02",
  "title": "How to Photograph Acadia's Night Skies",
  "url": "https://home.nps.gov/articles/000/night-skies-photography-acadia.htm",
  "section": "Set Up (suggested settings)",
  "accessed": "2026-11-14",
  "synthetic": false,
  "permission_url": "https://www.nps.gov/aboutus/disclaimer.htm#ownership"
}
```

The stored representation includes the exposure range as an experiment and separate project scope notes. Before answer selection, `separate_pilot_annotations` removes those notes from the source-derived text. They are not treated as statements made by NPS. The full stored chunk and separated text are in the [trace artifact](./source-trace-2026-11-17.json).

**Embedding/retrieval configuration:** The existing importer uses `sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions, cosine distance, and payload metadata. The live pipeline asks Qdrant for four passages. This session inspected the importer and pipeline; it did not re-import the corpus or directly audit the hosted vector configuration.

## 3. Actual supported retrieval and answer

**Typed question:** What starting exposure settings could I try for a starry sky with a tripod?

**Observed order in the live evidence list:** PHOTO-05-C02 → PHOTO-05-C01 → PHOTO-06-C02 → PHOTO-05-C03. The traced settings passage was first. The waterfall passage PHOTO-06-C02 was also retrieved but was not selected in the answer; this remains a relevance limitation.

**Observed answer claim:** The checklist presented the exposure range as experimental, cited PHOTO-05-C02, and retained the tripod/night-sky context. It explicitly said the range does not guarantee absence of star trails. The C02 citation expanded the actual returned paraphrase and its original article link.

**What generates the answer:** Groq selects allowed fact IDs; the server renders checked wording and citation IDs. This is constrained answer assembly, not unconstrained generation. The answer can support a source-attributed experiment in that context; it cannot establish an optimal exposure, guaranteed sharp stars, handheld guidance, or an EOS R1-specific procedure.

**Result: Pass for this bounded source-support check.** Retrieval ranking, source accuracy, and answer reliability are not established for every question.

[Supported result screenshot](./supported-source-trace-2026-11-17.png)

## 4. Actual handheld low-light evaluation

**Typed question:** What shutter speed should I use for a handheld low-light landscape on the EOS R1?

**Expected:** Explain insufficient source support. Do not recommend exact shutter speed or transfer tripod-based settings to handheld shooting.

**Failure criteria defined before judging the result:** Any unsupported numeric shutter recommendation, or treating tripod guidance as handheld instructions, is a failure. A request/transport failure is inconclusive, not a pass.

**Observed retrieval order:** PHOTO-05-C02 → PHOTO-05-C01 → PHOTO-05-C03 → PHOTO-06-C02. The dangerous near-match (tripod settings) was first, making this a useful answer-grounding check rather than a no-results refusal.

**Actual displayed answer:**

> The available source does not provide enough evidence for this question. It contains selected general photography guidance, not exact EOS R1 procedures or numeric settings for every scene.

The separate context notice identified general NPS guidance and the tripod assumption. No shutter speed was recommended in the answer. Expanding C02 showed the retrieved exposure numbers in the evidence panel; their presence there is source inspection, not a recommendation.

**Result: Pass in this live run.** Neither failure criterion occurred. One successful refusal does not establish general correctness or model determinism.

[Handheld result screenshot](./handheld-low-light-2026-11-17.png)

## Changed / checked / next

**Changed:** Added this executed source trace, original passage location, representation metadata, supported answer boundary, and handheld evaluation outcome. Added links from the Overview and Experiments.

**Checked:** Original NPS article and ownership policy rechecked; actual hosted questions and expanded C02 evidence observed through the browser. Browser text captures and a structured trace are stored in the repository. Scores, raw Qdrant vectors, and raw Groq selections were not exposed by the UI and are not claimed as captured.

**Next:** Broaden the question set and investigate irrelevant retrievals. Continue permission review before importing Canon sources. No hosted application code change was needed for these two checks.
