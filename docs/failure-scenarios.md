# Chapter 8 failure-scenario worksheet

The five cases below correspond to the book's capstone. They are **decision exercises**; this repository automates only a controlled failed health check and local recovery.

| Chapter 8 scenario | What to examine before acting | Repo support |
| --- | --- | --- |
| A. Flaky test | First failure, timing, isolation, quarantine owner, evidence quality | Reasoning exercise only |
| B. Missing production credential | Should a pre-deploy check have stopped mutation? What state changed? | Reasoning exercise only; no real secrets used |
| C. Infrastructure change succeeds, app not ready | Reviewed plan identity/checksum; actual state; readiness gap | Reasoning exercise only; no Terraform apply |
| D. Health fails after deployment | Preserve failure, confirm prior known-good availability and compatibility, roll back and re-verify | **Runnable local lab** (stateless Shop API) |
| E. Destructive migration proposed | Expand/migrate/contract compatibility; why reverting the image may not revert data | Reasoning exercise only; no database |

After each scenario, write a **promotion, recovery and improvement decision** in `evidence/release-evidence-template.md`. Never report a result as executed if it was only a hypothetical case.
