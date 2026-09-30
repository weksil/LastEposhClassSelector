# Mastery Roulette · Last Epoch

A one-page site with a roulette wheel that picks one of the 15 Last Epoch masteries and lays out every skill of its class, so you can sketch a build right away. It follows the Ascendancy Roulette (`D:\tmp\Poe2ClassSelector`): same wheel, modes, sound and settings.

- Open `index.html` in a browser, or serve the folder statically, e.g. `python -m http.server`.
- The wheel has 15 sectors, one per mastery, coloured by class. Each shows the mastery emblem at the rim and the mastery and class names along the radius. The sectors are shuffled on every load, and the page opens on whichever mastery the pointer is already aiming at.
- Two modes. **Single roll** draws one mastery. **Elimination** knocks the sector under the pointer off the wheel on every spin, keeps a ladder of who went out in which place, and crowns the last one standing. **Minimum spin** sets how long a spin lasts at the least (2–60 s).
- After a spin the page background switches to the art of that mastery, the page accent takes on the class colour, the winning sector lights up in gold and the name rises off the hub. A knockout throws embers in the class colours, shakes the wheel and strikes the name through.
- The wheel clacks on every sector edge (Web Audio, no files), and the pointer flaps like a peg wheel. The speaker button mutes the sound, and the sparkle button turns the effects off. Reduced motion is respected.
- **Wheel line-up**: click masteries to take them off the wheel. Two always stay on.
- Randomness comes from random.org, with `crypto.getRandomValues` as the fallback. The wheel starts turning on the click itself, so it never waits for the network.
- The character name generator makes Latin-letter names of 3–16 characters, flavoured by class.
- The badge links to [twitch.tv/blindermine](https://www.twitch.tv/blindermine).

## Build sketch

Under the wheel, for the mastery on show:

- the emblem, name, class and the in-game mastery description;
- the **mastery bonuses** you get for choosing it, and its **mastery skill**;
- **every skill of the class**, in five groups: that mastery (lit, first), the class skills unlocked by character level, the skills of the class passive tree, and the other two masteries of the class. Each tile says how the skill unlocks: *Level N*, *N points* in the tree, or *Mastery skill*. The mastery skill of another mastery is greyed out because it belongs to that mastery alone;
- hovering or tapping a tile opens the skill card: description, notes, mana cost, cooldown, speed, base damage, attribute scaling, scaling tags and where the skill comes from. The layout matches lastepochtools.com;
- a **five-slot skill bar**, like the game's. Click tiles to put skills on it or take them off. **Random five** fills it from random.org (the mastery skill always included), and **Copy build** copies `Mastery (Class): skill, skill, …` to the clipboard.

## Season 5 and new classes

The data is from Season 5, “Rage of the Frostborn” (1 October 2026). The season adds no new class or mastery, but it does add three skills and move two others:

| Mastery | Change |
|---|---|
| Bladedancer | new **Dreamslash**, 10 points in the tree |
| Paladin | new **Radiant Lance**, 15 points |
| Shaman | new **Summon Tide Elemental**, 30 points |
| Bladedancer | Synchronized Strike now needs 35 points (from 10) |
| Paladin | Symbols of Hope now needs 35 points (from 15) |

Forge Guard's second mastery bonus changed as well: Stalwart now gives 10% armour and also stacks when you hit.

**Stubs for announced skills.** A skill announced for a coming season can go into `UPCOMING` in `tools/meta.py`, with the season in `SEASON`. Until the data has it, it shows as a dashed stub in its mastery group:
- the mastery emblem stands in for the icon;
- the tooltip says when the season starts;
- the stub cannot go on the skill bar.

`build.py` drops a stub by itself once the data has a skill with the same English name. The list is empty now, since the three Season 5 skills are in the data.

The page is ready for a class added later:
- the wheel, line-up, build sketch and skill bar are all driven by `data/le.js`;
- a class without an entry in `CLASS_COLORS` is drawn in neutral gold;
- the name generator borrows the epithets of every class;
- a mastery without art in `assets/bg/` shows the plain backdrop.

To add a class, put it in `CLASSES` in `tools/meta.py`, rebuild, and add `assets/emblem/<key>.webp` and `assets/bg/<mastery>.webp`, plus colours and name epithets in `index.html` if you want them.

## Languages

All ten languages the game ships: English, Deutsch, Español, Français, 日本語, 한국어, Polski, Português (Brasil), Русский, 简体中文. Class, mastery and skill names, descriptions, bonuses and skill cards are the game's own texts, taken from lastepochtools.com. The interface strings are written for this page. A language whose card file is missing falls back to the English cards.

A known slip in the source: lastepochtools prints the Cold damage type as «Золото» (gold) in the Russian base-damage lines, in 10 skills including Maelstrom, Glacier and Frost Claw. `build.py` replaces it with «Холод».

## Settings and privacy

Language, mode, minimum spin, sound, effects and the wheel line-up live in one `localStorage` entry, `le-roulette-prefs`. It is written only when you change something, dropped after a year untouched, and cleared from the footer. There are no cookies and no analytics. The page makes requests to random.org, decapi.me / unavatar.io (the channel picture) and Google Fonts.

## Data

- `data/le.js`: 5 classes, 15 masteries and 141 skills with their unlock requirements, mana costs, and the names, descriptions and mastery bonuses in 10 languages. It comes from the lastepochtools.com data (version150, Season 5 “Rage of the Frostborn”; the folder is `DATA_VERSION` in `tools/meta.py`): `classSkillSources`, `masterySkillSources`, `LEAbilities` and the `i18n/full/<lang>.json` dictionaries.
- `data/skills/<lang>.js`: the skill cards, one file per language, loaded only when needed. They are captured from the rendered ability cards of lastepochtools.com and reduced to plain `div/span/ul/li` markup with a whitelist of classes; links, icons and inline styles are dropped.

### Rebuilding the data

The scripts are in `tools/`. Run them from inside that folder:

1. Download `https://www.lastepochtools.com/data/<version>/i18n/full/<lang>.json` for the ten languages into `tools/i18n/`, and the planner icon sprite (`.webp` + `.css`) as `tools/sprite.webp` / `tools/sprite.css`.
2. On a lastepochtools skills page, save `classSkillSources`, `masterySkillSources` and the fields of `LEAbilities.abilityList` used by `build.py` to `cls_src.json`, `mst_src.json` and `ab_src.json`.
3. For each language, pick it in the site's selector, run `harvest.js` in the console, and save `window.__res` as `tools/cards/<lang>.json`.
4. `python icons.py` cuts the icons. `python build.py` writes `data/le.js` and `data/skills/*.js`.

## Assets

- `assets/emblem/*.webp`: the 15 mastery emblems and 5 class emblems from the class pages of lastepoch.com.
- `assets/skills/*.webp`: 141 skill icons, cut from the lastepochtools.com icon sprite.
- `assets/bg/*.webp`: page backgrounds. Eleventh Hour Games publishes no wide artwork per mastery, so each mastery gets an official piece that fits its theme, from the lastepoch.com media kit and class pages:

| Mastery | Art |
|---|---|
| Beastmaster | Primalist key art (class page) |
| Shaman | Northern village under an aurora (game art) |
| Druid | Blooming garden (game art) |
| Sorcerer | Void rift tower (game art) |
| Spellblade | Season 5 “Rage of the Frostborn” key art: fire and ice |
| Runemaster | Cliffs with a glowing runic gate (game art) |
| Void Knight | Void crystal (game art) |
| Forge Guard | Golden hall (game art) |
| Paladin | Sentinel key art (class page) |
| Necromancer | Acolyte key art with the undead (class page) |
| Lich | Dark mountain fortress (game art) |
| Warlock | Crypt with ghostfire torches (game art) |
| Bladedancer | Rogue key art (class page) |
| Marksman | Forest cliffs (game art) |
| Falconer | River valley with a watchtower (game art) |

Last Epoch, its class names, texts and art © Eleventh Hour Games. Skill data and icons via lastepochtools.com.
