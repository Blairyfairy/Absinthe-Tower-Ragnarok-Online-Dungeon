# Design and drop model

## Core crawl

- 100 floors.
- One party/run at a time in the supplied implementation.
- Floors 1-33, 34-66 and 67-100 use separate monster pools.
- Every third floor has one or two Gilded mini bosses depending on depth.
- Floors ending in 5 get a bonus MVP.
- Floors ending in 10 get a main MVP.
- Floor 100 uses the three configured finale MVP IDs.
- Floor 100 also gets a bonus MVP.

## Alchemical theme

The dungeon's progression revolves around the Philosopher's Stone / Sage's Stone concept:

- Philosopher's Stone Fragments are the common crawl material.
- The completed Philosopher's Stone is a rare MVP-tier reward.
- Flame Heart, Mystic Frozen, Rough Wind and Great Nature are the elemental reagent set.
- Sage's Stone Cache is a guaranteed-material + random-bonus box.
- Alchemical Reliquary is a weighted random reward box.

## Card reward model

The supplied script already uses the server's card rate as a multiplier for dungeon album rolls. This package further separates the multiplier by monster class:

- Normal: `item_rate_card`
- Gilded mini: `item_rate_card_boss`
- MVP: `item_rate_card_mvp`

The floor-depth multiplier is still applied, so the deeper crawl improves the chance of the dungeon's supplemental album/reward rolls without rewriting the server's normal monster card drops.

The rAthena drop configuration exposes separate common/boss/MVP and card/boss/MVP rate settings, so this is the intended place to align the dungeon with a server's card-rate policy. citeturn0search8

## OCA behavior

`Old Card Album` remains the server's normal OCA item. The two custom albums are dungeon-specific:

- `32103 Absinthe Mini Boss Card Album` -> rolls the configured mini-boss monster pool and returns a card from a selected mob's drop table.
- `32104 Absinthe MVP Card Album` -> rolls the main MVP, bonus MVP and finale MVP pools.

If an eligible mob has no card in its current database drops, the function falls back to an Old Card Album rather than giving an invalid item.

## Same mobs, dungeon-only rewards

No duplicate mob IDs are created. A Poring remains the same Poring ID, for example; the dungeon spawns it with the display name `Transmuted Poring`. This avoids duplicating sprites, AI and base monster definitions.
