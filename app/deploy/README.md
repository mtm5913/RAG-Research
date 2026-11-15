# Separate course-server deployment

Deployed at https://fieldlight.megan373lab.xyz . Public HTTPS, supported answer, citation expansion and insufficient-evidence response verified. The staging/setup notes below describe the reproducible procedure. Existing repositories and services were not changed.

- Target hostname: `fieldlight.megan373lab.xyz`
- Course-server IPv4: `137.184.201.122`
- Separate root: `/home/deploy/fieldlight`
- Prepared release: `/home/deploy/fieldlight/releases/b760607c9310`
- Existing external network: `hosting-web`; proxy entrypoint `websecure`; resolver `letsencrypt`
- New Compose project: `fieldlight`; no published host port; route disabled until final setup
- Limits: 192 MB, 0.25 CPU, 64 PIDs; read-only container; unprivileged UID/GID 1000; dropped capabilities

The credential-free image built on the course server. A temporary isolated container passed health, expanded collection configuration and saved-example HTTP checks, using about 17.3 MiB of its 192 MiB limit. It had no external network, credentials or public port, and was removed afterward. Live provider access, DNS, certificate issuance and public browser behavior remain unverified.

## Required setup

In Porkbun DNS for `megan373lab.xyz`, add an **A** record with host **fieldlight**, answer **137.184.201.122**, default TTL. Preserve existing records. The hostname did not resolve during preparation. DNS propagation must finish before final setup.

Run locally:

```sh
python3 /Users/meganmcneal/Documents/ChatGPT/jobs/RAG-Research/app/deploy/finish-course-deploy.py
```

This checks DNS first, then asks privately for the existing Qdrant and Groq keys. They go through encrypted SSH stdin to the course server, are validated against the providers, and are saved only in `/home/deploy/fieldlight/secrets` with directory mode 700/file mode 600. Compose mounts them as read-only files; they are not baked into the image or placed in container environment values. Server administrators retain access. No keys are committed or printed. Do not paste keys into chat.

The helper starts Fieldlight with public routing disabled, waits for container health, then enables only its HTTPS route and checks health again. A healthy result is not proof of an issued certificate: verify the public URL and run supported/refusal checks afterward. Existing apps and proxy are not restarted.

Use `--check-only` to check DNS without entering keys or changing server state. On timeout, inspect status before repeating setup.

## Roll back this app only

On the server, from its prepared release directory:

```sh
docker compose --env-file deployment.env stop app
```

This stops only Fieldlight. Do not run commands against the existing deployment project. Keep the credential files private and excluded from packaging. The package builder uses an explicit file allowlist; secrets are never included.

## Limits

This is a small course prototype behind the existing TLS proxy, not a hardened production service. Shared provider/global rate limits remain active. No owner import endpoint is exposed. The Python development HTTP server's broader production limitations, load behavior and availability require further review before broader use.
