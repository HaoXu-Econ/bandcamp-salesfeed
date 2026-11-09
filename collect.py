"""Fetch the latest window (~10 min) of Bandcamp's public sales feed and save it raw.

One run = one file: data/raw/YYYY-MM-DD/HHMMSS.json.gz (UTC time of the run).
Consecutive runs overlap, so duplicates are removed later, at parsing time.
Standard library only, so the GitHub Actions job needs no installation step.
"""
import gzip
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

FEED_URL = "https://bandcamp.com/api/salesfeed/1/get?start_date={}"
USER_AGENT = "Mozilla/5.0 (compatible; academic-research-collector)"


def main() -> None:
    now = int(time.time())
    request = urllib.request.Request(FEED_URL.format(now - 600), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()

    feed = json.loads(body)  # stop here if Bandcamp did not return JSON
    n_items = sum(len(event.get("items", [])) for event in feed.get("events", []))
    if n_items == 0:
        sys.exit("feed returned no sales: the endpoint may have changed")

    run_time = datetime.fromtimestamp(now, tz=timezone.utc)
    out = Path("data/raw") / run_time.strftime("%Y-%m-%d") / f"{run_time:%H%M%S}.json.gz"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(gzip.compress(body))

    span_min = (feed["end_date"] - feed["start_date"]) / 60
    print(f"{out}: {n_items} sales, window {span_min:.1f} min")


if __name__ == "__main__":
    main()
