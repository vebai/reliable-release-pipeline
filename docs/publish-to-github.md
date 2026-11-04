# Publish this companion repository to GitHub (after local validation)

You do **not** need GitHub for the local Docker exercise. This is an **optional later step** so readers can examine the files and run the automated GitHub lab. Do not publish the repository until you have reviewed its contents and are happy with the validation evidence.

**Example intended destination:** `https://github.com/vebai/reliable-release-pipeline`. That URL is **not proof** that the repository has been created. You must create it and verify the contents online.

## 1. Know what is being published

A **Git repository** is a folder with a tracked change history. **GitHub** is a website that stores and shares that history. The ZIP alone is not yet a GitHub repository.

**Keep these in the public repository:** `scripts/` (all test, build, verification and recovery scripts), `app/` including tests and Dockerfile, `tests/`, `.github/workflows/`, `docs/`, `evidence/`, `README.md`, `.gitignore`, and `VALIDATION_REPORT.md`. These are the reusable learning materials; **do not delete them after validation**.

**Do not publish:** the `.lab/` folder, Docker images or image archives, Python caches, temporary test logs, secrets, credentials or personal machine configuration. `.gitignore` excludes the normal generated files. A `.gitignore` entry does not erase an item that was deliberately committed previously: always review the staged file list before making a commit.

## 2. Create an empty public repository on GitHub

Sign in to [github.com](https://github.com/) using your own account. Create a **new repository** named `reliable-release-pipeline` and select **Public**. For a first upload from this folder, leave GitHub's “Add README”, “Add .gitignore” and “Choose a licence” options **unselected** so the online repository starts empty. If you choose another account or repository name, replace the example `vebai` values in later commands with the actual destination.

A **public** repository allows readers to view the source code. It does **not** necessarily make a separately published container image public: GHCR has its own package visibility and access settings.

## 3. Open Terminal in the project folder

**Where to run:** Mac Terminal or a Linux terminal, **not** GitHub's website and not inside Docker.

```bash
cd ~/Downloads/reliable-release-pipeline
pwd
ls
./scripts/validate-repo.sh
```

If your extracted folder is elsewhere, change the path. The test command confirms the offline checks are still working; it does not deploy the application.

## 4. Create local Git history

Type these commands **one at a time**:

```bash
git init -b main
git add .
git status --short
```

- `git init -b main` creates local history with a branch named **main** (the default publishing branch).
- `git add .` prepares files for the first commit. It should respect `.gitignore`.
- `git status --short` displays the exact files waiting to be committed. **Inspect this list carefully before continuing.** It should contain the repository's source and documentation, **not** `.lab/`, credential files, Python caches or Docker image archives.

If Git asks you to set an author name and email for the commit, configure your own values (you choose what to disclose publicly). For example, scoped **only to this repository**:

```bash
git config user.name "Your chosen author name"
git config user.email "your-github-associated-email@example.com"
```

Replace those placeholders with your real intended details. GitHub also supports a privacy-preserving `noreply` email address in account settings.

When the staged list looks correct:

```bash
git commit -m "Add Reliable Release Pipeline companion lab"
```

If the command says there is nothing to commit, check whether you are already in a Git repository and whether a commit already exists. **Do not delete `.git` to retry.**

## 5. Connect the local folder to your new GitHub repository

```bash
git remote add origin https://github.com/vebai/reliable-release-pipeline.git
git push -u origin main
```

`origin` is simply Git's name for the remote GitHub repository. `push` sends your new commit to GitHub. You must have permission to push to that destination and a working GitHub authentication method, such as an installed credential manager or configured SSH credentials. GitHub account passwords are not a substitute for supported Git authentication; **never put tokens or passwords inside source files or commit them**.

If `origin` already exists, inspect it rather than adding it twice:

```bash
git remote -v
```

Do not push to an unexpected repository. If authentication fails, check your account access and the official GitHub authentication instructions before retrying.

## 6. Verify the actual published result

Open `https://github.com/vebai/reliable-release-pipeline` in a browser. Confirm that the **main** branch contains the README, all scripts, application code, tests, evidence and guides, and that `.lab/` and secrets are absent. Do not put a repository URL in the book until this succeeds.

The Actions tab should show the `CI - PROVE (validation only)` workflow for the `main` push. Check that it **actually passes**; a workflow appearing in the repository is not evidence that it runs successfully.

Next, read [**GitHub Actions lab setup**](github-actions.md) and configure the `lab-production` environment and GHCR permissions **before** starting the manual release workflow. Capture the real registry digest from its `release-record-final` artefact after it runs.

## Common stopping points

- **`Permission denied` or authentication failure on push:** do not paste credentials into files. Check repository ownership and Git authentication.
- **Git reports `remote origin already exists`:** inspect `git remote -v`; do not overwrite a working remote without checking.
- **Protected branch or permission rejection:** follow the actual repository's review and authorisation policy; do not bypass it.
- **Unwanted files shown by `git status --short`:** stop and correct the staged content before committing. The aim is a clean, reproducible public repository, not a copy of your local lab state.
