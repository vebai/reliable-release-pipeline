# Local Docker lab — your first release, controlled failure and recovery

**Companion to Chapters 2–8 of _The Reliable Release Pipeline_.** In the book, the release engineer examines evidence before deciding whether the release may advance. In this optional lab you can see those decisions applied to a tiny, runnable Shop API.

**Where every command runs:** Mac Terminal or a Linux terminal, from inside the extracted `reliable-release-pipeline` folder. **Do not** run the commands in an AWS shell or inside a Docker container. Copy only the command text, not your terminal's `$` or `%` prompt. If you have never used Terminal, complete [First-time setup](first-steps.md) first.

**Safety:** Here **staging** and **production** are *both disposable containers on your own computer*. They listen on `127.0.0.1:8081` and `127.0.0.1:8082`. They are not cloud environments and receive no real customer traffic. There is no 5% canary; the book's canary scenario is a separate reasoning exercise.

**Learning sequence:** **BUILD → OBSERVE → BREAK → DIAGNOSE → FIX → VERIFY**, while preserving the book's **CHANGE → PROVE → PACKAGE → PROMOTE → VERIFY → RECOVER** evidence record.

## Before starting — check your location and tools

Open Terminal and enter:

```bash
cd ~/Downloads/reliable-release-pipeline
pwd
ls
```

`cd` changes to the project folder; `pwd` confirms where you are; `ls` should include `README.md`, `app`, `docs` and `scripts`. If you extracted the ZIP elsewhere, replace the `cd` path with the real folder path. **Stay in this folder for the rest of the lab.**

```bash
./scripts/validate-repo.sh
./scripts/preflight.sh
```

The first command runs **twelve automated tests**, Python compilation and syntax checks (plus an optional YAML parse). A single test *intentionally* prints HTTP `500` and then `ok`; that is part of the test. The second command verifies that Docker is installed and that the running Docker engine can be reached.

**Continue only if** the first command ends with `PASS - offline repository checks` and the second ends with `Preflight PASS`. If not, follow [Troubleshooting](troubleshooting.md) and investigate the failed step; do not skip it.

## Step 1 — Build the first image (`good-v1`)

**What this proves:** The same source can be packaged as a concrete Docker image with an inspectable identity. This is a local Docker image ID, **not** yet a remotely published registry digest.

```bash
./scripts/build-local.sh good-v1
```

`good-v1` is a human-readable **revision label** for this lab, not an existing Git commit or a filename. The command builds the Shop API image, names it `reliable-shop:good-v1`, and saves its full ID in `.lab/state/last-built`. Docker may download a base image on the first run.

At the end you should see something shaped like:

```text
SOURCE_REVISION=good-v1
LOCAL_IMAGE_ID=sha256:<64 hexadecimal characters>
IMPORTANT: LOCAL_IMAGE_ID is a Docker image ID, not a remote registry manifest digest.
```

The long value differs across builds and machines. **Never copy an image ID from this guide**; use the real one printed by your Docker engine.

Save the value for the next commands by typing:

```bash
IMAGE_V1="$(sed -n '1p' .lab/state/last-built)"
printf '%s\n' "$IMAGE_V1"
```

`IMAGE_V1` is a **shell variable**: a temporary name holding a long value so you do not have to retype it. Keep the quotation marks and `$`. `sed -n '1p'` reads the first line of the saved file. You should see a full `sha256:...` image ID. The variable lasts only while that Terminal session stays open; the file stays on disk. See [Troubleshooting](troubleshooting.md) if you close Terminal.

## Step 2 — Deploy and verify **staging**

**What this proves:** The deployment action is not the same as verification.

```bash
./scripts/promote-local.sh staging "$IMAGE_V1"
```

This starts the Shop API in a Docker container named `rrp-staging`, using local port **8081**. Its success message starts:

```text
PROMOTED (not yet verified): environment=staging ...
```

**“Not yet verified” is deliberate.** You have started a container; you have not yet accepted the release.

Now check it:

