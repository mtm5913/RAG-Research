# Fieldlight browser prototype

Separate from the VitePress research site. Python standard library only; no install needed.

## Start

From the RAG-Research folder:

```sh
python3 app/server.py
```

Open http://127.0.0.1:8765 for a saved-example preview. Saved examples are exact prior live test results, visibly labeled, with known limitations. Typed questions require live mode.

```sh
python3 app/server.py --live
```

Enter the existing Qdrant key, then Groq key privately. They stay in process memory; neither browser nor files receive them. Environment variables `QDRANT_API_KEY` and `GROQ_API_KEY` are also supported. Keep terminal open; Ctrl+C stops the app. Never put keys in a URL or source file. Default backend targets the existing NPS pilot collection; no import, upload or delete route exists.

## Boundaries

The server binds only to loopback, validates host/origin and a per-process request token, accepts bounded questions, allows one live request at a time and three per minute, and strips diagnostic drafts and project notes from browser responses. It sets a restrictive Content Security Policy. Model text is rendered as text with a small allowlist for formatting and citation buttons. Questions and request logs are not saved by this app. Provider data handling still applies to live requests.

General/tripod context and prototype limits always accompany answers. Citation buttons expand the actual returned passage with its original NPS URL. These are AI-prepared paraphrases, not original quotations. Unsupported additions and conditionality errors remain documented; citation-ID checks do not prove factual support. Saved-example answers retain their original flaws and are labeled accordingly.

This is a local browser prototype, not a public production deployment. Server secrets, TLS proxy configuration, deployed access control, process management and resource checks must be configured and verified in a separate app deployment. The original course deployment repo has not been modified. Do not expose this loopback development server publicly.

## Constrained checklist revision

Live NPS answers now use `source_checklist_v1`: Groq selects only an answerable flag and known fact IDs in JSON. The backend verifies IDs against exact allowlisted sentences present in retrieved passages with the expected original URL. It renders the checklist itself; generated wording cannot reach the answer. Exposure selections require equipment and conditional star-trail context. Invalid selections fail closed; insufficient support gets a fixed refusal. This prevents novel model prose in displayed checklists; it does not prove semantic relevance or correctness of the original paraphrases. Saved examples still replay the earlier free-form version and remain labeled.

Restart an already-running server after code changes (Ctrl+C, then the same `--live` command); credentials must be entered again. No existing process or credential file is changed automatically.

### Development diagnostics

The local live server reloads the developer-owned pipeline module between requests, preserving credentials only in its private process closure. Changes to the web server itself still need a restart. Safe validation reason codes may be returned in API responses, but raw model drafts remain excluded. Checklist selection now uses Groq strict JSON Schema with enumerated fact IDs; backend validation remains in place. The initial JSON-object live revision withheld two supported answers; the exact original validation reason was not exposed, so that failure was not fully diagnosed. The stricter revision must be tested live before success is claimed.
