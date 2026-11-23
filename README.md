[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Avapage/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Avapage/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Image — Monday 23 November 2026

A newspaper front page that sums up one day of world news in a single
1024×1024 image: six stories, each cross-checked against at least two
news sources reporting on 23 November 2026 in some time zone.

- **COP31 climate talks collapse** — the Antalya summit ends with no
  deal after the EU rejects a pact that never mentions fossil fuels
  (BBC, NBC News, NPR, The Guardian).
- **Democrats hit 258 House seats** — the largest House majority since
  1992; Chuck Hubbard beats Virginia Foxx in the North Carolina
  recount (NYT, Washington Post, AP).
- **24 body bags in the Java factory fire** — 29 workers still missing
  after the candy-factory blaze; the search resumes Monday
  (BBC, Reuters).
- **Russia rolls out the Sarmat ICBM** — satellite images suggest the
  new nuclear missile is being loaded at Uzhur (IISS via Militarnyi,
  United24 Media, Clash Report).
- **Minister quits over AI cheating** — South Korea's education chief
  resigns after the CSAT exam-cheating scandal (Korea JoongAng Daily,
  The Guardian, AJP).
- **India's record 720 in Wellington** — the highest Test total ever in
  New Zealand; Rahul 136, Pant 128 (ESPNcricinfo, Cricbuzz,
  SuperSport).

## How the entry is made

`build_image.py` draws the front page with Pillow: flat vector-style
panels and DejaVu type, rendered at twice the final size and shrunk for
crisp text. `main.py` is the program the competition grades — standard
library only, no network — and it copies the committed `entry.png`
byte for byte into the output directory, so a second run writes the
same bytes as the first.

## Running it

```
python3 main.py
```

That writes `/output/entry.png`; set `MAKEFUN_OUTPUT_DIR` to choose a
different output directory. No build step is needed — the image is
already in the repository, and the program only copies it.
