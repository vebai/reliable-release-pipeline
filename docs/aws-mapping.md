# Mapping this small lab to the book's AWS running example

**Status: mapping only — AWS resources and deployments have not been created, tested or validated by this repository.** The manuscript's Shop API uses AWS, Amazon ECR and federated identity as its running example. The GitHub Actions demonstration uses GHCR because the immediate lab is deliberately small and has no AWS preconditions.

| Book concept | In this repo | What an AWS implementation would additionally require |
| --- | --- | --- |
| Registry as source of artefact truth | GHCR manifest digest | ECR repository, immutable tags/retention policy and ECR registry digest |
| CHANGE → PROVE | Commit, unit and contract tests | Reviewed security, secret and dependency checks per policy |
| PACKAGE | Single pushed image | AWS ECR publish job, digest capture, managed retention and recovery availability |
| Identity / least privilege | Job `GITHUB_TOKEN`, environment reviewer rule | AWS IAM role trust, GitHub OIDC federation, scoped ECR/ECS permissions, distinct environments |
| PROMOTE | Same GHCR digest into ephemeral runners | Persistent deployment target (e.g. ECS service), environment-specific configuration and release concurrency control |
| VERIFY | `/health`, `/version`, `/products` | Real runtime and business signals, CloudWatch, error-rate/latency observation window |
| Canary | Not implemented | Real traffic splitting, threshold evaluation and controlled incremental rollout |
| RECOVER | Manually verified local prior-image restore | Previously verified ECR digest, ECS task/service recovery, compatibility and traffic checks |
| Terraform governance | Not implemented | Reviewed/saved plan, plan identity/checksum, state locking, restricted apply role, drift detection |

An AWS extension must be designed as **a separate, fully validated enhancement**, not as a few untested Terraform resources or a README that implies production readiness. It should include an AWS preflight (account, role, Region, quota, cost, identity), accurate provisioning and cleanup, source-to-ECR digest continuity, staging verification, production approval, rollback compatibility checks, and retained evidence. Do not provision chargeable services simply to use the companion repo.
