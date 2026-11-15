# Qdrant smoke test — November 14, 2026

Executed by the assistant through the authenticated Qdrant dashboard, at Megan’s request. No API key was copied into this record.

## Environment

- Cluster: photography-rag; Qdrant v1.20.1; AWS us-east-2; Free tier.
- Isolated collection: photography_smoke_test; dense vector size 384; cosine distance.
- Cloud embedding model requested: sentence-transformers/all-MiniLM-L6-v2. Usage response identifies sentence-transformers/all-minilm-l6-v2.
- Content: three original synthetic test passages, not photography source documents.

## Operations and actual observations

1. GET /collections returned status ok and an empty collection list before creation.
2. PUT /collections/photography_smoke_test returned result true and status ok.
3. Inserted IDs 1–3 with text/model inference objects, source IDs, synthetic=true and passage text in the payload. Upsert returned operation_id=1, completed, status=ok; server-reported time 0.342659511 seconds. This is the service’s response time, not measured browser end-to-end latency.
4. Queried: “How can I take pictures of the night sky using a stable camera support?” with the same cloud model, limit=3 and with_payload=true.

| Rank | ID / source | Synthetic passage | Score |
| --- | --- | --- | --- |
| 1 | 1 / SYNTHETIC-01 | Synthetic test passage about photographing stars at night with a camera on a tripod. | 0.5264486 |
| 2 | 2 / SYNTHETIC-02 | Synthetic test passage about a daytime landscape with mountains, trees and a lake. | 0.30493823 |
| 3 | 3 / SYNTHETIC-03 | Synthetic test passage about making vegetable soup in a kitchen. | -0.05513684 |

Query response: status=ok; time=0.07756809 seconds; inference usage for the model=15 tokens. These scores are similarities, not confidence probabilities.

## Interpretation and limits

PASS for a bounded integration check: cloud-side text embedding, persistence and vector querying worked; the expected synthetic topic ranked first and its metadata was returned. The test collection remains for repeatability. It is separate from any future source corpus.

This does not test photography accuracy, source permissions, real-document parsing/chunking, missing-evidence handling, generation, citations, or the full application. No generation model was called. No keyword-baseline comparison was run. It does not establish an authenticated connection from the course server.

## Course-server read-only checks

SSH connected using the existing course key and an already trusted host IP. No files, services, repo configuration or firewall rules were changed. Memory output: total 1967 MB; available 730 MB; no swap. This is one observation, not a memory allocation guarantee.

Unauthenticated HTTPS GET /collections from the course server returned HTTP 403. This demonstrates DNS/TLS/HTTP reachability and a rejected unauthenticated request, not successful authenticated access. The authenticated server check is pending the saved Qdrant API key. A local script can prompt for it privately, transmit it through SSH stdin and test the API without writing server files.
