#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"
require python3
require git
python3 --version
if ! command -v docker >/dev/null 2>&1; then
  echo 'Docker not found. Unit tests can run, but the container lab cannot.'
  exit 2
fi
if ! docker info >/dev/null 2>&1; then
  echo 'Docker command exists, but the Docker daemon is not reachable.' >&2
  exit 2
fi
docker version --format 'Docker server {{.Server.Version}}'
echo 'Preflight PASS'
