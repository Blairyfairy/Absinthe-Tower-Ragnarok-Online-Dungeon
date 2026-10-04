# Absinthe Tower — Blair Page

**A complete 100-floor Endless-Tower-style dungeon expansion package for a private Ragnarok Online server.**

Author/project attribution in this package: **Blair Page / Absinthe Tower project**.

The starting point is the supplied Absinthe Tower source: a 100-floor crawl with an Absinthe Fairy entrance/token shop, a hidden controller, Mini Boss/MVP Card Albums, an existing-map deployment model, and runtime ID validation. fileciteturn0file0L1-L14

## What is included

```text
absinthero/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── docs/
│   ├── DESIGN.md
│   ├── DEPLOYMENT.md
│   └── EATHENA_COMPAT.md
├── source/
│   └── absinthe_tower_original.txt
├── server/
│   ├── npc/
│   │   ├── absinthe_tower.txt
│   │   └── load_absinthero.conf
│   ├── db/import/
│   │   ├── item_db.yml
│   │   ├── item_group_db.yml
│   │   └── map_drops.yml
│   ├── db/const_abt.txt
│   ├── legacy/item_db2.txt
│   └── scripts/reload_absinthe.txt
├── client/
│   ├── data/BGM/
│   │   ├── absinthe_t1.mid
│   │   ├── absinthe_t2.mid
│   │   ├── absinthe_t3.mid
│   │   ├── absinthe_boss.mid
│   │   └── absinthe_victory.mid
│   ├── data/idnum2itemdisplaynametable.txt
│   ├── data/idnum2itemdesctable.txt
│   ├── data/idnum2itemresnametable.txt
│   ├── data/itemslotcounttable.txt
│   ├── lua/ItemInfo_AbsintheTower.lua
│   └── README.md
├── source_art/
│   ├── *.png
│   └── *.bmp
├── deploy/aws/
│   ├── deploy_server.sh
│   ├── publish_patch.sh
│   ├── reload_mapserver.sh
│   ├── aurora.env.example
│   └── aurora_preflight.sql
├── tools/
│   ├── build_patch.sh
│   ├── build_rgz.py
│   ├── lint_absinthe.py
│   └── validate_ids.py
└── tests/
```

## Dungeon design

The supplied design is preserved: 100 floors; floors ending in 5 get a bonus MVP; floors ending in 10 get a main MVP; floor 100 gets three finale bosses; and every third floor gets a Gilded mini boss. The supplied NPC text also describes Philosopher's Stone Fragments, elemental stones, Old Card Albums, Mini Boss/MVP Card Albums, tokens, EXP and milestone rewards. fileciteturn0file0L104-L113

### Drop progression

The package adds:

- **Old Card Album (OCA)** — existing server item 616.
- **Absinthe Mini Boss Card Album** — custom 32103; dynamically rolls a card from the configured Gilded mini-boss pool.
- **Absinthe MVP Card Album** — custom 32104; dynamically rolls a card from the configured MVP/bonus/finale pools.
- **Philosopher's Stone Fragment** — 32105.
- **Philosopher's Stone** — 32106.
- **Sage's Stone Cache** — 32107; guaranteed fragments plus a weighted random bonus.
- **Alchemical Reliquary** — 32108; weighted random dungeon rewards.

The supplied source already multiplies supplemental dungeon drops by floor depth, glass reward strength, and server card rate. fileciteturn0file0L336-L383 The expanded script keeps that model and selects the normal/boss/MVP card-rate tier where available.

Current rAthena exposes separate common/boss/MVP and card/boss/MVP rate controls, so the package's card scaling is designed to follow the server's configured card-rate policy instead of replacing the server's normal card-drop system. citeturn0search8

## Why the monsters do not need new sprites

The dungeon deliberately uses the same monster IDs as normal rAthena mobs. It spawns those IDs with dungeon-only display names such as `Transmuted <Mob>` and `Gilded <Mob>`. This means the monsters retain their existing AI, stats source and sprites unless the server owner chooses to add a separate visual layer.

The supplied source itself performs runtime validation and skips unknown IDs, and explicitly recommends validating the IDs after rAthena updates. fileciteturn0file0L11-L14

## Current rAthena database model

Current rAthena documents `db/import` customization and the current YAML item database. citeturn6search10turn1search1 Item groups support weighted random selection, including `Random` subgroups and the `groupranditem`/`getrandgroupitem`/`getgroupitem` commands. citeturn8view0

The primary dungeon path uses script-based random caches so the core dungeon does not depend on an item-group implementation being present. The supplied `item_group_db.yml` is included as an optional modern data-driven extension.

## Install — server

### 1. Copy files

```bash
cp server/npc/absinthe_tower.txt /path/to/rathena/npc/custom/absinthero/
cp server/db/import/item_db.yml /path/to/rathena/db/import/
cp server/db/import/item_group_db.yml /path/to/rathena/db/import/
cp server/db/import/map_drops.yml.example /path/to/rathena/db/import/map_drops.yml  # optional; it intentionally adds no drops
```

### 2. Enable the script

Add this line to a loaded custom NPC configuration:

```text
import: npc/custom/absinthero/absinthe_tower.txt
```

rAthena's script-loading documentation uses `.conf` imports and notes that scripts must be activated by a configuration file. citeturn0search5

### 3. Check IDs

```bash
python3 tools/validate_ids.py --rathena /path/to/rathena
python3 tools/lint_absinthe.py
```

**Important:** verify that 32100–32108 are free on the target server. The package cannot know what another private server has already added.

### 4. Reload

On an authorized GM/admin session:

```text
@reloadscript
@reloaditemdb
```