```bash
./scripts/verify-release.sh staging "$IMAGE_V1"
```

A successful result looks like:

```text
PASS: /health 200; /version good-v1; /products 200; environment staging
VERIFIED: staging good-v1 sha256:...
```

The script also checks that the **running container's image ID** matches the image you asked to deploy. It writes the successful result into `.lab/state/staging.verified`.

Optional: in your web browser, open `http://127.0.0.1:8081/health`, `http://127.0.0.1:8081/version`, and `http://127.0.0.1:8081/products`. You should receive small JSON text responses. The browser display is useful but **does not replace** the version-and-image verification script.

**Stop if this fails.** Read the first meaningful error; try `docker logs rrp-staging`. Do not promote an unverified image.

## Step 3 — Promote **the same image** to the production lab

**Where you are if you already completed staging:** Start here. You do **not** need to rebuild `good-v1` or repeat staging. In a new Terminal session, retrieve the verified staging image ID:

```bash
IMAGE_V1="$(sed -n '1p' .lab/state/staging.verified)"
printf '%s\n' "$IMAGE_V1"
```

You should see the same complete local `sha256:...` ID you used at staging. The next command requires that staging has recorded a successful verification for **this exact image**.

```bash
./scripts/promote-local.sh production "$IMAGE_V1" --approve
```

`production` here means the **second local container**, `rrp-production`, on port **8082**. It does not touch a real production server. The `--approve` option is an **explicit learning acknowledgement**, not an authorised human approval or a substitute for access controls.

Now verify independently:

```bash
./scripts/verify-release.sh production "$IMAGE_V1"
```

Expected successful lines:

```text
PASS: /health 200; /version good-v1; /products 200; environment production
VERIFIED: production good-v1 sha256:...
```

Both **VERIFIED** lines must contain **the same entire image ID**. That is the local demonstration of *build once, promote the same artefact*. The verified production result is saved in `.lab/state/production.verified`.

**Safe stopping point:** You now have one successfully verified lab release in both environments. If you prefer, stop and examine the evidence before creating a failure. You can leave the containers running while you inspect them.

## Step 4 — Build a second candidate (`candidate-v2`)

**What this proves:** A new candidate is a *different* image, but it must be promoted consistently within its own release. Before building, preserve the known-good ID from the first production release:

```bash
IMAGE_V1="$(sed -n '1p' .lab/state/production.verified)"
printf '%s\n' "$IMAGE_V1"
```

Then build the next candidate **once**:

```bash
./scripts/build-local.sh candidate-v2
IMAGE_V2="$(sed -n '1p' .lab/state/last-built)"
printf '%s\n' "$IMAGE_V2"
```

The file `last-built` now refers to **candidate-v2**; do not mistakenly use it to recover the `good-v1` ID. The labels `good-v1` and `candidate-v2` are intentionally simple; they do not imply actual software feature changes.

Staging must still be tested independently for candidate-v2:

```bash
./scripts/promote-local.sh staging "$IMAGE_V2"
./scripts/verify-release.sh staging "$IMAGE_V2"
```

Expected version: `candidate-v2`; `/health` and `/products` should pass. **Stop if staging is not verified.**

## Step 5 — Create a **controlled production-lab failure**

The next command deliberately configures the production-lab container so that `/health` returns **HTTP 500**. This is *not* a new Docker build: it deploys the exact `candidate-v2` image that staging just verified, but with different runtime configuration. This demonstrates the book's warning that a matching artefact does not guarantee matching environment behaviour.

```bash
./scripts/promote-local.sh production "$IMAGE_V2" --approve --simulate-broken
```

Next, run the normal verification:

```bash
./scripts/verify-release.sh production "$IMAGE_V2"
```

**Expected result: FAIL / non-zero exit. This is a successful *failure-detection exercise*, not a successfully verified release.** You should **not** see `VERIFIED: production candidate-v2 ...`. Do not suppress the failure or proceed as if it passed.

The application did not change; the deployment's `SIMULATE_FAILURE=1` runtime setting made the health endpoint unhealthy. The book's actual 5% canary and production metrics are **not** implemented by this local lab.

