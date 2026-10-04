# Client asset map

| Repo asset | Target client location | Notes |
|---|---|---|
| `source_art/*_item.bmp` | `data/texture/<client UI>/item/` | Inventory icon; exact encoded folder depends on client.
| `source_art/*_item.bmp` | `data/texture/<client UI>/collection/` | Collection/description image; resize/crop as needed.
| converted `*.spr/*.act` | `data/sprite/<client item folder>/` | Required by clients that use sprite-based drop icons.
| `client/lua/ItemInfo_AbsintheTower.lua` | `System/ItemInfo.lua` source | Merge, don't overwrite.
| `client/data/idnum2item*.txt` | matching legacy client tables | Merge, don't overwrite.
| `client/data/BGM/*.mid` | `BGM/` | Add to GRF/RGZ/Thor patch and ensure the client can resolve the names.

The exact Korean/encoded client folder names vary by client generation; use the target client's existing item resource paths as the authoritative names.
