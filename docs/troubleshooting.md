# Troubleshooting the companion lab — read the failure before changing state

**Where to run commands:** in Mac Terminal or a Linux terminal, from the extracted `reliable-release-pipeline` folder. Start with `cd ~/Downloads/reliable-release-pipeline` if that is where you extracted the ZIP. These checks are for your **own computer**, not AWS.

The book teaches that a failed check is information, not an invitation to bypass it. First note **which command failed**, the **first meaningful error** and the **last known verified stage**. Apply the smallest justified fix, then repeat verification.

## “No such file or directory” when opening the project

```bash
pwd
ls
```

`pwd` shows your current folder; `ls` shows the names inside it. You should find `README.md`, `scripts/`, `app/` and `docs/`. If you are outside the folder, use `cd` with the real location of the extracted folder. On macOS you can check the exact folder location in Finder. Do not move individual scripts away from their project folder.

## “Permission denied” when running `./scripts/...`

First confirm you are using the extracted project folder and have inspected the scripts. The scripts should normally be executable after extraction. If permissions were lost when copying the files, restore executable permission to the project's own shell scripts:

```bash
chmod +x scripts/*.sh
```

Then retry **the original command**. Do not make unrelated system files executable.

## Python version or command error

```bash
python3 --version
```

`python3` must exist. **Python 3.11.4 has been successfully used for these tests**, and the host guide recommends Python 3.11 or newer. The Dockerfile uses Python 3.13 *inside the image*, independently of the Python version installed on your Mac. If `python3` is missing, see [First-time setup](first-steps.md) before proceeding.

The offline check may print a test where `/health` returns **HTTP 500** followed by **`ok`**: this is deliberate and should not be mistaken for a failing test run. Look at the **final summary** and whether all twelve tests pass.

## Docker command exists, but Docker cannot connect

```bash
docker info
```

If it reports that the Docker daemon is unavailable, open **Docker Desktop** on macOS and let its engine start. On Linux, check your Docker installation, service and access following the official [Docker Engine instructions](https://docs.docker.com/engine/install/). Do not use `sudo` on some commands and omit it on others: mixing different Docker contexts may make images appear to be missing. Once the engine is reachable:

```bash
./scripts/preflight.sh
```

Continue only after `Preflight PASS`.

## A local port (8081 or 8082) is already in use

The staging container uses local port **8081**. The production **lab** uses local port **8082**. An error saying a port is allocated means another process or container already uses it. Inspect your Docker containers:

```bash
docker ps -a
```

Look for containers called `rrp-staging` and `rrp-production`. If you want to stop **this project's disposable containers** and you have saved all required observations, run:

```bash
./scripts/cleanup-local.sh
```

This does **not** delete `.lab/` state or images, so do not assume your earlier evidence has reset. If another application owns the port, do not forcibly stop it without checking what it is. The project's fixed lab ports must be free before retrying.

## A `sha256:` image variable appears empty or wrong

Shell variables such as `IMAGE_V1` are **temporary**: they disappear when Terminal closes. The `.lab/state/` files are stored on disk. Recover the ID from the **appropriate verified file**, depending on where you are in the lab:

**After verifying `good-v1` in staging, before promoting it to production:**

```bash
IMAGE_V1="$(sed -n '1p' .lab/state/staging.verified)"
printf '%s\n' "$IMAGE_V1"
```

**After verifying `good-v1` in production, before promoting `candidate-v2`:**

```bash
IMAGE_V1="$(sed -n '1p' .lab/state/production.verified)"
printf '%s\n' "$IMAGE_V1"
```

**After verifying `candidate-v2` in staging, before creating the controlled failure:**

```bash
IMAGE_V2="$(sed -n '1p' .lab/state/staging.verified)"
printf '%s\n' "$IMAGE_V2"
```

**Caution:** `.lab/state/last-built` changes every time you run `build-local.sh`. After building `candidate-v2`, it no longer refers to `good-v1`. Do not blindly reuse that file to choose a recovery target. If you have already deployed the broken `candidate-v2` to production, the rollback script reads the saved `.lab/state/production.previous-verified` and checks it; you do not need to supply the old image ID to rollback.

If a state file is missing or empty, the corresponding step has not produced verified evidence. Recheck the earlier step rather than constructing an image ID by hand.

## The app starts but verification fails

First inspect the container and logs:

```bash
docker ps -a
docker logs rrp-staging
```

Replace `rrp-staging` with `rrp-production` when diagnosing the production **lab**. Look for HTTP status, version mismatch, missing container or port error. The verification script checks **three endpoints plus identity**; a successful `docker run` alone does not establish release success.

**Special case — Step 5:** The command `./scripts/verify-release.sh production "$IMAGE_V2"` **must fail** after `--simulate-broken`. Its failure demonstrates that the gate blocks an unhealthy candidate. **Do not** reinterpret it as a verified production release. Capture the logs before safe recovery.

## Rollback refuses to run

`rollback-local.sh` requires a **previously verified production image** and your explicit compatibility acknowledgement. If you never verified `good-v1` in production, there is no valid recovery target stored in `.lab/state/production.previous-verified`. Do not fabricate evidence or manually create state files. Complete the required verification history first.

If the script reports the previous Docker image is unavailable, do not proceed: the artefact has been removed or is inaccessible. In real systems, this is why artefact retention is part of recovery design. If the compatibility assessment is unclear, stop and investigate; do not supply `--compatible` just to bypass the check.

## Where are the records and generated files?

- `.lab/state/`: local image IDs and verification status files (created by scripts).
- `.lab/evidence/`: local rollback logs (latest and uniquely archived copies), the append-only-in-normal-use event journal `events.jsonl`, and the worksheet generated by `make-local-record.py`. These files are editable; they are not signed audit evidence.
- `evidence/`: the **blank template** and **fictional book example** distributed with the repo.
- `scripts/`, `app/test_shop_api.py`, `tests/`: **reusable validation source files** that must remain in the published repo.

`.lab/`, Python cache files and local secrets are ignored by Git and should not be published. **Never remove validation scripts as part of cleanup.**

## The generated Record shows only `good-v1`, not the failed `candidate-v2`

Earlier versions of this repository saved only the latest deployed and verified state. The new event journal starts collecting events **only after it is installed**. Past events are not automatically reconstructed. If you already completed the failure-and-rollback lab, use your saved Terminal output and `.lab/evidence/production-before-rollback.log` to fill in the older sequence manually. For a newly observed full timeline, repeat the local exercise using the updated scripts. Do not manufacture `events.jsonl` entries to make a Record appear complete.
