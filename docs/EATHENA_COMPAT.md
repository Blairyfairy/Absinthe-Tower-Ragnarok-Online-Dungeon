# eAthena / older-fork compatibility

This repository's primary target is **current rAthena**, because the supplied source is already written in rAthena script conventions and current rAthena uses YAML/import databases.

A genuine legacy eAthena fork may not support:

- YAML item databases
- YAML item groups
- `getbattleflag("item_rate_card_mvp")`
- `getmobdrops()` in the same form
- modern `playBGMall` naming/semantics

For that reason, `server/legacy/item_db2.txt` is a starting point for old text item databases, not a promise of byte-for-byte compatibility with every eAthena fork.

### Legacy port strategy

1. Keep the exact monster IDs from the original source.
2. Port the NPC syntax using your fork's script-command documentation/compiler.
3. Keep `ABT_RollCard` as the album engine if your fork supports `getmobdrops`; otherwise replace it with a static card-ID pool generated from your mob database.
4. Replace `getbattleflag("item_rate_card_mvp")` with the equivalent card-rate configuration variable in your fork.
5. Replace BGM calls with the fork's accepted BGM command.
6. Validate every custom item ID before adding it.

Do not copy a modern YAML file into a legacy eAthena server.
