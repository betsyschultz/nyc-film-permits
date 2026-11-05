import requests
import json
from pathlib import Path
import re

url = "https://data.cityofnewyork.us/resource/tg4x-b46p.json"
params = {"$limit": 25000}

TIMEOUT_S = 30

folder = Path(__file__).parent
out = folder / "out"
permit_path = out / "permits.json"
segments_path = out / "segments.json"

if not permit_path.is_file() or permit_path.stat().st_size == 0:
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT_S)
        response.raise_for_status()
        data = response.json()
        print(len(data), data[0].keys())

        with open(permit_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")

with open(permit_path, "r", encoding="utf-8") as f:
    data = json.load(f)
# dates
starts = [r["startdatetime"] for r in data if "startdatetime" in r]
print(f"min startdatetime: {min(starts)}, max startdatetime: {max(starts)}")

entered = [r["enteredon"] for r in data if "enteredon" in r]
print(f"last entry: {max(entered)}")

# parking held streets
parking_held = []
unparsed = []
for permit in data:
    if "parkingheld" in permit:
        chunks = permit["parkingheld"].split(',')
        for p in chunks:
            chunk = p.strip()
            if not chunk:
                continue
            m = re.fullmatch(r"(.+?)\s+between\s+(.+?)\s+and\s+(.+)", chunk)
            if not m:
                unparsed.append((permit["eventid"], chunk))
                continue
            on_street, cross_from, cross_to = (re.sub(r"\s+", " ", s).strip() for s in m.groups())
            parking_held.append({"event_id": permit["eventid"], "on_street": on_street, "cross_from": cross_from, "cross_to": cross_to})

with open(segments_path, "w", encoding="utf-8") as f:
    json.dump(parking_held, f)

print(len(parking_held), "segments,", len(unparsed), "unparsed")
print(parking_held[:5])
print(unparsed[:10])