#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"
require docker
for env in staging production; do
  NAME="$(container_for "$env")"
  if docker container inspect "$NAME" >/dev/null 2>&1; then docker rm -f "$NAME" >/dev/null; fi
done
echo 'Lab containers removed. Local image IDs and .lab evidence remain for inspection.'
