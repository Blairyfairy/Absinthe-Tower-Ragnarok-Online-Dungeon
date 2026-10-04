#!/usr/bin/env bash
set -euo pipefail
: "${RO_HOST:?Set RO_HOST}"
: "${RO_USER:?Set RO_USER}"
: "${ROATHENA_ROOT:?Set ROATHENA_ROOT}"
: "${RO_GM_COMMAND:?Set RO_GM_COMMAND to your approved GM/admin command transport}"

# rAthena supports @reloadscript and @reloaditemdb. How you deliver an @ command
# depends on your console/GM setup; this script deliberately does not hard-code
# credentials or an unsafe remote console protocol.
echo "On the authorized server console/GM client, run:"
echo "  @reloadscript"
echo "  @reloaditemdb"
echo "If item-group parsing does not reload cleanly on your build, restart map-server."
