# The World Today — 26 November 2026 in One Image

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/h05meigames2/news-26nov26-frontpage/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/h05meigames2/news-26nov26-frontpage/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for the [news-image-20261126 bounty](https://make.fun/bounty/news-image-20261126)
— "Sum up 26 November's world news in one image" ($100, top 50 share).

## What it is

A Python program that draws a newspaper front page for Thursday
26 November 2026 and writes it to `/output/entry.png` (1024×1024 PNG,
deterministic — two runs produce identical bytes, no network).

The front page, **"THE WORLD TODAY"**, leads with the Trump
administration readying new tariffs on China, the EU and 14 more
economies, beside a drawn Shenzhou-24 / Tiangong illustration. Eight
more stories follow in two columns — the first Pakistani astronaut
aboard China's space station, the Ukraine war spilling into Libya,
Russia's near-500,000 war toll, the Colombia hostage rescue, the
Mississippi plane crash, Xi's graft probe, the Solomon Islands–Australia
security treaty, and mines in the Strait of Hormuz — plus a
"By the numbers" strip and an "Also today" ticker.

## Run it

```sh
python3 gen_image.py        # renders entry.png in this directory
python3 main.py             # renders and writes /output/entry.png
```

Requires Python 3.13 and Pillow. No network access is used.

## License

MIT — see [LICENSE](LICENSE).
