#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"
ENVIRONMENT="${1:-}"
IMAGE_ID="${2:-}"
check_env "$ENVIRONMENT"
check_image_id "$IMAGE_ID"
require docker
require python3
docker image inspect "$IMAGE_ID" >/dev/null || fail 'Requested image is unavailable locally'
VERSION="$(image_version "$IMAGE_ID")"
[[ -n "$VERSION" && "$VERSION" != '<no value>' ]] || fail 'Image is missing source revision metadata'
if [[ "$ENVIRONMENT" == production ]]; then
  [[ "${3:-}" == '--approve' ]] || fail 'Production lab promotion requires explicit --approve'
  STAGED="$(read_state_image "$STATE_DIR/staging.verified")"
  [[ "$STAGED" == "$IMAGE_ID" ]] || fail 'Production blocked: same image ID has not passed staging verification'
fi
NAME="$(container_for "$ENVIRONMENT")"
PORT="$(port_for "$ENVIRONMENT")"
CURRENT="$(read_state_image "$STATE_DIR/$ENVIRONMENT.verified")"
LIVE_ID="$(docker container inspect --format '{{.Image}}' "$NAME" 2>/dev/null || true)"
if [[ -n "$CURRENT" && "$CURRENT" == "$LIVE_ID" && "$CURRENT" != "$IMAGE_ID" ]]; then
  cp "$STATE_DIR/$ENVIRONMENT.verified" "$STATE_DIR/$ENVIRONMENT.previous-verified"
fi
if docker container inspect "$NAME" >/dev/null 2>&1; then
  docker rm -f "$NAME" >/dev/null
fi
FAILURE_FLAG=0
if [[ "${3:-}" == '--simulate-broken' || "${4:-}" == '--simulate-broken' ]]; then
  FAILURE_FLAG=1
fi
docker run -d --name "$NAME" --publish "127.0.0.1:${PORT}:8000" \
  --env "ENVIRONMENT=$ENVIRONMENT" --env "SIMULATE_FAILURE=$FAILURE_FLAG" "$IMAGE_ID" >/dev/null
write_state "$STATE_DIR/$ENVIRONMENT.current" "$IMAGE_ID" "$VERSION"
rm -f "$STATE_DIR/$ENVIRONMENT.verified"
if [[ "$FAILURE_FLAG" == 1 ]]; then JOURNAL_NOTE=simulated-health-500; else JOURNAL_NOTE=normal; fi
python3 "$ROOT_DIR/scripts/journal_local.py" PROMOTE "$ENVIRONMENT" "$IMAGE_ID" "$VERSION" DEPLOYED_UNVERIFIED --note "$JOURNAL_NOTE"
printf 'PROMOTED (not yet verified): environment=%s image_id=%s source=%s http://127.0.0.1:%s\n' "$ENVIRONMENT" "$IMAGE_ID" "$VERSION" "$PORT"
echo 'NEXT: run scripts/verify-release.sh to accept or reject the deployed candidate.'
