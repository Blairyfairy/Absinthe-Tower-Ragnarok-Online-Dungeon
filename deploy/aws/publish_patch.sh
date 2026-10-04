#!/usr/bin/env bash
set -euo pipefail
: "${PATCH_BUCKET:?Set PATCH_BUCKET, e.g. s3://my-ro-patches}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$ROOT/tools/build_patch.sh"
aws s3 sync "$ROOT/client/patch" "$PATCH_BUCKET/absinthero/0.2.0/" --exclude '*.md'
echo "Published patch to $PATCH_BUCKET/absinthero/0.2.0/"
