#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
LAB_DIR="${ROOT_DIR}/.lab"
STATE_DIR="${LAB_DIR}/state"
mkdir -p "$STATE_DIR"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Required command missing: $1"; }
check_env() { [[ "${1:-}" == staging || "${1:-}" == production ]] || fail 'Environment must be staging or production'; }
check_image_id() { [[ "${1:-}" =~ ^sha256:[0-9a-f]{64}$ ]] || fail 'Pass a complete local image ID sha256:<64 hex>, not a tag'; }
port_for() { case "$1" in staging) echo 8081;; production) echo 8082;; esac; }
container_for() { printf 'rrp-%s' "$1"; }

image_version() {
  docker image inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' "$1"
}

write_state() {
  local file="$1" image_id="$2" version="$3"
  printf '%s\n%s\n' "$image_id" "$version" > "$file"
}

read_state_image() { [[ -f "$1" ]] && sed -n '1p' "$1" || true; }
read_state_version() { [[ -f "$1" ]] && sed -n '2p' "$1" || true; }
