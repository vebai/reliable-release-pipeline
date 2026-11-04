# First-time setup — using this repository without prior command-line experience

This guide is written for a reader who has **never run a CI/CD lab**. You need a Mac or a Linux computer, an internet connection to download tools/images, and permission to install software. You do **not** need AWS credentials or a GitHub account for the local exercise.

## 1. Understand what you downloaded

The downloaded file, `reliable-release-pipeline.zip`, is a **ZIP archive** (a compressed folder). After you extract/unzip it, you should have a folder called `reliable-release-pipeline`. This is the **repository**: a normal folder containing the application, its tests, scripts, and instructions. It is not yet a public GitHub project.

On a Mac, open **Finder → Downloads**, then double-click the ZIP. On Linux, extract it with your file manager or a ZIP utility. **Keep the extracted folder together:** moving only the scripts will break the relative file paths they use.

If you previously started the exercise in a folder with the same name, **continue in that existing folder**. Do not delete or overwrite its `.lab/` directory; it holds the results and identifiers created by earlier lab commands. You can replace the Markdown documentation separately when receiving an updated release.

## 2. Open a terminal

A **terminal** is a window in which you type commands and read their output. On macOS, open **Applications → Utilities → Terminal**, or use Spotlight to search for **Terminal**. On Ubuntu, open **Terminal** from the applications menu.

A line such as `MacBookPro:~ vebai$` or `%` is a **prompt**: it tells you the terminal is ready. **Do not type the prompt**; type only the command shown inside a code block, then press **Return/Enter**.

The default Mac terminal shell may be `zsh` or `bash`; the scripts work with either because they explicitly start Bash. A message suggesting `chsh -s /bin/zsh` is informational and not part of this lab.

## 3. Go into the correct folder

**Where to run:** your Mac/Linux terminal, not inside Docker or AWS.

If the folder is in your Mac or Linux Downloads directory, type:

```bash
cd ~/Downloads/reliable-release-pipeline
```

`cd` means **change directory** (open a folder from the terminal). The `~` means your home folder. You can check the result:

```bash
pwd
ls
```

`pwd` prints your current folder. `ls` lists files. You should see `README.md` plus the `app`, `docs`, `evidence` and `scripts` folders. If you see “No such file or directory”, locate the extracted folder in Finder/file manager and use its actual path. Do not continue while you are in the wrong folder.

**All commands in this repository's local lab assume you stay in this top-level folder.** If you close Terminal and open a new window later, use `cd` again.

## 4. Check the three tools

We have confirmed the scripts pass on a Mac with **Python 3.11.4**. The Docker image uses Python **3.13** internally; you do **not** need Python 3.13 installed on your Mac for this exercise. Python 3.11 or newer is recommended for the host; older versions are not part of the tested baseline.

Type these commands, one at a time:

```bash
python3 --version
git --version
docker --version
```

- **Python** runs the application tests and some verification scripts. If your Mac does not recognise `python3`, install a current supported Python 3 version from [python.org](https://www.python.org/downloads/) or your normal package manager.
- **Git** records changes to project files and is checked by the preflight script. You do not need to understand branches or remotes to run the local lab. On a Mac, `git --version` may prompt you to install Apple command-line tools; follow the on-screen instructions.
- **Docker** builds and runs the application in containers. On macOS, install and open **Docker Desktop** using the official [Docker Desktop for Mac instructions](https://docs.docker.com/desktop/setup/install/mac-install/). On Linux, follow the official [Docker Engine installation guide](https://docs.docker.com/engine/install/) for your distribution. **Installing a Docker command alone is not enough:** the Docker engine must also be running.

On Ubuntu or Debian Linux, Python and Git can usually be installed using:

```bash
sudo apt update
sudo apt install -y python3 git
```

On Fedora or another system that uses `dnf`, use:

```bash
sudo dnf install -y python3 git
```

For Docker on Linux, use the distribution-specific official instructions linked above, including the documented way to grant your account Docker access. Do not guess at installation steps or bypass an unexpected permission error. The local scripts expect Docker to work **without adding `sudo` before every command**.

## 5. Check that Docker is actually running

Open Docker Desktop on your Mac and check that the engine has started. Then type:

```bash
./scripts/preflight.sh
```

`./` means “run a file in the current folder”. The file `scripts/preflight.sh` checks the tools and Docker connection; it does not deploy the application. Successful output ends with:

```text
Preflight PASS
```

If you see “Docker daemon is not reachable” or “Cannot connect to the Docker daemon”, start Docker Desktop or check your Linux Docker service. See [Troubleshooting](troubleshooting.md). **Stop here until preflight passes.**

## 6. Run the checks before building anything

```bash
./scripts/validate-repo.sh
```

This runs **five application tests**, **four Release Evidence Record tests**, Python compilation and shell syntax checks. If an optional YAML parser is installed, it also checks the workflow files as YAML. The tests may print `HTTP 500` because one test **deliberately checks that an unhealthy application is detected**. That individual test is successful when it reports `ok`.

Successful overall output ends with:

```text
PASS - offline repository checks (Docker/GitHub/AWS untested in this environment)
```

This line means **the offline checks passed**. It does **not** mean you have already run a Docker deployment, GitHub workflow or AWS exercise.

## 7. Move on to the local lab

You are ready for [**Local lab: first release, failure and recovery**](local-lab.md). It tells you exactly what to type next and what each command establishes.

If you find a term you do not know, use this short glossary:

| Term | Plain-language meaning |
| --- | --- |
| **Script** | A small file containing commands so you do not have to type them individually |
| **Image** | The packaged application from a Docker build |
| **Container** | One running copy of an image |
| **Tag** | A readable label, such as `good-v1`; it is not the authoritative identity of a published release |
| **Image ID** | Docker's content identifier for a *local image*; the local lab compares these between containers |
| **Registry** | A service that stores packaged images for other machines to download (for example, GHCR or Amazon ECR) |
| **Registry digest** | The authoritative digest for the published registry image; used by the GitHub lab, not produced by `build-local.sh` |
| **Environment** | A place/configuration in which the app runs; in this local lab, staging and production are both containers on **your own computer** |
| **Verify** | Check the running application and its identity rather than assuming deployment worked |
| **Rollback** | Restore an earlier release **only after** confirming that doing so is safe |
| **Evidence Record** | A retained document of the source, checks, identity, deployment, verification and recovery decisions |

**Safe practice:** If a command fails, read the first meaningful error, check prerequisites and stop at that stage. Do not skip a failed verification to continue to promotion.
