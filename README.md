# The Reliable Release Pipeline — optional companion repository

**Companion to _The Reliable Release Pipeline: A Beginner's Guide to CI/CD — Design, Prove, Package, Promote, Verify, and Recover Software Releases_, by Victor Ebai (2026).**

**You can read the entire book without downloading or running this repository.** The book teaches how to make reliable release decisions. This repository gives you a small, optional example you can examine and run on your own computer.

**The book's model:** **CHANGE → PROVE → PACKAGE → PROMOTE → VERIFY → RECOVER**

The main outcome is a **Release Evidence Record**: a written explanation of what changed, what was tested, what was built, what was deployed, what happened after deployment, and how recovery was handled. The tiny Shop API exists only to give those decisions a real application to work with.

The lab now writes a **chronological local event journal** to `.lab/evidence/events.jsonl`. This records verified passes, failed HTTP verification and recovered releases as separate events. The generated Markdown worksheet shows both the **current state** and the **event history**; it does not claim that older exercises performed before journalling was added were automatically recorded.

## Get the book on Amazon

**Paperback:** [Amazon UK](https://www.amazon.co.uk/dp/B0HQFSPVS5) · [Amazon US](https://www.amazon.com/dp/B0HQFSPVS5) · [Amazon India](https://www.amazon.in/dp/B0HQFSPVS5)

**Kindle eBook:** [Amazon UK](https://www.amazon.co.uk/dp/B0H7PZNFZP) · [Amazon US](https://www.amazon.com/dp/B0H7PZNFZP) · [Amazon India](https://www.amazon.in/dp/B0H7PZNFZP)

## Start here — choose one route

You **do not** need programming, cloud or CI/CD experience to read the documentation. The three routes are independent; choose the one that suits your starting point.

| Route | What you do | Tools/account needed | Where to start |
| --- | --- | --- | --- |
| **Read and inspect** | Read the worked release evidence and architecture; do not run code | None beyond a browser or text editor | [Chapter reading map](docs/reading-map.md) and [completed example](evidence/example-release-evidence.md) |
| **Run a local lab (recommended)** | Test, build, deploy to two local environments, detect failure and recover | Python, Git, Docker; **no GitHub or AWS account** | [First-time setup](docs/first-steps.md), then [local lab](docs/local-lab.md) |
| **Run GitHub Actions** | See CI, one registry image build, promotion of the same digest into two temporary lab runners | A GitHub account and permissions to run Actions and use GitHub Container Registry | [Publish to GitHub](docs/publish-to-github.md), then [GitHub Actions guide](docs/github-actions.md) |

**Already ran the offline tests or staging?** You do not need to start over. Open the [local lab guide](docs/local-lab.md) and continue from the last successfully verified step. Do not delete your `.lab/` directory or rebuild unnecessarily: it contains evidence of your earlier work.

## What you are learning

The book asks six questions. This repository shows where the answers come from:

| Book stage | What the reader should be able to prove | Example here |
| --- | --- | --- |
| CHANGE | Which source revision was used? | `good-v1` and `candidate-v2` local exercise labels; full Git commit SHA in GitHub workflow |
| PROVE | What checks ran and what do their results mean? | Five Shop API tests, seven evidence/journal tests and a CI workflow |
| PACKAGE | What *exact* image was built? | Local Docker image ID; **published registry digest only in the GitHub lab** |
| PROMOTE | Which image crossed into staging and production? | Same image ID in both local containers; same registry digest in GitHub lab |
| VERIFY | Does the running service respond correctly? | `/health`, `/version`, `/products` checks |
| RECOVER | Can we restore a suitable earlier version and verify it? | Controlled failure, inspect evidence, explicit local rollback and re-verification |

**Important:** These stages describe the *reasoning*, not a fixed sequence of CI jobs. Promotion and verification can occur more than once, as they do here.

## What is the Shop API?

An **API** is a program that accepts requests and returns responses. This example is intentionally small. It has only three URLs (called *endpoints*):

- `/health`: returns **HTTP 200** if the application is healthy; during our deliberate failure it returns **HTTP 500**.
- `/version`: reports the release label, such as `good-v1`, and the lab environment.
- `/products`: returns a short, fixed list of products. It is not a real shop and uses no customer data.

**HTTP 200** means a request succeeded. **HTTP 500** means the application reported a server error. A deployment command reporting success does not establish that the running service is healthy; that is why we check the endpoints separately.

## If this is your first command-line project

Open [**First-time setup: every step explained**](docs/first-steps.md). It explains how to download/extract the ZIP, open Terminal, find the correct folder, check Python/Git/Docker, and interpret the text printed after a command. Commands are for your **Mac or Linux computer**, not for the inside of a container or an AWS terminal. Use the commands *without* typing the `$` prompt printed in the book.

Once set up, the lab runs in this order:

1. Run the automated checks; observe **PASS**.
2. Build **one** Docker image, `good-v1`, and record its complete image ID.
3. Deploy it to **staging**, then verify its three endpoints.
4. Deploy **the same image** to **production lab**, then verify again.
5. Build a second image, `candidate-v2`; verify it in staging.
6. Deploy the second image with a deliberately broken **production-only** health response. **Verification must fail.**
7. Preserve failure observations, decide whether the earlier image is available and compatible, roll back in this stateless learning lab, and verify the restored application.
8. Complete your Release Evidence Record, then clean up lab containers.

**Detailed commands, expected output and safe stopping points:** [Local lab guide](docs/local-lab.md). Do not skip directly to rollback; the script expects a previously verified production image.

## Important boundaries: local image ID, registry digest and AWS

A **Docker image** is the packaged application. A **container** is a running instance of that image. A **tag** (`reliable-shop:good-v1`) is a convenient name. A **digest** is a cryptographic identifier.

The local lab returns a complete `LOCAL_IMAGE_ID=sha256:...`. That proves both local containers ran the same image, but **it is not the registry manifest digest** required by the book's cross-environment release model. The manual GitHub Actions lab builds and pushes an image *once* to GitHub Container Registry (GHCR), records the **registry manifest digest** and uses it in both temporary lab environments.

The manuscript uses **AWS and Amazon ECR** as its running example. This small repository **does not create AWS services, ECR repositories, Terraform infrastructure or a persistent production deployment**. It also does not implement the book's 5% canary, full security gates, signing, live monitoring or real database migrations. See [Architecture](docs/architecture.md) and [AWS concept mapping](docs/aws-mapping.md). These omissions are explicit so that no one mistakes a teaching lab for production infrastructure.

## Repository guide

| File or folder | What it contains |
| --- | --- |
| [`docs/first-steps.md`](docs/first-steps.md) | Beginner setup: download, Terminal, commands, Python, Git, Docker |
| [`docs/local-lab.md`](docs/local-lab.md) | Complete copyable lab, one step at a time, including recovery |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | What to do if a command fails or you lose a shell variable |
| [`app/`](app/) | Tiny Shop API, five tests and Dockerfile |
| [`.github/workflows/`](.github/workflows/) | CI checks and an optional manual GHCR release demonstration |
| [`scripts/`](scripts/) | **Keep these files**: tests, preflight, build, promotion, verification, rollback, cleanup and local event journalling |
| [`evidence/`](evidence/) | Blank Release Evidence Record, book-aligned fictional example and guidance |
| [`docs/reading-map.md`](docs/reading-map.md) | How each part corresponds to Chapters 1–8 |
| [`docs/github-actions.md`](docs/github-actions.md) | Optional GitHub release workflow, setup and limitations |
| [`docs/publish-to-github.md`](docs/publish-to-github.md) | How to publish a checked repository without publishing local lab evidence |
| [`docs/validation.md`](docs/validation.md) | What has actually been checked and what remains untested |

## Safety, cost and housekeeping

- The local exercise runs only on **your computer**, listening at `127.0.0.1:8081` (staging) and `127.0.0.1:8082` (production **lab**). Here, “production” is only the name of a second local container. No real users, production service or AWS account are involved.
- Docker may download a Python base image over the internet. The local lab does not provision chargeable cloud infrastructure. GitHub Actions and GHCR can have usage limits or charges; review your account before running cloud-hosted workflows.
- `--approve` is a *learning acknowledgement*, not actual access control. `--compatible` is your explicit judgement that rollback is safe for this **stateless example**; it does not prove compatibility for a real database or service.
- **Keep all `scripts/` files and `app/test_shop_api.py` and `tests/` in the published repository.** Readers need them to reproduce the book's evidence. Only generated files, local logs, temporary state and secrets should be excluded. The `.gitignore` already excludes `.lab/` and Python caches.
- The local and GitHub workflows are demonstrations, **not** production security templates. Never weaken a failed gate merely to make a run green.

**Suggested first click:** [First-time setup](docs/first-steps.md). **Already set up?** Go straight to the [local lab](docs/local-lab.md).
