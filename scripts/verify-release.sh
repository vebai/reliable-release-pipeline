#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"
ENVIRONMENT="${1:-}"
IMAGE_ID="${2:-}"
check_env "$ENVIRONMENT"
check_image_id "$IMAGE_ID"
require docker
require python3
NAME="$(container_for "$ENVIRONMENT")"
RUNNING_IMAGE="$(docker container inspect --format '{{.Image}}' "$NAME" 2>/dev/null || true)"
[[ "$RUNNING_IMAGE" == "$IMAGE_ID" ]] || fail 'Running container image ID does not match the expected ID'
CURRENT="$(read_state_image "$STATE_DIR/$ENVIRONMENT.current")"
[[ "$CURRENT" == "$IMAGE_ID" ]] || fail 'Candidate state does not match the expected image ID'
VERSION="$(image_version "$IMAGE_ID")"
PORT="$(port_for "$ENVIRONMENT")"
if python3 "$ROOT_DIR/scripts/verify_http.py" "http://127.0.0.1:$PORT" "$VERSION" "$ENVIRONMENT"; then
  write_state "$STATE_DIR/$ENVIRONMENT.verified" "$IMAGE_ID" "$VERSION"
  python3 "$ROOT_DIR/scripts/journal_local.py" VERIFY "$ENVIRONMENT" "$IMAGE_ID" "$VERSION" PASS
  printf 'VERIFIED: %s %s %s\n' "$ENVIRONMENT" "$VERSION" "$IMAGE_ID"
else
  python3 "$ROOT_DIR/scripts/journal_local.py" VERIFY "$ENVIRONMENT" "$IMAGE_ID" "$VERSION" FAIL --note http-check-failed
  fail 'Deployment was not verified; inspect logs and assess recovery before continuing'
fi
