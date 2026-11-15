# Groq playground grounding check — November 14, 2026

## Observed

- Groq billing page displayed Free ($0) as Current Plan.
- Playground selected `openai/gpt-oss-120b`.
- Supplied original synthetic passage: “Synthetic test passage about photographing stars at night with a camera on a tripod.” ID: SYNTHETIC-01.
- Asked for exact Canon EOS R1 aperture, shutter speed and ISO, instructing the model to use only this passage, cite its ID and acknowledge missing evidence.
- Actual final answer: “The provided passage does not contain any specific numeric aperture, shutter-speed, or ISO values for shooting a starry sky with a Canon EOS R1, so the evidence is insufficient to give exact settings. 【SYNTHETIC-01】” (typographic spacing normalized).
- Result: this one missing-evidence case passed: no invented numerical settings; passage ID retained.

## Limits and next

This was a manually supplied-context playground check, not an integrated Qdrant-to-Groq API test. No API key created or stored by the agent. One response does not establish reliability, photography correctness or citation validation. Need API connectivity, supported-answer cases, repeated missing-evidence checks and application-side citation validation.

Megan also supplied a terminal result from her course server: HTTP 200, status ok, collection photography_smoke_test. This is user-reported authenticated connectivity evidence, separate from the agent-observed dashboard retrieval test.
