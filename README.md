# news-image-20-nov-2026-lucky-tapir-48

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20-nov-2026-lucky-tapir-48/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20-nov-2026-lucky-tapir-48/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One square image that sums up the world's news of Friday, 20 November 2026, for
make.fun's "Sum up 20 November's world news in one image" bounty, $250 in USDC.

Six stories that broke, or ran, on that Friday, each carried by its own drawn
icon and each tagged with its region, so the day's breadth shows at a glance:

| Region | Story | What happened |
| --- | --- | --- |
| Europe | Missiles hit Poland | Two Russian missiles and a suspected drone came down on Polish soil during a major overnight bombardment of Ukraine; NATO called it a grave violation of airspace and Poland's prime minister an intentional provocation. |
| Markets | Stocks in correction | US stocks slid into correction territory as an AI-driven selloff deepened, with the Nasdaq turning negative for the year. |
| Climate | COP31 runs overtime | Talks in Antalya ran past their deadline, deadlocked over fossil fuels and climate finance, with the draft deal dropping references to fossil fuels. |
| Asia | China nuclear buildup | A day after the Xi-Putin summit, Trump said China's nuclear buildup is "hot and heavy" and threatened penalties on AI data centres built abroad. |
| Middle East | Iran: no deal | Trump insisted Iran would not make an "acceptable" deal, as concern grew about next steps and strikes on tankers were reported. |
| Africa | 700,000 displaced | Around 700,000 people were displaced by conflict in southern Ethiopia. |

The image is 1024 x 1024 PNG, 86 KB, drawn entirely in code with no external
assets: every icon, rule and letterform is drawn by `draw.py` from the system's
Liberation faces. Redrawing it is deterministic, byte for byte.

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
python3 draw.py    # writes entry.png beside it
```

## Files

| Path | What it is |
| --- | --- |
| `main.ts` | The entry program: verifies and places `entry.png`. |
| `draw.py` | Draws the image. Standard library and Pillow only. |
| `entry.png` | The entry: 1024 x 1024, 86 KB. |
| `LICENSE` | MIT. |

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
