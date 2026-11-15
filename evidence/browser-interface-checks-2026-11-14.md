# Browser interface verification

Fieldlight lives in app/, separate from the VitePress documentation. Existing portfolio and deployment repositories were not changed.

## Executed

- 8 HTTP integration tests passed against loopback, using a fake provider callback rather than real credentials: live route dispatch, private-field stripping, origin rejection, question length, request limits, saved-example labeling, preview behavior, static security headers and path handling (some combined in one test).
- Existing 10 pipeline tests passed.
- IAB browser: desktop interface rendered; saved E1 answer displayed as saved/not live; citation button expanded its passage and NPS link; E3 rendered insufficient-evidence state; typed question in preview rendered a connection message.
- Responsive check at 390px width: no horizontal overflow observed, stacked cards and readable input. Viewport reset after check.
- Model text rendered via DOM text nodes; generated HTML is never inserted.

## Limits

No live cloud request was run through the new browser interface because provider keys remain private. The existing CLI's user-reported tests establish the underlying pipeline, not a new browser end-to-end test. The preview replays prior recorded answers and preserves their known limitations. The revised short preview error wording was a copy-only adjustment after browser QA.

App is loopback-only and not publicly hosted. Live startup requires private key entry once per server process. Answer-quality limitations remain; this work implements interface behavior and credential separation, not a claim of reliable photography advice.

## Subsequent live browser verification

After Megan started the server with private keys, AI tested the actual browser form (not saved examples). The status displayed Live / Qdrant + Groq.

- Submitted the starry-sky/tripod/focus question; browser returned a LIVE RESPONSE checklist with all three source IDs, manual mode, general/tripod context and conditional star-trail wording. Clicking PHOTO-05-C01 expanded the actual equipment/manual-mode passage and original NPS link.
- The live answer still added camera-shake/fine-tuning explanations absent from the indexed paraphrase; this verification demonstrates integration, not complete factual grounding.
- Submitted the indoor basketball shutter-speed question; browser returned the deterministic insufficient-evidence message, three inspectable passages and no approved numerical sports advice. No unvalidated draft was displayed.
- Both requests were submitted through the form and authenticated by the existing server-side credentials. No keys were read or copied by AI. No server process was stopped because this live process was started by Megan.

The earlier no-live-browser-test limit describes the initial preview phase and is superseded for these two cases only. Public hosting, broader retrieval quality and full answer-quality acceptance remain unverified.
