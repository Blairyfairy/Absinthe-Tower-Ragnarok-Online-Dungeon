# Server package

Copy the contents of `server/db/import/` into the corresponding `db/import/` directory of the target rAthena checkout.

Copy `server/npc/absinthe_tower.txt` to your custom NPC directory, for example:

`npc/custom/absinthero/absinthe_tower.txt`

Then add:

`import: npc/custom/absinthero/absinthe_tower.txt`

to a loaded custom NPC `.conf` file.

The dungeon intentionally reuses the exact mob IDs from the supplied design. No custom mob database entries or mob sprites are required for the base implementation.
