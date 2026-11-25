# Chapter-by-chapter reading map

**New to command-line work?** Start with [First-time setup](first-steps.md) and the [local lab](local-lab.md).

This is an **optional implementation companion**. The book's chapters remain readable without running anything here.

| Book chapter | Evidence and judgement taught | Corresponding repository material |
| --- | --- | --- |
| **1 — Design the Release System** | The evidence contract and six questions | `README.md`, `docs/architecture.md`, `evidence/release-evidence-template.md` |
| **2 — Prove Every Change** | Distinguish meaningful gates from decorative checks | `app/test_shop_api.py`, `scripts/test.sh`, `.github/workflows/ci.yml` — **not** a complete security stack |
| **3 — Build Once and Identify What You Built** | Build once; authoritative registry digest; retain artefacts | `app/Dockerfile`, `scripts/build-local.sh`, `.github/workflows/release.yml` — note local image ID vs registry digest |
| **4 — Control Environments, Configuration, Identity, and Infrastructure** | Externalise configuration, control who can change environments | `ENVIRONMENT` runtime variable, GitHub `lab-production` protected environment setup, `docs/aws-mapping.md` — AWS OIDC/Terraform not implemented |
| **5 — Promote the Same Release Safely** | Keep identity and decision continuity across environment boundaries | `scripts/promote-local.sh` and the staging/production jobs in `release.yml` — **not** a real 5% canary |
| **6 — Recover from Failed Releases** | Preserve evidence, check known-good availability/compatibility, recover and re-verify | `scripts/rollback-local.sh`, deliberate health failure in `docs/local-lab.md` |
| **7 — Improve Flow Without Weakening Evidence** | Do not weaken the confidence floor for speed; observe the first meaningful failure | `docs/validation.md`, `docs/failure-scenarios.md` — no simulated operational metrics |
| **8 — Capstone: Design and Operate a Complete Release** | Three decisions: promote, recover, improve; complete the Release Evidence Record | `evidence/example-release-evidence.md` (fictional), `evidence/release-evidence-template.md`, `scripts/make-local-record.py` |

## How the capstone relates to the lab

Chapter 8 is a **reasoning case study**: the application, infrastructure and pipeline are assumed to exist. It does not ask readers to provision AWS or write a CI platform. This companion adds an *opt-in* runnable lab and never substitutes a passing test for engineering judgement. In particular, the book's worked example contains a 5% canary and AWS controls; this small lab does not claim to recreate those controls.
