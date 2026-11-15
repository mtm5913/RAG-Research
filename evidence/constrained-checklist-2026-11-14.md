# Constrained checklist revision

## Implemented

Live NPS requests use source_checklist_v1. The generator chooses an answerable boolean and known fact IDs; the backend rejects arbitrary answer text, unknown/duplicate IDs, inconsistent or incomplete selections. Fact candidates are allowlisted whole sentences from the previously checked paraphrases, admitted only when the exact sentence and expected URL are in a retrieved passage. The backend supplies the wording, source IDs, general/tripod context and no-guarantee warning. Selecting exposure settings also requires equipment and star-trail context. No model prose or draft reaches the browser. Saved example replay remains historical and explicitly labeled.

## Checked

18 local pipeline tests pass, including attempted novel settings, malformed JSON, unsupported fact IDs, missing context, wrong source URL, modified source wording, annotation separation, deterministic refusal and synthetic-path compatibility. Mocked provider calls do not establish actual model-selection behavior. JavaScript syntax and Python compilation pass.

## Pending

The existing user-started live server still has its previous Python module in memory. It must be restarted privately by Megan, retaining no keys on disk. Then retest E1–E5 through the live browser, checking both coverage decisions and selection completeness. This design prevents invented displayed prose but cannot guarantee that selected evidence answers a question, that paraphrases accurately capture the original source, or that retrieval on a larger corpus is effective. No public hosting or source-permission expansion is claimed.

## Initial live check and follow-up

After Megan restarted the live server, AI submitted E1 and E2 through the browser. Both retrieved three passages but displayed answer_withheld instead of a checklist. This is a failure on supported questions. The browser/API boundary hid validation reason codes, so the exact reason was not established; no causal diagnosis is claimed. Remaining tests were paused to avoid repeating the same failed path.

Follow-up code uses strict JSON Schema with fact-ID enums, explicit fact_id entries, lower reasoning effort and a larger completion budget. References checked: https://console.groq.com/docs/structured-outputs and https://console.groq.com/docs/reasoning . Safe validation codes now reach the API while drafts stay private. The local development query handler reloads the pipeline module per request so subsequent pipeline adjustments do not require re-entering keys. Web-server changes still require restart. 18 pipeline tests pass; this is not a live success result.

## Strict-schema live browser retest — executed by AI

Megan restarted the local live server with private keys. AI submitted the exact E1–E5 questions through the browser form, using actual Qdrant and Groq requests rather than saved examples. The three-per-minute app limit was respected with a pause before E4/E5.

| Case | Observed display | Outcome for this run |
| --- | --- | --- |
| E1 | Equipment, manual mode, experimental settings, conditional star-trail warning and manual focus, with matching passage IDs. No novel live-view/zoom or camera-shake explanation. | Pass for expected checklist support and context. |
| E2 | Equipment, experimental 10–20-second range and conditional star-trail wording; explicit no-guarantee note. | Pass for exposure qualification. |
| E3 | Deterministic insufficient-evidence response; no exact R1 menu procedure or quoted annotation. | Pass for absent R1 procedure. |
| E4 | Only the checked manual-focus/distant-bright-light sentence, with C03. | Pass for focus technique; no unsupported autofocus comparison. |
| E5 | Deterministic insufficient-evidence response; no numerical sports recommendation. | Pass for out-of-domain behavior. |

All five passed their bounded criteria in this run after the strict-schema revision. This supersedes the initial two withheld supported cases, but does not establish statistical reliability. The exact cause of the earlier selection failures was not independently recovered. A generic no-trails caveat still appears on focus-only answers; it is accurate context but unnecessary for that question. Broader source accuracy, selection relevance on varied questions, selective retrieval with a larger corpus and public hosting remain open. No credentials were read or copied by AI.
