# Release Evidence Record — template

**Release identifier:** [enter]  
**System / service:** [enter]  
**Owner:** [enter]  
**Created at (UTC):** [enter]  
**Pipeline run / evidence links:** [enter]

## CHANGE — What changed?

| Field | Observed evidence and link |
| --- | --- |
| Source repository and full commit SHA | [enter] |
| Change / pull request and review | [enter] |
| Build workflow / run ID | [enter] |

## PROVE — What made progression justified?

| Gate / check | Result / evidence | Fresh for this release? | Owner / override decision |
| --- | --- | --- | --- |
| Unit tests | [enter] | [enter] | [enter] |
| Integration/contract tests | [enter] | [enter] | [enter] |
| Coverage floor (where applicable) | [enter] | [enter] | [enter] |
| Security / secrets / dependency checks | [enter] | [enter] | [enter] |
| Runtime checks after deployment | [enter] | [enter] | [enter] |

**Decision:** PROCEED / HOLD. **Reason / approver / timestamp:** [enter]

## PACKAGE — What exactly was built?

| Field | Evidence |
| --- | --- |
| Image repository | [enter] |
| Immutable **registry manifest digest** (`sha256:...`) | [enter] |
| Tag (non-authoritative) | [enter] |
| Build run / toolchain and pinned inputs | [enter] |
| SBOM / provenance / signature (if policy requires) | [enter / N/A with reason] |
| Retention and previous known-good digest | [enter] |

## CONTROL and PROMOTE — What was moved, where and by whom?

| Field | Staging | Production |
| --- | --- | --- |
| Target environment | [enter] | [enter] |
| **Deployed digest** (must match) | [enter] | [enter] |
| Identity / authorisation | [enter] | [enter] |
| Configuration contract | [enter] | [enter] |
| Infrastructure plan ID/checksum if applicable | [enter] | [enter] |
| Approval evidence and timestamp | [enter] | [enter] |
| Strategy (e.g., rolling/canary) | [enter] | [enter] |

**Decision:** PROCEED / HOLD. **Reason / approver / timestamp:** [enter]

## VERIFY — Did the release actually work?

| Observed signal | Staging | Production |
| --- | --- | --- |
| `/health` status and time | [enter] | [enter] |
| `/version` source identity | [enter] | [enter] |
| `/products` contract check | [enter] | [enter] |
| Running artefact identity | [enter] | [enter] |
| Error rate / latency / observability window | [enter] | [enter] |
| Acceptance decision and time | [enter] | [enter] |

## RECOVER — What happened if verification failed?

- **Failure and first meaningful evidence:** [enter]
- **State mutated / blast radius:** [enter]
- **Evidence captured before changing state:** [enter]
- **Recovery options assessed:** [enter]
- **Selected recovery action and authorised owner:** [enter]
- **Known-good candidate verified, available, and compatible?** [enter — each separately]
- **Recovery artefact digest:** [enter]
- **Post-recovery health, identity and business checks:** [enter]
- **If rollback unsafe, explain fix-forward / mitigation decision:** [enter]

## IMPROVE — What will change?

- **Root-cause hypothesis supported by evidence:** [enter]
- **Control/test/observability gap:** [enter]
- **Smallest justified prevention change:** [enter]
- **Owner and due date:** [enter]
- **Follow-up verification / closure evidence:** [enter]

**Final decision:** ACCEPTED / RECOVERED / UNRESOLVED  
**Release evidence retention location:** [enter]
