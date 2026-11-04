# Chapter 8 — fictional release evidence example

> **Illustrative case study only.** All SHA and digest values below are abbreviated exactly as in the manuscript. They are **not real artefact identities, test results, AWS resources, or evidence of deployment**. Use the blank template for real releases.

| Evidence field | Case-study observation |
| --- | --- |
| System / release | Shop API / `shop-app:9f32a7c` |
| CHANGE source revision | `9f32a7c` |
| PROVE unit / integration | PASS / PASS |
| PROVE coverage | 84% (floor 75%) |
| PROVE security gate | PASS |
| PACKAGE digest (abbreviated) | `sha256:8a3f…` |
| Supply chain | SBOM attached and signature verified **where policy requires** |
| Identity | Federated CI release role (OIDC), in the book's AWS scenario |
| Target configuration | Validated before each target change |
| PROMOTE | staging → production, same digest |
| VERIFY staging | `/health` 200, `/version` `9f32a7c`, `/products` 200 |
| Production promotion decision | Approved based on available evidence |
| Production strategy | 5% canary **in the book's scenario**, not implemented in this repository |
| VERIFY production, initial | `/health` 200, `/version` `9f32a7c` |
| Failure at canary | `/health` 500, with error-rate and latency evidence preserved |
| Recovery decision | Roll back after checking a known-good, available, compatible target |
| Known-good recovery candidate | `shop-app@sha256:5c9e…` (abbreviated) |
| Post-recovery verification | `/health` 200, `/version` `64b18dc`, `/products` 200 |
| Improvement | Add a contract check for the downstream interface and staging endpoint verification; assign owner and follow-up |

**Why this matters:** the decision was not simply "was the deployment green?" It was whether the evidence justified promotion, recovery, and system improvement. Chapter 8 gives five additional failure cases (flaky test, missing credential, infrastructure/application mismatch, failed health check, destructive migration). The local lab deliberately exercises **only the failed-health-check / safe-rollback path**, with a controlled runtime configuration mismatch rather than a 5% traffic canary.
