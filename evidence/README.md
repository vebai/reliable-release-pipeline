# Using the Release Evidence Record (the main learning outcome)

The **Release Evidence Record** is the centre of _The Reliable Release Pipeline_. It is a short, retained explanation of **what changed, what was proved, what exact artefact was built, what was promoted, whether the running system worked, and what happened during recovery**. It supports decisions; it is not simply a copy of a terminal log.

## Which file should I open first?

| File | Purpose | What to do |
| --- | --- | --- |
| [`release-evidence-template.md`](release-evidence-template.md) | A **blank worksheet** | Make a copy, then enter evidence you actually observed |
| [`example-release-evidence.md`](example-release-evidence.md) | The book's **fictional Chapter 8 scenario** | Read it to see the intended reasoning; do **not** treat its shortened digests as real identifiers |
| `.lab/evidence/local-release-record.md` | **Generated only after** the local exercise runs | Review the fields collected from your Mac/Linux lab and add your decisions |
| `release-record-final` GitHub Actions artefact | **Generated only after** a successful online GitHub workflow | Download from the workflow run to see the actual published GHCR digest and lab verification |

If you are working from a downloadable ZIP, the `.lab/evidence/` directory **does not yet exist**. It is created by scripts during the exercise. The GitHub Actions artefact also does not exist until that workflow has run successfully.

## How to write your own Record

**Where to run:** the following commands are for Mac/Linux Terminal in the repository root. You can also copy the template using Finder or your file manager instead.

After running the local lab and saving your observations, enter:

```bash
mkdir -p .lab/evidence
cp evidence/release-evidence-template.md .lab/evidence/my-release-evidence.md
```

`mkdir -p` creates a folder if it is missing. `cp` makes a copy, preserving the original reusable template. Open your new `.md` file in any text editor. Fill in the answers one stage at a time:

1. **CHANGE:** What source label or full commit actually produced the image?
2. **PROVE:** Which tests ran, and did they pass? Were any tests or scans not implemented?
3. **PACKAGE:** Is your identifier a **local Docker image ID** or an actual **registry manifest digest**? Name it correctly.
4. **PROMOTE:** Which environment received that exact image? Was any approval a real control or only a teaching acknowledgement?
5. **VERIFY:** What did the running service return on `/health`, `/version` and `/products`? What identity was checked?
6. **RECOVER:** What failed, what evidence was preserved, which prior image was available and compatible, what was restored, and what did post-recovery verification show?
7. **IMPROVE:** Which test, configuration check or release policy should change? Who owns the follow-up?

A release can finish **RECOVERED** rather than **ACCEPTED**. A deliberately unhealthy candidate must not be recorded as successfully verified. Write **NOT RUN**, **NOT IMPLEMENTED** or **N/A**, with a reason, when evidence genuinely does not exist. Never invent test results, approvals, AWS actions, canary metrics, security scans, a registry digest or recovery compatibility.

**Critical distinction:** The local image ID is useful evidence that two containers used the same local image. It is **not** an authoritative published registry digest. The GitHub workflow is the part that publishes an image and captures a **GHCR registry manifest digest**.

The blank record remains book-aligned and technology-neutral. Use the [local lab](../docs/local-lab.md) to collect evidence, [failure scenarios](../docs/failure-scenarios.md) to practise decisions, and [reading map](../docs/reading-map.md) to locate the relevant chapters.
