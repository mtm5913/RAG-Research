# Course deployment staging

AI inspected only selected routing/network metadata, resource figures and public DNS. Existing network hosting-web, HTTPS entrypoint websecure and resolver letsencrypt were confirmed. Domain nameservers are Porkbun. Proposed fieldlight.megan373lab.xyz had no address returned. Memory available: 755 MB; free disk: 43,201 MB.

A credential-free allowlisted package was transferred over SSH to /home/deploy/fieldlight and verified against SHA-256 b760607c9310e8169ed1d38856e2964abb0b7368938cd6e80faa393287dabbe5. New release b760607c9310 was unpacked into a separate directory; Compose configuration validated and fieldlight:local built using official Python 3.13-slim, resolved image digest e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90. Public routing remains disabled. No existing repository, service or proxy was changed or restarted.

A temporary container ran with network disabled, no keys and no published host port. Health, expanded collection flag and saved-example HTTP flow passed. Observed memory 17.3 MiB /192 MiB. The disposable test container was removed. 21 pipeline tests and 10 local HTTP tests passed, including exact HTTPS origin checks and secret-free health response.

Remaining: Porkbun A record, private provider key setup, live container startup, DNS/certificate verification and public supported/refusal checks. Container build/preview checks do not establish live API access or a hosted release. The local private setup helper is prepared and syntax-checked; it has not saved any credentials or enabled a route yet.

## Hosted foundation — public checks executed

**Public app:** [Fieldlight](https://fieldlight.megan373lab.xyz). Megan ran the private setup helper and supplied a healthy container result. AI then opened the public HTTPS page successfully without a certificate warning, observed Live / Qdrant + Groq and two articles/seven passages, and submitted actual typed questions:

- Waterfall blur: correct, focused PHOTO-06-C02 checklist item; citation button expanded the returned passage and original beginner-guide URL.
- Exact R1 remote-shooting menu buttons: deterministic insufficient-evidence response; no invented menu path.

These are executed public browser checks, not saved examples. They verify this hosted flow for two cases, not the full earlier suite on the public deployment or general reliability. A read-only server check confirmed running/healthy state, restart policy unless-stopped, route enabled, secret directory mode 700 and both secret file modes 600. No key contents were read. Observed app memory was 21.9 MiB /192 MiB at that snapshot.

The separate Compose project uses 0.25 CPU and a 192 MiB cap on the existing course server. It has no published host port and routes through the existing HTTPS proxy. The portfolio, original deployment repository and existing service processes were not changed or restarted by the deployment procedure. The app now runs independently of Megan’s local terminal.

**Changed / checked / next:** hosted foundation and public app link added; 21 pipeline tests plus 10 HTTP tests passed before staging, isolated-container checks passed, and two public live cases passed. Still pending: broader public regressions, baseline/chunk comparisons, load/failure/restart checks and original-source accuracy review. No production-readiness or uptime guarantee is claimed.
