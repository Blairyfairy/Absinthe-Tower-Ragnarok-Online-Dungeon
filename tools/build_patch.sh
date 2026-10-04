#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/build_rgz.py"
( cd "$ROOT" && find client/data client/lua -type f -print0 | sort -z | xargs -0 sha256sum > client/patch/SHA256SUMS.txt )
# Optional Thor/GRF workflow: point your Thor/GRF tooling at client/data and client/lua.
# Do not commit proprietary patcher binaries or the resulting .thor/.grf files.
echo "Patch assets and checksums are ready under client/patch/"
