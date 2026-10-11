# buni-arrivals

Predicting how long San Francisco buses and trains take between stops, trained on 511's record of when every vehicle actually reached every stop. The goal is better arrival times and smoother bus motion for [buni](https://polar3197.github.io/buni/support/), a live SF transit map for iPhone.

**Status:** just starting. Nothing to see yet.

## Layout

```
notebooks/   the work, in order
src/         shared code (scoring, data loading)
scripts/     data download
DATA.md      what the data is and where it goes
```

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

The data isn't in this repo; see [DATA.md](DATA.md) for getting it.

---

Transit data provided by [511.org](https://511.org). Not affiliated with SFMTA (Muni), BART, MTC, or 511.
