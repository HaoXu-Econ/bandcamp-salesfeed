# Bandcamp sales feed collector

Collects Bandcamp's public sales feed (`https://bandcamp.com/api/salesfeed/1/get`) for an
academic data-science project (Université Paris Dauphine, M2). The feed only exposes the last
~10 minutes of sales, so a GitHub Actions job (`.github/workflows/collect.yml`) fetches it every
5 minutes and commits the raw response.

## Data

- `data/raw/YYYY-MM-DD/HHMMSS.json.gz`: one raw feed response per run (UTC run time).
- Each sale has: UTC timestamp, artist, item title, item type (track / album / physical package),
  price, amount paid (and in USD), currency, buyer country, item URL.
- Consecutive windows overlap: deduplicate on the sale timestamp + URL when parsing.
- Scheduled runs are sometimes delayed or skipped by GitHub, so coverage has gaps; the
  `start_date` / `end_date` of each file record which minutes were actually observed.

## Stop

Actions tab → `collect` → `...` → Disable workflow (or delete the repository).
