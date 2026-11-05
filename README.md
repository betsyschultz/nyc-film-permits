# nyc-film-permits

Which NYC blocks get taken over by film and TV shoots the most?

This project pulls every film permit from [NYC Open Data](https://data.cityofnewyork.us/d/tg4x-b46p) (published by the Mayor's Office of Media and Entertainment), breaks each permit's "parking held" field into individual street segments, and will map permits by zip code with a ranked list of the most-filmed streets.

## Status

- [x] Fetch all permits and cache them locally
- [x] Parse parking-held text into street segments (~67.5k segments, 9 unparseable)
- [ ] Count permits by zip and by street (DuckDB)
- [ ] Interactive zip heatmap and top streets list (JS)
- [ ] Daily refresh via GitHub Actions
- [ ] Publish on GitHub Pages

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 fetch.py
```

The first run downloads the dataset to `out/permits.json`. Later runs reuse that file and only re-parse. Output goes to `out/segments.json`, one row per held segment:

```json
{"event_id": "965623", "on_street": "35 STREET", "cross_from": "34 AVENUE", "cross_to": "35 AVENUE"}
```

## Data notes

- **The feed appears stalled.** The newest permit was entered on July 31, 2026, and the latest shoot starts August 3, 2026, even though the portal says the dataset refreshes daily. Coverage is January 2023 through July 2026.
- **No production titles.** Permits list a category (for example, Television / Episodic series) but not which show or film.
- **Multi-value fields.** `zipcode_s`, `communityboard_s`, and `policeprecinct_s` can hold several comma-separated values per permit.
- **Missing fields.** The API leaves out null fields entirely, so every field is treated as possibly missing.
- **One permit, many segments.** A single shoot can hold every side of a block, so street rankings count distinct permits, not segments.
