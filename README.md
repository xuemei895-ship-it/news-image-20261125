# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/xuemei895-ship-it/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/xuemei895-ship-it/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page that sums up the world news of Wednesday
25 November 2026 in a single 1024×1024 image: Zelenskiy confirming
Ukraine's drone strike on a Russian ship in the Gulf of Finland leads,
with five more top stories (the Houthi strike on Riyadh's tallest tower,
China's investigation of Politburo member Chen Jining, the US jury
convicting Huawei of trade-secret theft, Trump awarding Rudy Giuliani
the Medal of Freedom, and the Hamas security chief killed in Gaza)
plus a ticker of the day's other news.

## Run it

```sh
python3 main.py
```

The program copies `assets/entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`). It uses only the Python standard library:
no network, no randomness, no clock — two runs write identical bytes.

To regenerate the image from the stories, run `python3 generate.py`
(requires Pillow and the DejaVu fonts; it writes `assets/entry.png`).
Story sources are listed in `SOURCES.md`.

---

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards
