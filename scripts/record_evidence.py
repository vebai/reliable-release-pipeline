"""Append a concise, auditable lab release record (not an attestation)."""
import argparse
import re
import datetime
from pathlib import Path


def write_new(out, source, image_ref, run_url):
    if not re.fullmatch(r"ghcr\.io/[a-z0-9_.-]+(?:/[a-z0-9_.-]+)+@sha256:[0-9a-f]{64}", image_ref):
        raise ValueError("A complete GHCR registry manifest digest is required")
    out.write_text(
        f"# Release Evidence Record — GitHub Actions lab\n\n"
        f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n\n"
        f"- **Source commit:** `{source}`\n"
        f"- **Pipeline run:** {run_url}\n"
        f"- **PROVE:** Unit tests passed in this release workflow.\n"
        f"- **Security/coverage gates:** Not implemented in this teaching repository; no PASS claim.\n"
        f"- **PACKAGE — registry artefact:** `{image_ref}`\n"
        f"- **Authority:** Registry manifest digest after push (not local image ID).\n"
        f"- **Environment configuration:** `ENVIRONMENT` is external; application version baked into the image.\n"
        f"- **Production approval:** Only enforced when GitHub's `lab-production` environment has required reviewers configured. Inspect its deployment approval audit trail.\n"
        f"- **Recovery readiness:** A previously verified, available and compatible digest must be established separately; not assumed.\n\n"
        f"## Chronological verification\n\n", encoding="utf-8")


def append_phase(out, phase, status, image_ref, environment):
    if not out.is_file():
        raise FileNotFoundError(f"Release record does not exist: {out}")
    current = out.read_text(encoding="utf-8")
    if f"**PACKAGE — registry artefact:** `{image_ref}`" not in current:
        raise ValueError("Record artefact identity differs from the image being verified")
    with out.open("a", encoding="utf-8") as stream:
        stream.write(f"- **{phase.upper()} — {status}:** `{environment}` ephemeral Actions runner; "
                     f"`/health`, `/version`, `/products` verified against `{image_ref}`. "
                     "This is a demonstration, not a persistent AWS or production deployment.\n")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    initial = sub.add_parser("start")
    initial.add_argument("--output", required=True)
    initial.add_argument("--source", required=True)
    initial.add_argument("--image-ref", required=True)
    initial.add_argument("--run-url", required=True)
    phase = sub.add_parser("phase")
    phase.add_argument("--output", required=True)
    phase.add_argument("--phase", choices=("staging", "production"), required=True)
    phase.add_argument("--image-ref", required=True)
    phase.add_argument("--status", choices=("PASS",), required=True)
    args = parser.parse_args()
    if args.command == "start":
        write_new(Path(args.output), args.source, args.image_ref, args.run_url)
    else:
        append_phase(Path(args.output), args.phase, args.status, args.image_ref, args.phase)


if __name__ == "__main__":
    main()
