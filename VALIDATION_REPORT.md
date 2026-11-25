# Companion repository — validation record

**Review date:** 4 November 2026  
**Method:** Offline checks executed in the authoring environment; local Docker checks reported from the reader's MacBook terminal session on 4 November 2026. Do not substitute a stated PASS for a command that has not actually been observed.

## Results actually observed

| Check | Status | Observed evidence |
| --- | --- | --- |
| Python compilation | **PASS** | `python3 -m compileall -q app scripts tests` |
| Shop API tests | **PASS** | 5 tests, including deliberately unhealthy `/health` returning HTTP 500 |
| Evidence Record and journal tests | **PASS** | 7 tests total: original 4 digest/record tests plus 3 local journal/chronology tests (tested in authoring environment) |
| Bash syntax | **PASS** | All supplied `.sh` scripts parse with `bash -n` |
| Workflow YAML parsing | **PASS (syntax only)** | Two workflow YAML files loaded by parser; this is **not** execution in GitHub Actions |
| Host preflight, reader's Mac | **PASS** | Python **3.11.4**, Docker server **20.10.11**, `Preflight PASS` |
| First local Docker build | **PASS** | `./scripts/build-local.sh good-v1` built image `sha256:62c072e10504b4caac10d97e8ce99226dca4f7c797f3753009fac8dd856753b1` |
| Local staging promotion | **PASS (started)** | `promote-local.sh staging` reported **PROMOTED (not yet verified)** with same ID |
| Local staging verification | **PASS (verified)** | `/health` 200; `/version good-v1`; `/products` 200; `VERIFIED: staging good-v1` with matching full ID |
| Local production promotion/verification | **PASS** | Author-provided MacBook transcript: `good-v1` checked `/health 200`, `/version good-v1`, `/products 200`, with same local image ID as staging |
| Controlled production failure and rollback | **PASS** | Author-provided MacBook transcript: `candidate-v2` image `sha256:ab1c283fb94e08ab50d84d3277989c01bec444ef2eb81c86a3fbd6d607d264fd` verified in staging; failed production `/health` HTTP 500; rollback restored `good-v1`, endpoints verified; pre-rollback log preserved |
| Local chronological journal (new change) | **PASS (synthetic offline test only)** | Unit test replays deployment, failure and rollback events and checks that the final Markdown record retains the failed candidate; Mac live exercise predates the change |
| GitHub CI / GHCR registry-digest workflow | **NOT YET OBSERVED** | Requires published repository, configured permissions and actual workflow execution |
| AWS ECR / live deployment / Terraform | **NOT IMPLEMENTED** | Outside this deliberately small companion repository |

**Identity distinction:** The `sha256:62c0...` above is a **local Docker image ID**, not a remote registry manifest digest. The book's actual cross-environment registry-digest principle is illustrated in the GitHub Actions workflow but must be separately validated after publication. The two local environments are on the reader's Mac, not AWS.

## Acceptance criteria before declaring the working lab fully tested

1. Verify the first image in **both** local environments, with matching image IDs and healthy endpoints.
2. Verify the second image in staging, deploy it with a deliberately failed health check in production lab, and **observe verification failure** (not a pass).
3. Capture failure evidence, assess that the stateless first image is verified/available/compatible, roll back and observe **post-recovery verification**.
4. Generate and interpret the local Release Evidence Record, noting omitted security and registry controls honestly.
5. After publication, confirm the GitHub workflows really run, capture the published **registry manifest digest**, and confirm both temporary GHCR lab stages use it. Check environment protection separately.

The book remains self-contained, and the documentation updates do not change any already-tested application or deployment script logic.

## Record completeness limitation and correction

The author supplied a local release record on 4 November 2026 after a verified rollback. It correctly showed current production `good-v1`, but lacked the failed `candidate-v2` promotion/verification history. The generator now reads an event journal which logs both failures and recovery on **subsequent** runs. The earlier run is grounded in the author-provided Terminal output and failure log; its past events are **not** automatically claimed by the journal. The new journal and record generation were tested with a synthetic rollback history; an updated end-to-end Docker re-run remains unobserved.