For a production rollout, a map-server restart is the safest path if your exact rAthena revision does not reload every dependent item-group/script structure cleanly. rAthena documents `@reloadscript`, `@loadnpc`, and `@unloadnpc` for script changes. citeturn0search5

## Install — client

### Modern clients

Merge `client/lua/ItemInfo_AbsintheTower.lua` into the client's ItemInfo source and compile it to the appropriate `.lub` format when required.

### Older clients

Merge the `client/data/idnum2item*.txt` fragments into the existing client tables.

rAthena's current customization guidance distinguishes newer clients using `System/ItemInfo.lub` from older clients using the `idnum2item*` tables. citeturn5search0

### Item art

`source_art/` contains original PNG/BMP source artwork for the custom items. Ragnarok client generations that require `.spr/.act` binaries need those resources converted with a tool appropriate to the exact client build. There is no single universal `.spr/.act` pair that can safely be substituted across all client generations.

The client folder layout is documented by rAthena under `data/sprite` and `data/texture`. citeturn6search0

## Music patch

The server script now uses:

```text
BGM/absinthe_t1.mid
BGM/absinthe_t2.mid
BGM/absinthe_t3.mid
BGM/absinthe_boss.mid
BGM/absinthe_victory.mid
```

These are original MIDI compositions generated for this package, not copied game music.

Build an RGZ patch:

```bash
./tools/build_patch.sh
```

The included builder follows the documented RGZ structure. RGZ is a Ragnarok client patch archive used for files such as background music. citeturn10view0

For GRF deployment, put the custom `data/` content in a dedicated server GRF and load it above the official GRFs. rAthena's GRF documentation describes building a GRF from a `data` directory and using it as an override. citeturn0search1

For Thor, use the generated client directory as the source for your Thor patch-generation tool. Thor supports delivering files directly into the player's client folders or GRFs. citeturn0search4

## AWS + Aurora deployment

### Recommended architecture

```text
                  +------------------+
Players -------->| Login/Char/Map    |
                  | rAthena services  |
                  +---------+--------+
                            |
                  +---------v---------+
                  | Aurora MySQL      |
                  | Multi-AZ / backup |
                  +-------------------+

Patch clients <--- S3/CloudFront or Thor patch host

Metrics/logs ---> CloudWatch / centralized logging
```

**Do not run multiple active copies of this exact dungeon controller without redesigning the global run lock.** The supplied implementation uses process-local globals such as `$@abt_run`, so Aurora does not magically make two map-server processes share that state. For reliable scaling, keep one active dungeon owner or refactor the lock/state into a shared instance/database service.

### Server upload

```bash
export RO_HOST='map.example.com'
export RO_USER='deploy'
export ROATHENA_ROOT='/srv/rathena'
./deploy/aws/deploy_server.sh
```

### Patch upload to S3

```bash
export PATCH_BUCKET='s3://your-patch-bucket'
./deploy/aws/publish_patch.sh
```

Or directly:

```bash
aws s3 cp client/patch/absinthero_0.2.0.rgz \
  "$PATCH_BUCKET/absinthero/0.2.0/absinthero_0.2.0.rgz"
```

### Aurora connectivity test

```bash
mysql --host="$AURORA_HOST" --port=3306 \
  --user="$AURORA_USER" --password --ssl-mode=REQUIRED \
  "$AURORA_DATABASE" < deploy/aws/aurora_preflight.sql
```

Do not store the Aurora password in Git. Use AWS Secrets Manager or SSM Parameter Store.

## Release procedure

1. Back up the server and database.
2. Run `tools/lint_absinthe.py`.
3. Run `tools/validate_ids.py` against the exact rAthena checkout.
4. Deploy server files.
5. Reload/restart map-server.
6. Build the client RGZ/Thor/GRF patch.
7. Test with a clean client.
8. Test floors 1–3.
9. Test a floor-3 Gilded mini boss.
10. Test floor 5 bonus MVP.
11. Test floor 10 main MVP.
12. Test a normal OCA, Mini Boss Card Album and MVP Card Album.
13. Test floor 100 and the victory BGM.
14. Verify timeout/cleanup and map flags.
15. Publish the patch version.

## Complete dungeon test checklist

- [ ] Entry fee works.
- [ ] Party leader restriction works.
- [ ] Global one-run lock works.
- [ ] Party is warped to `quiz_01`.
- [ ] Floor 1 starts after the initial delay.
- [ ] Every monster must die before the next floor.
- [ ] Every third floor spawns Gilded mini boss.
- [ ] Floors ending in 5 spawn bonus MVP.
- [ ] Floors ending in 10 spawn main MVP.
- [ ] Floor 100 spawns finale set.
- [ ] Normal mob alchemical drops occur.
- [ ] OCA follows server card-rate scaling.
- [ ] Mini Boss Card Album produces an eligible card.
- [ ] MVP Card Album produces an eligible card.
- [ ] Sage's Stone Cache produces guaranteed + random rewards.
- [ ] Alchemical Reliquary produces a random reward.
- [ ] Floor-depth reward multiplier increases with depth.
- [ ] Glass difficulty multiplier affects rewards.
- [ ] Player death/revive behavior works.
- [ ] Time limit removes players.
- [ ] Victory state cleans up after 30 seconds.
- [ ] Music changes at tier/boss/victory transitions.
- [ ] Patch client sees custom item names/icons.
- [ ] No custom item ID conflicts exist.

## Notes on the supplied source

The untouched supplied file is retained at `source/absinthe_tower_original.txt`. The expanded implementation is intentionally a separate file so the original can always be diffed/recovered.

The original design explicitly says it runs on an existing map and that unknown monster/item IDs are skipped at runtime. fileciteturn0file0L9-L14
