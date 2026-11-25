# Validation plan and acceptance criteria

This repository has three deliberately separate evidence levels:

| Level | Test | Meaning |
| --- | --- | --- |
| **Offline** | `./scripts/validate-repo.sh` | Python source compiles; tests and shell syntax pass; YAML parses if parser installed |
| **Local Docker** | `./scripts/preflight.sh` then [local lab](local-lab.md) | Two local containers use the same local image ID, checks detect a failed health endpoint, safe recovery verified |
| **Published GitHub lab** | Run `CI - PROVE` and manual `Release lab` workflows | GHCR registry manifest digest is published once and reused in the staging and production *ephemeral runner* jobs |

## Local success criteria

- Local unit and evidence test suites pass; all Bash scripts parse.
- Chronological local journal records the candidate promotion, failed HTTP verification, recovery start and verified rollback without mislabelling the failed candidate as accepted.
- First local image is deployed to staging; `/health`, `/version`, `/products` pass, including source identity.
- Production with image 1 is refused unless staging image 1 has passed and `--approve` is present.
- Image 2 is built once; staging and production run its **same local image ID**.
- Production-only `SIMULATE_FAILURE=1` produces HTTP 500; verification **fails** and no `verified` state is written for image 2.
- `rollback-local.sh` refuses without an explicit compatibility acknowledgement, refuses a missing previous verified image, preserves failure logs, restores image 1 and verifies endpoints.
- Evidence worksheet distinguishes local image ID from registry digest; no fake security results are recorded.

## Published workflow success criteria

- CI triggers on PR and main push, and its PR build is explicitly **not** the release artefact.
- Manual release runs PROVE, then a single release build/push, outputs `ghcr.io/...@sha256:<64 hex>` from registry.
- Staging and production lab jobs pull the exact same digest and verify app revision plus environment.
- The GitHub `lab-production` environment rule is confirmed by the user in GitHub settings; actual approval can be audited.
- `release-record-final` contains the full commit, digest and verification results; it does not claim AWS deployment or full security scanning.

## Completion log — 4 November 2026

| Validation | Observed status | Supporting evidence / next action |
| --- | --- | --- |
| Offline compilation and tests | **PASS** | Nine Python unit tests; shell syntax; optional YAML parsing |
| Mac preflight | **PASS** | Python 3.11.4, Docker server 20.10.11 |
| First Docker image built | **PASS** | `good-v1`, local image ID `sha256:62c072e10504b4caac10d97e8ce99226dca4f7c797f3753009fac8dd856753b1` |
| First staging promotion and verification | **PASS** | `/health` 200, `/version good-v1`, `/products` 200; verified same local ID |
| First production-lab verification | **NOT YET OBSERVED** | Next: use `production` and verify the already-staged first image |
| Controlled failure and safe rollback | **NOT YET OBSERVED** | Requires two verified candidates/history and deliberate failed check |
| GitHub CI checks | **NOT YET OBSERVED** | Requires live GitHub repository and Actions execution |
| GHCR registry-digest workflow | **NOT YET OBSERVED** | Requires manual workflow and real published digest |
| AWS ECR/ECS/OIDC/Terraform | **NOT IMPLEMENTED** | Intentionally outside the scope of this repo |

The image value shown above is a **local Docker image ID**, **not** an ECR/GHCR manifest digest. The staging and production names refer to disposable **local lab containers**. Update this log **only after observing real results** and preserve failure output as evidence.
