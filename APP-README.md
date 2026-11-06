# infographic.bucklerfamily.estate — Great House Farm: the land changing hands

v3.10.0 (6 Nov 2026). The parcel database lives in the repo as typed JSON (data/*.json, schema data/schema.graphql); the build compiles the page's query into static JSON and the page itself, and a service worker keeps the page on the device for instant repeat visits and offline use. The linked workbook is no longer read. See README.md for how to edit.

v3.9.0 (6 Nov 2026). A parcel database (maps, parcels, title_events, settings) sits in a linked workbook and in public/data/db/; the page reads the workbook on each load and falls back to the committed copy. The dropdown lists only numbers something is held for; on the 1824 plan each bracket is the reference table's own name. 🗺️ Map opens the chosen map cropped to the parcel; Tenants: shown adds the tenancies beside the freehold lines; a parcel tied to line A or B by the family position plays that line (settings tab, one cell per line).

v3.8.0 (5 Nov 2026). The parcel dropdown lists the same 59 numbers on every map (working model, 1824 Stewart plan, 1841 tithe map); the map choice changes which records show beneath a number, never the list, and tithe plot numbers appear inside records only. The dropdown is a custom listbox whose rows carry a real status dot plus a status word: green/concrete where the figure is clearly read in the site's 1824 reading record and the parcel placed, with its record; amber/ambiguous where something is held even if ambiguous; red/none where nothing is held yet. Each number also carries its core identifying trait in brackets from the site's own per-parcel index, with every tithe match marked as the site's own reading. Under the working model the 59 parcels head the list and the ring's own lines sit in a separate group, not matched to parcel numbers.

v3.7.0 (5 Nov 2026). A Map dropdown (working model, 1824 Stewart plan, 1841 tithe plots) sits above the parcel dropdown; the pick draws only what the records tie to it, with text under the diagram.

v3.6.0 (4 Nov 2026). A dropdown lists the parcels of the 1824 Stewart plan, numbered 1-59; each number opens the record tied to that parcel (1841 tithe entries from the site's index, grid reference, traced area, and the farm's documented chain). The 30-39 / 50-59 figure readings are unsettled (old-style 3 or 5) and both are listed rather than excluding 46-59; unread figures and open source conflicts are stated as such. One circle. On the ring: title holders and official actors. Inside it: no title — the permissive occupancy ploys (💩, each with its year; 💩💩 = 1955), the two people named in the statement of Mary (Nancy) Williams (🦹 Bruce Sutherland, with Mr. Knapp, estate agent, above), and the shredded-paper icons (papers gone).

Data-status note: the 1877 A/B division is shown as the working model, not as a verified conveyance. The separate 1877 Clyde Street, Roath lease is excluded as a different property; a Great House Farm-specific instrument is still required to establish the proposed split.

The message: into the circle comes one farm, A + B, on the root title chain; out comes A + B again, but as synthetic A3 and B (merged at BP Properties, 1987), plus two simple lines, SA1 and SA2.

Lines (all drawn on load; the replay button draws one again from its start to its last official actor with narration; reduced motion draws it at once):
- **A+B IN:** Herbert family ★ → Vaughan family (1500s) → Bute Estate (early 1800s) → the 1877 split.
- **A:** + Bute Estate → Daniel Thomas & Son 1877 → Williams family 1928 → 🦹 1950 → papers gone. 1974: a line from the Williams family heads for the papers beside BP Pension Trust, turns back just short and returns.
- **B:** + Bute Estate → Mountjoy Ltd 1926 → Western Ground Rents 1938 → BP Pension Trust 1969 → BP Properties 1975, again 1982 → merges with SA3, 1987.
- **SA1 (woodland):** 💩 1949 → 💩💩 1955 → the 29 Mar 1961 deed naming Cardiff City Corporation (dashed; terms and extent not inspected), where the line stops. Separately, Ideal Homes → Forest of Cardiff 1994 (WA735527; the woodland title history has BP Properties → Ideal Homes, 3 Dec 1993). No transfer from Cardiff City Corporation is on record, so none is drawn.
- **SA2 (village green):** 💩💩 1955 → 💩 1959 → Glamorgan County Council 1970 (VG41, provisionally registered 16 June 1970); afterwards Llandough Community Council.
- **SA3 (house and yard):** 💩💩 1955 → 💩 1962 → 💩 1965 → 💩 1969 → BP Pension Trust 1969 → 💩 1971 → 💩 1974 → 💩 1975 → BP Properties 1975, again 1983 (WA240304) → merges with B, 1987.
- **SA3+B** draws both into the merge; **All** draws everything.

Each year sits where its line arrives. Dashed = the deed or record is not published here. Tap any line, pill or node for its record and sources; the list under the circle repeats the selected line's steps.

Data: `data/*.json` (maps, parcels, title_events, settings, parties; typed by `data/schema.graphql`) → persisted queries `data/queries/*.graphql` → `public/api/*.json`; `public/data/transfers.json` → `paths` (nodes, segs, filters); `public/data/stewart-parcels.json` → the 1-59 parcel records. Build: `tools/build.py` inlines both into `tools/template.html` and runs the public-words gate. Static, no external assets.

Compiled by Sion's Tab agent.
