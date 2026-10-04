# Absinthe Tower deployment runbook

## 1. Preflight

This package targets current rAthena-style YAML/import databases. rAthena's current item database is YAML-based and its import mechanism is designed for `db/import`; scripts are loaded through an NPC `.conf` import. citeturn1search1turn0search5

The original supplied dungeon uses `quiz_01`, so the base package does **not** require a new map cache. The map flags remain in the original script.

Before deployment:

```bash
python3 tools/validate_ids.py --rathena /opt/rathena
python3 tools/lint_absinthe.py
```

Verify custom IDs `32100-32108` are unused. If any collide, change them in **all** server/client files before deployment.

## 2. Server files

Copy:

```text
server/npc/absinthe_tower.txt -> <rAthena>/npc/custom/absinthero/absinthe_tower.txt
server/db/import/item_db.yml -> <rAthena>/db/import/item_db.yml
server/db/import/item_group_db.yml -> <rAthena>/db/import/item_group_db.yml
server/db/import/map_drops.yml -> <rAthena>/db/import/map_drops.yml
```

Add this to a loaded NPC configuration:

```text
import: npc/custom/absinthero/absinthe_tower.txt
```

Do not blindly replace a site's existing `scripts_custom.conf`; merge the one import line into the site's own custom config.

## 3. Reload

rAthena documents `@reloadscript`, `@loadnpc`, and `@unloadnpc` as script-management approaches; a full map-server restart remains the safest option for major changes. citeturn0search5

For this package:

```text
@reloadscript
@reloaditemdb
```

If your exact rAthena revision does not reload item groups correctly, restart map-server during a maintenance window.

Test:

```text
@iteminfo 32100
@iteminfo 32103
@iteminfo 32104
@iteminfo 32108
@mobinfo 1002
```

## 4. Client patch

Build the patch:

```bash
./tools/build_patch.sh
```

This creates an RGZ patch plus SHA256 checksums. RGZ is a Ragnarok patch archive format capable of carrying updated BGM and other client files. citeturn10view0

For Thor:

1. Use `client/data` as the patch source.
2. Generate the `.thor` with the Thor/GRF tooling appropriate to your patcher version.
3. Publish it to the patcher's update directory.
4. Increment your patch/version manifest.
5. Test on a clean client before production.

For GRF:

1. Create a `data/` directory containing the client assets.
2. Merge it into a dedicated server GRF.
3. Put that GRF first in `DATA.INI` if your client supports multiple GRFs.
4. Keep the official GRFs below it so the server GRF overrides custom assets. rAthena's GRF documentation describes this workflow. citeturn0search1turn6search5

For modern clients, custom item metadata lives in `System/ItemInfo.lub`/its source form; older clients use the `idnum2item*` tables. citeturn5search0

## 5. AWS + Aurora MySQL

A reliable architecture should treat the dungeon controller as stateful. The original design has a global one-run lock, so **do not horizontally run two active map-server copies against the same logical dungeon state** without changing the controller to a database-backed/instance-backed lock. Aurora can provide durable SQL storage, but it does not make rAthena's process-local globals distributed.

Recommended topology:

```text
Players
   |
Patch/CDN (S3 + CloudFront or Thor host)
   |
Login -> Char -> Map Server (active dungeon owner)
                     |
                     +---- Aurora MySQL-compatible cluster
                     |
                     +---- CloudWatch/log shipping
```

Use Aurora Multi-AZ/managed backups and keep credentials in AWS Secrets Manager or SSM Parameter Store. Do not commit database passwords.

Example connectivity preflight:

```bash
mysql --host="$AURORA_HOST" --port="3306" \
  --user="$AURORA_USER" --password \
  --ssl-mode=REQUIRED "$AURORA_DATABASE" < deploy/aws/aurora_preflight.sql
```

The dungeon's custom YAML item definitions do not require an Aurora migration in a standard current rAthena YAML database setup. If your fork uses SQL `item_db`/`mob_db`, use the schema supplied by **that exact fork** and port the item definitions after checking for ID collisions.

## 6. Upload commands

Server staging:

```bash
export RO_HOST='map.example.com'
export RO_USER='deploy'
export ROATHENA_ROOT='/srv/rathena'
./deploy/aws/deploy_server.sh
```

Patch publishing:

```bash
export PATCH_BUCKET='s3://your-private-or-public-patch-bucket'
./deploy/aws/publish_patch.sh
```

For a direct object upload:

```bash
aws s3 cp client/patch/absinthero_0.2.0.rgz \
  "$PATCH_BUCKET/absinthero/0.2.0/absinthero_0.2.0.rgz"
```

## 7. Rollout order

1. Back up server configuration and database.
2. Validate item IDs and mob IDs.
3. Deploy server script/database imports.
4. Reload or restart map-server.
5. Deploy client patch to a test channel/bucket.
6. Test a clean client.
7. Run floors 1-3, a floor 3 mini-boss, floor 5 bonus MVP, floor 10 main MVP, and floor 100.
8. Verify Mini Boss Card Album and MVP Card Album open correctly.
9. Verify the existing Old Card Album still works normally.
10. Verify timeout, party wipe/cleanup, and final victory cleanup.
11. Promote the patch.

## 8. Rollback

Server rollback:

```bash
rsync -av /path/to/backup/absinthero/ "$RO_USER@$RO_HOST:$ROATHENA_ROOT/npc/custom/absinthero/"
```

Then reload/restart map-server.

Client rollback: remove the Absinthe Tower patch from the patch manifest or publish the previous known-good patch version. Never delete the official base GRF.
