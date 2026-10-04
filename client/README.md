# Client package

## Music

The supplied MIDIs are original small compositions made for this project:

- `data/BGM/absinthe_t1.mid` — floors 1-33
- `data/BGM/absinthe_t2.mid` — floors 34-66
- `data/BGM/absinthe_t3.mid` — floors 67-100
- `data/BGM/absinthe_boss.mid` — boss floors
- `data/BGM/absinthe_victory.mid` — clear music

The server script calls `playBGMall` with these names. Client-side music lookup varies by client generation; if your client expects a BGM table, add the files there and update the relevant `mp3nametable`/BGM resource mapping rather than editing the server script again.

## Custom items

For modern clients, merge `lua/ItemInfo_AbsintheTower.lua` into the appropriate ItemInfo source and compile back to `.lub` if your client requires compiled Lua.

For older clients, merge the supplied `idnum2item*.txt` fragments into the matching client tables.

The source art is under `source_art/` at repository level. The PNG/BMP files are reference art. Ragnarok clients that require `.spr/.act` need those files converted/created with a client-version-appropriate sprite tool. There is deliberately no universal `.spr/.act` binary because the required format/resource naming depends on the target client build.

No custom monster sprite is required: the dungeon uses the exact existing mob IDs and changes only their displayed dungeon name.
