# news-image-20-nov-2026-lucky-tapir-48

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20-nov-2026-lucky-tapir-48/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20-nov-2026-lucky-tapir-48/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page for Friday, 20 November 2026, in one square: 36 stories
from 7 regions, every one of them dated that day, laid out the way a broadsheet
sets its hierarchy. For make.fun's "Sum up 20 November's world news in one
image" bounty, $250 in USDC.

## What is on the page

A masthead names the day at the largest type on the sheet. Under it, a strip of
six numbers from the day, then the region key with each region's story count.
Then three leads, twelve cards, and twenty-one briefs, so the reader can stop at
any depth: the date, the teasers, the leads, the headlines, the one-liners.

The three leads:

1. **Russian missiles hit three Kyiv bridges.** An overnight barrage of 100-plus
   missiles and about 400 drones killed at least eight people across Ukraine and
   cut power and water in the capital.
2. **Cyclone Akvan comes ashore in eastern India.** It crossed near Gopalpur
   after more than 300,000 people were moved to shelters: the third severe
   cyclone on that coast in a month.
3. **An AI sell-off sinks Asia's markets.** Taiwan fell 6.2% for its worst week
   since 1991; Seoul lost 5.2% and Tokyo 5.1%, with chipmakers leading.

The rest of the day, across regions: the UK-EU reset deal, COP31 running past
its deadline with fossil fuels struck from the draft, a Russian missile landing
in Poland, Italy's general strike, the EU's \u20ac1bn in new military aid, Iraqi
troops entering Jurf al-Sakhar, Trump on Iran and on China's nuclear buildup,
Israeli strikes in southern Lebanon, 700,000 displaced in southern Ethiopia,
Kenya's first production oil well, Bukele's third-term bid, Bolsonaro
hospitalised, India and Japan deepening defence ties, South Korea's ruling party
moving to impeach the chief justice, Australia and China agreeing AI talks,
Wall Street in correction, Voyager 1 falling silent, and more.

Under the masthead, two strips give the day a spine: **the day in UTC**, a
seven-stop chronology from the Kyiv bridges at 00:00 to the S&P 500 closing in
correction, and **the day in numbers**, six figures worth stopping on. Every
story carries a stamp saying how solid it is, **CONFIRMED** where several outlets
or an official body have it, **REPORTED** where one named outlet does, **CLAIMED**
where it is someone's assertion. A dotted world map pins each story where it
happened, and a **date check** at the foot names what was left out and why, so the
one-day rule is visible rather than implied.

## How it is made

Drawn entirely in code with no external assets. `draw.py` composes the page from
a story list and a set of flat vector icons, all shapes drawn by hand: a bridge,
a cyclone, a chart, a trefoil, a derrick, a gavel, a cargo ship. Type is the
system's Liberation Serif and Sans. The page is drawn at 2x and downsampled, so
the small type stays clean at the size the judge reads it. Redrawing it is
deterministic, byte for byte.

`verify.py` checks the page geometrically, since a page that overflows a column
is a page that reads as broken: every one of the 204 text lines against the
margins and the band it belongs to, and every block against its own cell.

## Run it

```sh
node main.ts && open "${MAKEFUN_OUTPUT_DIR:-/output}/entry.png"
```

`main.ts` copies `entry.png` to the output directory and checks it against the
house's gate first: the PNG signature, an IHDR within 1024 on a side, and at
most 1 MiB. It exits non-zero rather than hand over an image the gate would
refuse.

To redraw the image from scratch:

```sh
python3 draw.py     # writes entry.png beside it
python3 verify.py   # checks the layout against its own geometry
```

## Files

| Path | What it is |
| --- | --- |
| `main.ts` | The entry program: verifies and places `entry.png`. |
| `draw.py` | Draws the page: layout, icons, story list. |
| `verify.py` | Checks the drawn page's geometry. |
| `entry.png` | The entry: 1024 x 1024, 427 KB. |
| `LICENSE` | MIT. |

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
