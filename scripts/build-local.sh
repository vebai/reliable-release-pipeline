#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"
require docker
require python3
REVISION="${1:-}"
if [[ -z "$REVISION" ]]; then
  REVISION="$(git -C "$ROOT_DIR" rev-parse --short=12 HEAD 2>/dev/null || echo local-lab)"
fi
[[ "$REVISION" =~ ^[a-zA-Z0-9._-]+$ ]] || fail 'Revision must contain only letters, digits, dot, underscore or hyphen'
TAG="reliable-shop:${REVISION}"
docker build --file "$ROOT_DIR/app/Dockerfile" --build-arg "SOURCE_REVISION=$REVISION" --tag "$TAG" "$ROOT_DIR/app"
IMAGE_ID="$(docker image inspect --format '{{.Id}}' "$TAG")"
check_image_id "$IMAGE_ID"
image_version "$IMAGE_ID" | grep -Fx -- "$REVISION" >/dev/null || fail 'Image version label mismatch'
printf '\nSOURCE_REVISION=%s\nLOCAL_IMAGE_ID=%s\n' "$REVISION" "$IMAGE_ID"
printf '%s\n%s\n' "$IMAGE_ID" "$REVISION" > "$STATE_DIR/last-built"
python3 "$ROOT_DIR/scripts/journal_local.py" BUILD local "$IMAGE_ID" "$REVISION" BUILT
echo 'IMPORTANT: LOCAL_IMAGE_ID is a Docker image ID, not a remote registry manifest digest.'
