# Expanded source import

Megan supplied terminal output: status ok; collection photography_expanded_v1; documents 2; passages 7; activated_locally true; restart_required false. The importer writes the activation marker only after completed upsert and exact count verification. This is user-reported execution, not an independent AI query. The old pilot and synthetic collections were not targeted by the importer.

The next browser attempt could not connect to port 8765; no expanded live answer was observed. The local app process must be started again for live verification. No credential has been read, persisted or copied by AI.

Prepared UI now reads an expanded-state flag from local server configuration and displays two articles/seven passages plus both source links. Code and mock checks are separate from pending browser verification.

## Expanded corpus browser checks — executed

After the user-reported two-document/seven-passage import, AI confirmed the live interface showed two articles/seven passages and both source links. The original browser tab failed to reconnect; a read-only local HTTP check returned 200, and a fresh IAB tab connected successfully. No additional user restart was needed.

Actual typed questions and observations:

| Question | Expected evidence | Observed result |
| --- | --- | --- |
| How can I make a waterfall look smoother in a landscape photo? | PHOTO-06-C02; slower shutter, steady camera/tripod; no universal exposure time | Relevant passage ranked first and its guidance appeared, but extra night-sky items were selected. Partial initial result; relevance repair below. |
| How does aperture affect depth of field in an outdoor landscape photograph? | PHOTO-06-C03 | Correct aperture/depth-of-field paraphrase with C03 citation; no invented numeric landscape recipe. Pass in this run. |
| When is golden hour, and what is its light like for landscapes? | PHOTO-06-C04 | Correct timing and softer/warmer light paraphrase. Citation expanded the actual passage and the beginner-guide URL. Pass in this run. |
| What starting settings could I try for a starry sky with a tripod, and how should I focus? | PHOTO-05-C01–C03 | All expected evidence returned; constrained checklist retained tripod, manual mode, settings, focus and no-guarantee warning. Pass in this run. |
| What exact EOS R1 menu buttons turn on remote shooting? | No supporting procedure | Deterministic insufficient-evidence response. Pass in this run. |
| What shutter speed freezes a basketball player indoors? | No numeric sports guidance | Deterministic insufficient-evidence response; no transfer of night-sky values. Pass in this run. |

Each query retrieved four of seven passages, so retrieval now excludes some content. Relevant new passages ranked first for the three landscape questions. This is a small observed set, not a benchmark or proof of ranking quality. A keyword baseline, paraphrase comparison and larger authorized corpus remain pending.

**Waterfall repair:** when the selector chooses the waterfall item, the backend now emits only that item's checked wording. This conservative, single-topic response prevents cross-scene mixing, including star-specific settings. It may omit secondary topics in a compound question; users can ask those separately. A mock regression checks attempted overselection of night-sky settings. 21 pipeline tests pass. The development server reloads this pipeline between requests; no credential re-entry is needed for this change.

**Waterfall live retest:** AI resubmitted the same waterfall question after the patch. The browser displayed only the checked moving-water sentence with PHOTO-06-C02; no night-sky equipment, mode or exposure items appeared. Pass for this bounded relevance repair. No restart or private-key entry was needed. Expanded testing comprises six distinct questions plus this repair retest; results do not establish general reliability.