## Step 6 — Observe, diagnose and check recovery readiness

Inspect what the running container reported:

```bash
docker logs rrp-production
```

`docker logs` prints output from the named container. Look for the request to `/health` and the reported failure. Ask three questions before changing anything:

1. **What failed?** `/health` returned HTTP 500 in the production lab.
2. **What changed?** The same image ID as staging was deployed with a production-only simulated failure setting.
3. **Is recovery safe?** The previous `good-v1` image was previously verified, remains available locally and, in this deliberately **stateless** example, has no database migration or external state to become incompatible with.

You can inspect the earlier image's availability using the saved shell variable from Step 4:

```bash
docker image inspect "$IMAGE_V1" --format '{{.Id}}'
```

It must report that image ID. If it reports “No such image”, stop. **A real system requires more evidence than this:** retention, schema compatibility, configuration and authorised recovery decisions.

## Step 7 — Recover and verify the previously known-good version

Only after confirming Step 6, run:

```bash
./scripts/rollback-local.sh production --compatible
```

`--compatible` means **you** acknowledge that the previous image is safe for this disposable, stateless lab. The script cannot establish that an actual production database or dependency is compatible.

The script first writes the failing container's logs under `.lab/evidence/` (both a stable `production-before-rollback.log` copy and a timestamped archive), then replaces that container with the **previous verified** local image. It **re-runs runtime verification**. Success ends with:

```text
PASS: /health 200; /version good-v1; /products 200; environment production
VERIFIED: production good-v1 sha256:...
ROLLBACK VERIFIED: environment=production ... source=good-v1
```

If you do **not** see `ROLLBACK VERIFIED`, recovery has not been proven. Stop and diagnose.

## Step 8 — Produce and complete the Release Evidence Record

```bash
python3 scripts/make-local-record.py
```

This creates a **local worksheet**, normally at `.lab/evidence/local-release-record.md`. Open it in your text editor, or display it in Terminal:

New runs also append to `.lab/evidence/events.jsonl` when you build, promote, verify (PASS or FAIL) and recover. The worksheet will include a **chronological timeline** that distinguishes failed `candidate-v2` from the restored `good-v1`. The event journal is ordinary local text, not a signed audit log. If you completed the exercise **before the event journal was installed**, your old log and final-state files remain valid observations, but the timeline for that earlier run cannot be reconstructed automatically. Record that history manually from your saved Terminal output.

```bash
cat .lab/evidence/local-release-record.md
```

The worksheet can only fill fields that were actually observed in this local exercise. The final reasoning remains yours. Compare it with the [blank template](../evidence/release-evidence-template.md) and the [fictional Chapter 8 example](../evidence/example-release-evidence.md). Record:

- **Promotion decision:** Why did the first release and staging candidate have enough evidence to advance?
- **Recovery decision:** Why was `good-v1` an available, previously verified and compatible candidate for this particular lab?
- **Improvement decision:** What pre-deployment configuration or smoke check would have stopped an unhealthy production-only configuration before promotion?

**Never invent a registry digest, vulnerability scan, 5% canary result, real approval or AWS deployment.** Mark those items **NOT RUN**, **NOT IMPLEMENTED** or **N/A with a reason**, as appropriate.

## Step 9 — Stop and remove the lab containers

After you have saved what you want from the Record, run:

```bash
./scripts/cleanup-local.sh
```

This stops and removes only `rrp-staging` and `rrp-production`. It **does not** delete local Docker images or `.lab/` evidence. Retaining `.lab/` helps with review, but it contains machine-specific evidence and is intentionally ignored by Git. Keep the **scripts** and **tests**: they are part of the reusable companion repository.

## If something differs from the guide

Read [Troubleshooting](troubleshooting.md). Important examples: Docker isn't running, a port is in use, a shell variable was lost when Terminal closed, the wrong image ID was used, or a verification failed. **Do not skip a failed safety or identity check simply to reach the end of the lab.**
