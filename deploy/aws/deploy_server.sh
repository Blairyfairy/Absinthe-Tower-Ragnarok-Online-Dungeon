#!/usr/bin/env bash
set -euo pipefail
: "${RO_HOST:?Set RO_HOST to the map-server host}"
: "${RO_USER:?Set RO_USER to the deploy SSH user}"
: "${ROATHENA_ROOT:?Set ROATHENA_ROOT to the rAthena checkout path}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REMOTE="$RO_USER@$RO_HOST"

# Stage files without touching unrelated server content.
rsync -av --delete-after "$ROOT/server/npc/" "$REMOTE:$ROATHENA_ROOT/npc/custom/absinthero/"
rsync -av "$ROOT/server/db/import/" "$REMOTE:$ROATHENA_ROOT/db/import/"
rsync -av "$ROOT/server/npc/load_absinthero.conf" "$REMOTE:$ROATHENA_ROOT/npc/scripts_custom_absinthero.conf"

# IMPORTANT: only enable this line after reviewing the import path and your local conf layout.
# ssh "$REMOTE" "printf '%s\\n' 'import: npc/custom/absinthero/absinthe_tower.txt' >> '$ROATHENA_ROOT/npc/scripts_custom.conf'"

echo "Files staged. Run the reload checklist in docs/DEPLOYMENT.md."
