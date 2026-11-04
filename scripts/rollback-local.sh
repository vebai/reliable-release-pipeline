#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"
ENVIRONMENT="${1:-}"
check_env "$ENVIRONMENT"
[[ "${2:-}" == '--compatible' ]] || fail 'Explicit --compatible is required after checking recovery compatibility'
require docker
require python3
PREVIOUS="$STATE_DIR/$ENVIRONMENT.previous-verified"
[[ -f "$PREVIOUS" ]] || fail 'No previously verified release is recorded for this environment'
IMAGE_ID="$(read_state_image "$PREVIOUS")"
VERSION="$(read_state_version "$PREVIOUS")"
check_image_id "$IMAGE_ID"
docker image inspect "$IMAGE_ID" >/dev/null || fail 'Previously verified artefact is no longer available'
[[ "$(image_version "$IMAGE_ID")" == "$VERSION" ]] || fail 'Previous image metadata has changed'
python3 "$ROOT_DIR/scripts/journal_local.py" RECOVER "$ENVIRONMENT" "$IMAGE_ID" "$VERSION" STARTED --note compatibility-acknowledged
NAME="$(container_for "$ENVIRONMENT")"
mkdir -p "$LAB_DIR/evidence"
if docker container inspect "$NAME" >/dev/null 2>&1; then
  LOG_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
  LOG_ARCHIVE="$LAB_DIR/evidence/${ENVIRONMENT}-before-rollback-${LOG_STAMP}-$$.log"
  docker logs "$NAME" > "$LOG_ARCHIVE" 2>&1 || true
  cp "$LOG_ARCHIVE" "$LAB_DIR/evidence/${ENVIRONMENT}-before-rollback.log"
  docker rm -f "$NAME" >/dev/null
fi
PORT="$(port_for "$ENVIRONMENT")"
docker run -d --name "$NAME" --publish "127.0.0.1:${PORT}:8000" \
  --env "ENVIRONMENT=$ENVIRONMENT" "$IMAGE_ID" >/dev/null
write_state "$STATE_DIR/$ENVIRONMENT.current" "$IMAGE_ID" "$VERSION"
rm -f "$STATE_DIR/$ENVIRONMENT.verified"
echo 'Recovery state changed; verifying known-good candidate...'
if "$ROOT_DIR/scripts/verify-release.sh" "$ENVIRONMENT" "$IMAGE_ID"; then
  python3 "$ROOT_DIR/scripts/journal_local.py" RECOVER "$ENVIRONMENT" "$IMAGE_ID" "$VERSION" VERIFIED --note known-good-verified
  printf 'ROLLBACK VERIFIED: environment=%s image_id=%s source=%s\n' "$ENVIRONMENT" "$IMAGE_ID" "$VERSION"
else
  python3 "$ROOT_DIR/scripts/journal_local.py" RECOVER "$ENVIRONMENT" "$IMAGE_ID" "$VERSION" FAILED
  fail 'Recovery could not be verified; stop and investigate'
fi
