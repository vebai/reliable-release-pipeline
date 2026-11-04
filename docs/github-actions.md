# Optional GitHub Actions lab — build once, promote by **registry digest**

This guide is for readers who have already completed the [local lab](local-lab.md) or understand its release decisions and want to see a **published image** used across environments. It does **not** create an AWS service or a permanent production deployment.

**GitHub Actions** is a service that runs commands automatically on machines called **runners**. **GitHub Container Registry (GHCR)** stores Docker images. A **registry manifest digest** (`sha256:...`) identifies the exact published image that those runners download. It is different from the local Docker image ID in the first exercise.

## Prerequisites — do not assume these are already configured

1. A GitHub account that can create repositories and run Actions.
2. The project published to a repository's **main branch** following [Publish to GitHub](publish-to-github.md).
3. Repository permission to run GitHub Actions and publish packages using the workflow's **`GITHUB_TOKEN`** with `packages: write` (the workflow requests that permission). Check organisation and repository policies if applicable.
4. A GitHub environment named exactly **`lab-production`**. If you intend an actual **reviewed promotion**, you must configure **required reviewers** and confirm the rules are available and effective on your repository/account. Merely naming an environment in YAML does **not** enforce approval. If your account cannot enforce reviewers, the workflow can still illustrate digest continuity, but do **not** claim that it proved an enforced human approval.
5. Review GitHub Actions and GHCR usage/storage limits and possible charges before triggering a cloud-hosted job. The release workflow is **manual**; it does not publish automatically on every push.

### Create the GitHub environment in the browser

**Where:** your repository on github.com, not Terminal. Open **Settings → Environments** (the exact labels may vary as GitHub evolves). Create `lab-production`, then configure the required reviewer rule if supported. Review who is allowed to approve and whether your account's rules prevent self-approval. Confirm the protection rule actually applies to the `production` workflow job **before claiming a real approval boundary**.

### Inspect the workflow files

- [`.github/workflows/ci.yml`](../.github/workflows/ci.yml): runs tests and builds a **disposable** image on pull requests and main-branch pushes. That image is a validation candidate, **not** a releasable published image.
- [`.github/workflows/release.yml`](../.github/workflows/release.yml): manually triggered. Runs tests; builds and pushes **one** image to GHCR; captures its registry digest; pulls **the same digest** into staging and production **lab runners**; verifies the running application and writes a release record.

The Shop API is small on purpose. The workflows do **not** implement full security scanning, SBOM generation, signatures, production traffic, a 5% canary, an AWS IAM/OIDC role or rollback within GitHub Actions. The **local lab** demonstrates rollback separately.

## Run the CI workflow first

**Where:** your GitHub repository's **Actions** tab. Find `CI - PROVE (validation only)` and open the run for the commit you just pushed. The run should show passing unit tests, evidence tests, shell syntax, container build and HTTP smoke test. **If it fails, do not immediately try the release workflow.** Open the failed job, locate the first meaningful error, identify whether it concerns code, permissions, runner or network, and correct the underlying cause.

## Run the manual release workflow

After the CI checks pass, open **Actions → Release lab - build once, promote by registry digest → Run workflow**. Choose **main**. The workflow intentionally runs only on that branch.

Follow these jobs in sequence:

| Job | What actually happens | What to verify |
| --- | --- | --- |
| `prove` | Runs application and evidence tests | Checks pass; failures stop progression |
| `package` | Builds and pushes **one image** to GHCR | A complete `ghcr.io/.../shop-api@sha256:...` registry reference is produced |
| `staging` | Runs that published image on a temporary GitHub runner | `/health`, `/version` and `/products` pass; source revision matches |
| `production` | Runs that **same digest** on another temporary runner | Required reviewer decision **only if configured and enforced**, then the same checks pass |

These runners disappear when their jobs finish. They are not persistent staging and production servers. The name **production** means only a controlled *lab workflow environment*, not a real customer service.

## Inspect the Release Evidence Record

In the completed workflow run, open **Artifacts** and download `release-record-final`. Extract the downloaded archive and read `release-evidence.md` using a text editor. Check the **full source commit**, published **registry manifest digest**, staging verification and production verification. The digest in the staging and production jobs must be identical.

If the environment did not enforce a reviewer, record the actual outcome rather than claiming a human approval. The record explicitly distinguishes implemented checks from omitted security and operational controls. Compare it with [the book's blank Record template](../evidence/release-evidence-template.md).

## Common failures and safe stopping points

- **No workflow appears:** check that the files are present on `main` and Actions is enabled for this repository.
- **Package push denied:** inspect workflow `packages: write`, repository package policies and whether GHCR accepts the current account/token. Never paste a secret into the repository to get past this error.
- **GHCR pull denied:** check package visibility, access control and the runner job's `packages: read` permission. A public source repository does **not** guarantee a public image package.
- **Production runs without an approval prompt:** the environment rule is not working as an approval gate. Stop treating this as evidence of reviewer approval; configure and test protection separately.
- **Version or health verification fails:** do not report the release as verified. Inspect the first meaningful error and capture the result in the Record.

**Next:** The [architecture](architecture.md) explains exactly which book concepts this demonstration covers; [AWS mapping](aws-mapping.md) explains which AWS capabilities are only conceptual and are **not** deployed here.
