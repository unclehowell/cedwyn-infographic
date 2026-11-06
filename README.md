# cedwyn-infographic

"Land changing hands" — the Great House Farm (Tŷ Mawr) title-chain infographic, served at **bucklerfamily.estate/infographic/**.
Split from unclehowell/cedwyn (branch `infographic`); this repo is the source.

## Where the data lives (v3.10.0)

The repo is the single source of truth. There is no spreadsheet or server behind the page.

| file | what it holds |
| --- | --- |
| `data/maps.json` | the maps a parcel number can be read on (working model, 1824 Stewart plan, 1841 tithe map), with image and crop |
| `data/parcels.json` | one row per parcel number (1-59) per map: status, what is held, the identifying trait, crops and dots |
| `data/title_events.json` | each step of each title chain (freehold, registration, tenancy, occupancy, papers) with its sources |
| `data/settings.json` | single cells: `chain_for_A` (1) and `chain_for_B` (2) — the 1824 parcel that plays each line |
| `data/parties.json` | the parties named in the steps |
| `data/schema.graphql` | the types every row must match (GraphQL schema language) |
| `data/queries/*.graphql` | the persisted queries the build answers (the page's own is `db.graphql`) |
| `public/data/transfers.json`, `public/data/stewart-parcels.json` | the ring and the 59 parcel records (unchanged) |

Facts and the family position are kept apart: `trait`, `status`, `known` and `source` are what the records show;
`family_label` and `family_note` are the family position and the page always shows them as such. `review_flag` is an
editor-only note and is left out of everything the public page receives.

## How to edit

1. On GitHub, open the file under `data/` (for example `data/settings.json`), press the pencil, change the value, commit to `main`.
   One row per line; use `null` for an empty value; numbers without quotes; `known` is `true`/`false`.
   Example: to make parcel 3 play line B, change `"value": 2` to `"value": 3` on the `chain_for_B` row.
2. The **build-data** workflow (`.github/workflows/build-data.yml`) runs `python3 tools/build.py` on that push. It checks every row
   against `data/schema.graphql` and fails with a plain list of problems if something is wrong (a word where a number belongs,
   a missing field, a parcel outside 1-59, a party id that does not exist, a public word on the editorial blocklist). If it passes,
   it commits the rebuilt `public/index.html`, `public/sw.js` and `public/api/*.json`.
3. The rebuilt page reaches bucklerfamily.estate/infographic/ with the next split-repo sync and site publish.

Locally: `python3 tools/build.py` (or `--check` to validate only). Python 3 standard library only; nothing to install.

The old Google Sheet is no longer read by the page. `tools/import_sheet.py` can pull rows from it into `data/` once,
by hand (dry run by default, `--write` to apply); the repo wins.

## How it is served (serverless)

- **Compiled at build time.** `tools/gql.py` (a small, dependency-free GraphQL subset) runs each persisted query in
  `data/queries/` against the JSON tables and writes the answer to `public/api/<query>.json` — static files, no endpoint to keep
  up. The page's own query (`db`) is also inlined into `index.html`, so the first view needs no data request at all.
  Other apps read `/infographic/api/db.json`, `/infographic/api/title-chain.json` (each step with its parties) or
  `/infographic/api/stewart-parcels.json` (the 1824 parcels, facts and family position side by side).
- **Cached on the device.** `public/sw.js` (scope `/infographic/`) keeps the page and `title-chain/` in a cache named after the
  build, answers from it at once on repeat visits and offline, and revalidates with the server in the background
  (`cache: no-cache`, so the browser sends its validators). When the fresh copy carries a new build, open tabs show a small
  "Updated records · tap to refresh" button. It loads the site's own worker (`/cedwyn-sw.js`) inside it, so audio and data the
  site serves from its catalogue database behave as on every other page. `?sw=off` removes it from a browser.

## Files

- `tools/template.html` — the page; `tools/build.py` — checks and builds; `tools/gql.py` — schema checks and the query runner;
  `tools/sw.js` — the cache worker source; `tools/import_sheet.py` — optional one-way import.
- `public/` — what is published at /infographic/ (`index.html`, `sw.js`, `api/`, `title-chain/`, `audio/`, `data/`).

Compiled by Sion's Tab agent.
